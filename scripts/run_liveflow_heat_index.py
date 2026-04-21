from dataclasses import dataclass, asdict
import json
from typing import Dict


@dataclass
class LiveFlowHeatInput:
    closing_total: float
    live_total: float
    current_total: int
    minutes_remaining: float

    current_fg_pct: float
    current_3p_pct: float
    current_ft_pct: float

    expected_fg_pct: float
    expected_3p_pct: float
    expected_ft_pct: float

    turnovers_total: int
    offensive_rebounds_total: int
    free_throw_attempts_total: int
    fastbreak_points_total: int

    pace_z: float = 0.0
    oreb_z: float = 0.0
    fta_rate_z: float = 0.0
    fastbreak_z: float = 0.0

    primary_scorers_count: int = 0
    assist_rate_delta: float = 0.0


def compute_liveflow_heat_index(inp: LiveFlowHeatInput) -> Dict:
    fg_delta = max(0.0, inp.current_fg_pct - inp.expected_fg_pct)
    tp_delta = max(0.0, inp.current_3p_pct - inp.expected_3p_pct)
    ft_delta = max(0.0, inp.current_ft_pct - inp.expected_ft_pct)

    shooting_heat_score = (
        fg_delta * 0.8 +
        tp_delta * 1.4 +
        ft_delta * 0.3
    )

    pace_support_score = (
        inp.pace_z * 1.2 +
        inp.oreb_z * 0.8 +
        inp.fta_rate_z * 0.7 +
        inp.fastbreak_z * 0.6
    )

    clean_possession_penalty = 0
    if inp.turnovers_total <= 10:
        clean_possession_penalty += 8
    if inp.offensive_rebounds_total <= 10:
        clean_possession_penalty += 6
    if inp.free_throw_attempts_total <= 20:
        clean_possession_penalty += 5

    market_inflation = max(0.0, inp.live_total - inp.closing_total)
    market_inflation_score = market_inflation * 2.0

    required_remaining_points = inp.live_total - inp.current_total
    baseline_ppm = inp.closing_total / 48.0
    required_ppm = required_remaining_points / max(inp.minutes_remaining, 1.0)

    if required_ppm > baseline_ppm + 0.25:
        market_inflation_score += 10

    star_sustainability_offset = 0
    if inp.primary_scorers_count >= 3:
        star_sustainability_offset += 8
    if inp.assist_rate_delta >= 0:
        star_sustainability_offset += 5
    if pace_support_score >= 12:
        star_sustainability_offset += 5

    heat_index = (
        shooting_heat_score +
        market_inflation_score +
        clean_possession_penalty -
        pace_support_score -
        star_sustainability_offset
    )

    heat_index = max(0, min(100, round(heat_index)))

    if heat_index < 25:
        classification = "COOL"
        action_tag = "NO_EDGE"
    elif heat_index < 45:
        classification = "WARM"
        action_tag = "WATCH_UNDER"
    elif heat_index < 65:
        classification = "HOT"
        action_tag = "UNDER_TRIGGER"
    else:
        classification = "EXTREME_HEAT"
        action_tag = "UNDER_TRIGGER"

    if pace_support_score >= 14 and inp.primary_scorers_count >= 3 and inp.free_throw_attempts_total >= 20:
        action_tag = "DO_NOT_FADE"

    return {
        "heat_index": heat_index,
        "classification": classification,
        "action_tag": action_tag,
        "shooting_heat_score": round(shooting_heat_score, 2),
        "market_inflation_score": round(market_inflation_score, 2),
        "clean_possession_penalty": clean_possession_penalty,
        "pace_support_score": round(pace_support_score, 2),
        "star_sustainability_offset": star_sustainability_offset,
        "required_remaining_points": round(required_remaining_points, 2),
        "required_points_per_minute": round(required_ppm, 3),
    }


def prompt_float(label: str, default: float = 0.0) -> float:
    raw = input(f"{label} [{default}]: ").strip()
    return float(raw) if raw else float(default)


def prompt_int(label: str, default: int = 0) -> int:
    raw = input(f"{label} [{default}]: ").strip()
    return int(raw) if raw else int(default)


def main() -> None:
    print("=== SharpEdge LiveFlow Heat Index Runner ===")
    print("Enter percentages as whole numbers, e.g. 47.8 for 47.8%")

    inp = LiveFlowHeatInput(
        closing_total=prompt_float("Closing total"),
        live_total=prompt_float("Live total"),
        current_total=prompt_int("Current total points"),
        minutes_remaining=prompt_float("Minutes remaining"),
        current_fg_pct=prompt_float("Current FG%"),
        current_3p_pct=prompt_float("Current 3P%"),
        current_ft_pct=prompt_float("Current FT%"),
        expected_fg_pct=prompt_float("Expected FG%", 46.0),
        expected_3p_pct=prompt_float("Expected 3P%", 36.0),
        expected_ft_pct=prompt_float("Expected FT%", 78.0),
        turnovers_total=prompt_int("Total turnovers"),
        offensive_rebounds_total=prompt_int("Total offensive rebounds"),
        free_throw_attempts_total=prompt_int("Total FTA"),
        fastbreak_points_total=prompt_int("Total fastbreak points"),
        pace_z=prompt_float("Pace z-score", 0.0),
        oreb_z=prompt_float("Offensive rebound z-score", 0.0),
        fta_rate_z=prompt_float("FTA rate z-score", 0.0),
        fastbreak_z=prompt_float("Fastbreak z-score", 0.0),
        primary_scorers_count=prompt_int("Primary scorers count", 0),
        assist_rate_delta=prompt_float("Assist rate delta", 0.0),
    )

    result = compute_liveflow_heat_index(inp)

    print("\n=== INPUT SNAPSHOT ===")
    print(json.dumps(asdict(inp), indent=2))
    print("\n=== HEAT INDEX RESULT ===")
    print(json.dumps(result, indent=2))

    if result["action_tag"] == "UNDER_TRIGGER":
        print("\nSharpEdge Read: Fade the heat. Live under environment detected.")
    elif result["action_tag"] == "WATCH_UNDER":
        print("\nSharpEdge Read: Warm environment. Watch for a better under entry.")
    elif result["action_tag"] == "DO_NOT_FADE":
        print("\nSharpEdge Read: Real continuation environment. Do not auto-fade.")
    else:
        print("\nSharpEdge Read: No actionable heat edge.")


if __name__ == "__main__":
    main()
