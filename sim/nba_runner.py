#!/usr/bin/env python3
"""
SharpEdge NBA Runner

Stable bridge-safe NBA simulation wrapper for GitHub Actions.
Produces JSON artifacts with mean, median, edge, probability, and game-line probability fields.
Supports either a single-game config or a multi-game slate config with a top-level `games` array.
"""

from __future__ import annotations

import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_INPUTS_PATH = "config/nba.slate.2026-04-30.json"
FALLBACK_INPUTS_PATH = "config/nba.inputs.sample.json"
DEFAULT_OUTPUTS_DIR = "outputs/nba/_wire_test"


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


def blended_pace(home: Dict[str, Any], away: Dict[str, Any], context: Dict[str, Any]) -> float:
    home_pace = 0.65 * float(home["pace"]) + 0.35 * float(home.get("last10_pace", home["pace"]))
    away_pace = 0.65 * float(away["pace"]) + 0.35 * float(away.get("last10_pace", away["pace"]))
    pace = (home_pace + away_pace) / 2.0

    if context.get("home_b2b"):
        pace -= 1.0
    if context.get("away_b2b"):
        pace -= 1.0
    if context.get("altitude_game"):
        pace += 1.0
    if float(context.get("projected_close_spread", 6.0)) <= 4.0:
        pace += 0.8
    if context.get("playoff_intensity"):
        pace -= 0.7

    return round(clamp(pace, 92.0, 110.0), 3)


def transition_delta(home: Dict[str, Any], away: Dict[str, Any]) -> float:
    freq_ref = 0.18
    eff_ref = 1.20

    home_pressure = (float(home["transition_freq"]) / freq_ref - 1.0) * 0.6
    home_eff = (float(home["transition_eff"]) / eff_ref - 1.0) * 0.4
    away_pressure = (float(away["transition_freq"]) / freq_ref - 1.0) * 0.6
    away_eff = (float(away["transition_eff"]) / eff_ref - 1.0) * 0.4

    defensive_leak = (
        (float(home["def_transition_freq"]) / freq_ref - 1.0)
        + (float(away["def_transition_freq"]) / freq_ref - 1.0)
    ) * 0.5

    raw_pct = (home_pressure + home_eff + away_pressure + away_eff + defensive_leak) / 3.0
    raw_pct = clamp(raw_pct, -0.08, 0.08)
    return raw_pct


def volatility_guardrail(base_total: float, volatility: Dict[str, Any]) -> Dict[str, Any]:
    score = 0.0
    if volatility.get("high_shot_makers"):
        score += 1.2
    if volatility.get("high_transition_risk"):
        score += 1.0
    if volatility.get("low_tov_environment"):
        score += 0.8
    if volatility.get("high_three_volume_matchup"):
        score += 1.0

    recent_extreme_overs = int(volatility.get("recent_extreme_overs", 0))
    if recent_extreme_overs >= 1:
        score += 0.7
    if recent_extreme_overs >= 2:
        score += 0.5

    if float(volatility.get("pace_tier", 0.5)) > 0.70:
        score += 0.6
    if float(volatility.get("pace_tier", 0.5)) > 0.85:
        score += 0.4

    combined_halfcourt = 0.5 * (
        float(volatility.get("halfcourt_offense_tier", 0.5))
        + float(volatility.get("halfcourt_defense_weak_tier", 0.5))
    )
    if combined_halfcourt > 0.65:
        score += 0.6
    if combined_halfcourt > 0.80:
        score += 0.5

    score = clamp(score, 0.0, 6.0)
    boost = clamp(base_total * 0.015 * score, 0.0, 8.0)

    return {
        "risk_score": round(score, 3),
        "volatility_boost": round(boost, 3),
        "under_cap_active": score >= 3.0,
    }


def simulate_nba(inputs: Dict[str, Any]) -> Dict[str, Any]:
    home = inputs["teams"]["home"]
    away = inputs["teams"]["away"]
    context = inputs.get("context", {})
    market = inputs.get("market", {})
    volatility = inputs.get("volatility", {})

    pace = blended_pace(home, away, context)
    home_ppp = (float(home["off_rating"]) + float(away["def_rating"])) / 200.0
    away_ppp = (float(away["off_rating"]) + float(home["def_rating"])) / 200.0

    raw_total = (home_ppp + away_ppp) * pace
    trans_pct = transition_delta(home, away)
    trans_points = raw_total * trans_pct
    hv = volatility_guardrail(raw_total, volatility)

    total_mean = raw_total + trans_points + hv["volatility_boost"]
    total_median = total_mean * 0.985

    total_line = float(market.get("total_line", round(total_mean, 1)))
    total_stdev = clamp(12.0 + hv["risk_score"] * 0.85, 10.0, 18.0)
    over_probability = 1.0 - normal_cdf((total_line - total_mean) / total_stdev)
    under_probability = 1.0 - over_probability

    home_rating_edge = (float(home["off_rating"]) - float(away["def_rating"])) - (
        float(away["off_rating"]) - float(home["def_rating"])
    )
    home_spread = float(market.get("home_spread", 0.0))
    home_margin_mean = home_rating_edge * 0.42 - home_spread * 0.18
    margin_stdev = 12.5
    home_win_probability = normal_cdf(home_margin_mean / margin_stdev)
    away_win_probability = 1.0 - home_win_probability

    edge_vs_total_line = total_mean - total_line

    if edge_vs_total_line > 0:
        side = "OVER"
        side_probability = over_probability
    else:
        side = "UNDER"
        side_probability = under_probability

    return {
        "game": inputs["game"],
        "sport": "nba",
        "mode": inputs.get("mode", "B003_NBA_TOTALS_PREFLIGHT"),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "simulated": True,
        "model_version": "NBA_B003_BRIDGE_RUNNER_V2_SLATE",
        "market": market,
        "projection": {
            "pace": pace,
            "home_ppp": round(home_ppp, 4),
            "away_ppp": round(away_ppp, 4),
            "raw_total": round(raw_total, 3),
            "transition_delta_pct": round(trans_pct, 4),
            "transition_delta_points": round(trans_points, 3),
            "hv_risk_score": hv["risk_score"],
            "hv_volatility_boost": hv["volatility_boost"],
            "hv_under_cap_active": hv["under_cap_active"],
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
            "probability": round(side_probability, 4),
            "fair_american_odds": american_fair_odds(side_probability),
            "edge_points": round(abs(edge_vs_total_line), 3),
            "tier": "watch" if side_probability < 0.57 else "actionable" if side_probability < 0.65 else "strong",
        },
    }


def summarize_slate(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    ranked = sorted(results, key=lambda row: row["edge"]["probability"], reverse=True)
    return {
        "game_count": len(results),
        "top_edge": ranked[0]["game"] if ranked else None,
        "top_edge_side": ranked[0]["edge"]["side"] if ranked else None,
        "top_edge_probability": ranked[0]["edge"]["probability"] if ranked else None,
        "actionable_count": sum(1 for row in results if row["edge"]["tier"] in {"actionable", "strong"}),
        "strong_count": sum(1 for row in results if row["edge"]["tier"] == "strong"),
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
        print("Top edge:", payload["summary"]["top_edge"], payload["summary"]["top_edge_side"], payload["summary"]["top_edge_probability"])

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
