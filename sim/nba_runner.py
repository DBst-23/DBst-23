#!/usr/bin/env python3
"""
SharpEdge NBA Runner

Bridge-safe NBA simulation wrapper for GitHub Actions.
Routes projection through the main NBA totals engine, then adds market probability,
safety gating, and slate artifact output.
"""

from __future__ import annotations

import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sim.nba.nba_totals_engine import NBATotalsEngine, GameInputs, TeamProfile
from sim.nba.nba_pace_model import PaceContext
from sim.nba.sim.nba.hv_totals_guardrail import HVInputs

DEFAULT_INPUTS_PATH = "config/nba.slate.2026-04-30.json"
FALLBACK_INPUTS_PATH = "config/nba.inputs.sample.json"
DEFAULT_OUTPUTS_DIR = "outputs/nba/_wire_test"
MAX_PREGAME_CONFIDENCE = 0.74
VALIDATION_SPIKE_THRESHOLD = 0.80


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: Dict[str, Any], path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def american_fair_odds(probability: float) -> int:
    p = clamp(probability, 0.001, 0.999)
    if p >= 0.5:
        return round(-100 * p / (1 - p))
    return round(100 * (1 - p) / p)


def make_team_profile(team: Dict[str, Any], spread: float = 0.0, is_b2b: bool = False) -> TeamProfile:
    return TeamProfile(
        pace=float(team["pace"]),
        last10_pace=float(team.get("last10_pace", team["pace"])),
        off_rating=float(team["off_rating"]),
        def_rating=float(team["def_rating"]),
        trans_freq=float(team["transition_freq"]),
        trans_eff=float(team["transition_eff"]),
        def_trans_freq=float(team["def_transition_freq"]),
        def_trans_eff=float(team["def_transition_eff"]),
        long_reb_three_rate=float(team.get("three_rate", 0.40)),
        spread=spread,
        is_b2b=is_b2b,
    )


def make_hv_inputs(volatility: Dict[str, Any]) -> HVInputs:
    return HVInputs(
        high_shot_makers=bool(volatility.get("high_shot_makers", False)),
        high_transition_risk=bool(volatility.get("high_transition_risk", False)),
        low_tov_environment=bool(volatility.get("low_tov_environment", False)),
        high_three_volume_matchup=bool(volatility.get("high_three_volume_matchup", False)),
        recent_extreme_overs=int(volatility.get("recent_extreme_overs", 0)),
        pace_tier=float(volatility.get("pace_tier", 0.5)),
        halfcourt_offense_tier=float(volatility.get("halfcourt_offense_tier", 0.5)),
        halfcourt_defense_weak_tier=float(volatility.get("halfcourt_defense_weak_tier", 0.5)),
    )


def make_pace_context(context: Dict[str, Any]) -> PaceContext:
    return PaceContext(
        is_back_to_back_home=bool(context.get("home_b2b", False)),
        is_back_to_back_away=bool(context.get("away_b2b", False)),
        altitude_game=bool(context.get("altitude_game", False)),
        projected_close_spread=float(context.get("projected_close_spread", 5.0)),
        playoff_intensity=bool(context.get("playoff_intensity", False)),
    )


def classify_probability(raw_probability: float) -> Dict[str, Any]:
    validation_required = raw_probability >= VALIDATION_SPIKE_THRESHOLD
    capped_probability = min(raw_probability, MAX_PREGAME_CONFIDENCE)
    return {
        "raw_probability": round(raw_probability, 4),
        "display_probability": round(capped_probability, 4),
        "validation_required": validation_required,
        "cap_applied": raw_probability > MAX_PREGAME_CONFIDENCE,
        "confidence_ceiling": MAX_PREGAME_CONFIDENCE,
        "reason": "Pregame edge probability exceeded safety ceiling; requires secondary validation before bet-grade use."
        if raw_probability > MAX_PREGAME_CONFIDENCE else "Within pregame confidence range.",
    }


def tier_from_probability(probability: float, validation_required: bool) -> str:
    if validation_required:
        return "validation_required"
    if probability < 0.57:
        return "watch"
    if probability < 0.65:
        return "actionable"
    return "strong"


def simulate_nba(inputs: Dict[str, Any]) -> Dict[str, Any]:
    home = inputs["teams"]["home"]
    away = inputs["teams"]["away"]
    context = inputs.get("context", {})
    market = inputs.get("market", {})
    volatility = inputs.get("volatility", {})

    home_spread = float(market.get("home_spread", 0.0))
    engine_inputs = GameInputs(
        home=make_team_profile(home, spread=home_spread, is_b2b=bool(context.get("home_b2b", False))),
        away=make_team_profile(away, spread=-home_spread, is_b2b=bool(context.get("away_b2b", False))),
        hv_inputs=make_hv_inputs(volatility),
        context=make_pace_context(context),
    )
    engine_projection = NBATotalsEngine.simulate_total(engine_inputs)

    total_mean = float(engine_projection["final_total_mean"])
    total_median = float(engine_projection["final_total_median"])
    total_line = float(market.get("total_line", round(total_mean, 1)))
    total_stdev = clamp(13.5 + float(engine_projection.get("hv_risk_score", 0.0)) * 0.95, 12.0, 19.5)

    over_probability = 1.0 - normal_cdf((total_line - total_mean) / total_stdev)
    under_probability = 1.0 - over_probability

    home_rating_edge = (float(home["off_rating"]) - float(away["def_rating"])) - (
        float(away["off_rating"]) - float(home["def_rating"])
    )
    home_margin_mean = home_rating_edge * 0.42 - home_spread * 0.18
    margin_stdev = 12.5
    home_win_probability = normal_cdf(home_margin_mean / margin_stdev)
    away_win_probability = 1.0 - home_win_probability

    edge_vs_total_line = total_mean - total_line
    if edge_vs_total_line > 0:
        side = "OVER"
        raw_side_probability = over_probability
    else:
        side = "UNDER"
        raw_side_probability = under_probability

    safety = classify_probability(raw_side_probability)
    display_probability = safety["display_probability"]

    return {
        "game": inputs["game"],
        "sport": "nba",
        "mode": inputs.get("mode", "B003_NBA_TOTALS_PREFLIGHT"),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "simulated": True,
        "model_version": "NBA_B003_MAIN_ENGINE_ADAPTER_V1",
        "engine_status": {
            "runner_type": "main_engine_adapter",
            "main_engine_validated": True,
            "main_engine_path": "sim/nba/nba_totals_engine.py",
            "pace_engine_path": "sim/nba/nba_pace_model.py",
            "transition_engine_path": "sim/nba/transition_patch.py",
            "hv_guardrail_path": "sim/nba/sim/nba/hv_totals_guardrail.py",
        },
        "market": market,
        "projection": {
            "pace": round(float(engine_projection["pace"]), 3),
            "home_ppp": round(float(engine_projection["home_ppp"]), 4),
            "away_ppp": round(float(engine_projection["away_ppp"]), 4),
            "raw_total": round(float(engine_projection["raw_total"]), 3),
            "transition_patched_total": round(float(engine_projection["transition_patched_total"]), 3),
            "transition_delta_points": round(float(engine_projection["transition_delta"]), 3),
            "hv_risk_score": round(float(engine_projection.get("hv_risk_score", 0.0)), 3),
            "hv_volatility_boost": round(float(engine_projection.get("hv_volatility_boost", 0.0)), 3),
            "hv_under_cap_active": bool(engine_projection.get("hv_under_cap_active", False)),
            "total_mean": round(total_mean, 3),
            "total_median": round(total_median, 3),
            "total_stdev": round(total_stdev, 3),
            "edge_vs_total_line": round(edge_vs_total_line, 3),
        },
        "probabilities": {
            "over_probability": round(over_probability, 4),
            "under_probability": round(under_probability, 4),
            "home_win_probability": round(home_win_probability, 4),
            "away_win_probability": round(away_win_probability, 4),
            "line_probabilities": {
                "total_over": round(over_probability, 4),
                "total_under": round(under_probability, 4),
                "home_ml": round(home_win_probability, 4),
                "away_ml": round(away_win_probability, 4),
            },
        },
        "edge": {
            "side": side,
            "raw_probability": safety["raw_probability"],
            "probability": display_probability,
            "fair_american_odds": american_fair_odds(display_probability),
            "edge_points": round(abs(edge_vs_total_line), 3),
            "tier": tier_from_probability(display_probability, safety["validation_required"]),
            "safety_gate": safety,
        },
    }


def summarize_slate(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    ranked = sorted(results, key=lambda row: row["edge"]["raw_probability"], reverse=True)
    return {
        "game_count": len(results),
        "top_edge": ranked[0]["game"] if ranked else None,
        "top_edge_side": ranked[0]["edge"]["side"] if ranked else None,
        "top_edge_raw_probability": ranked[0]["edge"]["raw_probability"] if ranked else None,
        "top_edge_display_probability": ranked[0]["edge"]["probability"] if ranked else None,
        "actionable_count": sum(1 for row in results if row["edge"]["tier"] in {"actionable", "strong"}),
        "strong_count": sum(1 for row in results if row["edge"]["tier"] == "strong"),
        "validation_required_count": sum(1 for row in results if row["edge"]["tier"] == "validation_required"),
    }


def run_simulation() -> None:
    input_path = DEFAULT_INPUTS_PATH if Path(DEFAULT_INPUTS_PATH).exists() else FALLBACK_INPUTS_PATH
    inputs = load_json(input_path)

    if "games" in inputs:
        results = [simulate_nba(game) for game in inputs["games"]]
        payload = {
            "slate_date": inputs.get("slate_date"),
            "sport": "nba",
            "mode": inputs.get("mode", "B003_NBA_SLATE_PREFLIGHT"),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "data_quality_note": inputs.get("data_quality_note"),
            "summary": summarize_slate(results),
            "results": results,
        }

        print("Loaded NBA slate:", payload["slate_date"])
        print("Games:", payload["summary"]["game_count"])
        print("Top edge:", payload["summary"]["top_edge"], payload["summary"]["top_edge_side"], payload["summary"]["top_edge_raw_probability"])
        print("Validation required:", payload["summary"]["validation_required_count"])

        output_path = os.path.join(DEFAULT_OUTPUTS_DIR, "nba_slate_edges.json")
        save_json(payload, output_path)
        print(f"✅ NBA slate simulation complete. Output saved to {output_path}")
        return

    result = simulate_nba(inputs)
    print("Loaded NBA game:", result["game"])
    print("Mode:", result["mode"])
    print("Mean:", result["projection"]["total_mean"])
    print("Median:", result["projection"]["total_median"])
    print("Edge:", result["edge"])

    output_path = os.path.join(DEFAULT_OUTPUTS_DIR, "nba_full_game_edges.json")
    save_json(result, output_path)
    print(f"✅ NBA simulation complete. Output saved to {output_path}")


if __name__ == "__main__":
    run_simulation()
