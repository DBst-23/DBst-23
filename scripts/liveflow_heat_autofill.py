from dataclasses import dataclass, asdict
import json
from typing import Dict, List


@dataclass
class TeamStats:
    team_name: str
    points: int
    fg_made: int
    fg_attempted: int
    three_made: int
    three_attempted: int
    ft_made: int
    ft_attempted: int
    offensive_rebounds: int
    turnovers: int
    fastbreak_points: int
    assists: int


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


def pct(made: int, attempted: int) -> float:
    if attempted <= 0:
        return 0.0
    return round((made / attempted) * 100.0, 2)


def combined_fg_pct(team_a: TeamStats, team_b: TeamStats) -> float:
    return pct(team_a.fg_made + team_b.fg_made, team_a.fg_attempted + team_b.fg_attempted)


def combined_3p_pct(team_a: TeamStats, team_b: TeamStats) -> float:
    return pct(team_a.three_made + team_b.three_made, team_a.three_attempted + team_b.three_attempted)


def combined_ft_pct(team_a: TeamStats, team_b: TeamStats) -> float:
    return pct(team_a.ft_made + team_b.ft_made, team_a.ft_attempted + team_b.ft_attempted)


def count_primary_scorers(team_scores: List[int], threshold: int = 10) -> int:
    return sum(1 for pts in team_scores if pts >= threshold)


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


def prompt_team_stats(team_name: str) -> TeamStats:
    print(f"\n=== Enter stats for {team_name} ===")
    return TeamStats(
        team_name=team_name,
        points=prompt_int("Points"),
        fg_made=prompt_int("FG made"),
        fg_attempted=prompt_int("FG attempted"),
        three_made=prompt_int("3PT made"),
        three_attempted=prompt_int("3PT attempted"),
        ft_made=prompt_int("FT made"),
        ft_attempted=prompt_int("FT attempted"),
        offensive_rebounds=prompt_int("Offensive rebounds"),
        turnovers=prompt_int("Turnovers"),
        fastbreak_points=prompt_int("Fastbreak points"),
        assists=prompt_int("Assists"),
    )


def build_autofilled_input(team_a: TeamStats, team_b: TeamStats) -> LiveFlowHeatInput:
    closing_total = prompt_float("\nClosing total")
    live_total = prompt_float("Live total")
    minutes_remaining = prompt_float("Minutes remaining")
    expected_fg_pct = prompt_float("Expected FG%", 46.0)
    expected_3p_pct = prompt_float("Expected 3P%", 36.0)
    expected_ft_pct = prompt_float("Expected FT%", 78.0)
    pace_z = prompt_float("Pace z-score", 0.0)
    oreb_z = prompt_float("Offensive rebound z-score", 0.0)
    fta_rate_z = prompt_float("FTA rate z-score", 0.0)
    fastbreak_z = prompt_float("Fastbreak z-score", 0.0)
    primary_scorers_count = prompt_int("Primary scorers count (10+ points)", 0)
    assist_rate_delta = prompt_float("Assist rate delta", 0.0)

    return LiveFlowHeatInput(
        closing_total=closing_total,
        live_total=live_total,
        current_total=team_a.points + team_b.points,
        minutes_remaining=minutes_remaining,
        current_fg_pct=combined_fg_pct(team_a, team_b),
        current_3p_pct=combined_3p_pct(team_a, team_b),
        current_ft_pct=combined_ft_pct(team_a, team_b),
        expected_fg_pct=expected_fg_pct,
        expected_3p_pct=expected_3p_pct,
        expected_ft_pct=expected_ft_pct,
        turnovers_total=team_a.turnovers + team_b.turnovers,
        offensive_rebounds_total=team_a.offensive_rebounds + team_b.offensive_rebounds,
        free_throw_attempts_total=team_a.ft_attempted + team_b.ft_attempted,
        fastbreak_points_total=team_a.fastbreak_points + team_b.fastbreak_points,
        pace_z=pace_z,
        oreb_z=oreb_z,
        fta_rate_z=fta_rate_z,
        fastbreak_z=fastbreak_z,
        primary_scorers_count=primary_scorers_count,
        assist_rate_delta=assist_rate_delta,
    )


def main() -> None:
    print("=== SharpEdge LiveFlow Heat Autofill Runner ===")
    print("Enter current box-score inputs. Percentages will be auto-derived from makes/attempts.")

    team_a_name = input("Team A name [Team A]: ").strip() or "Team A"
    team_b_name = input("Team B name [Team B]: ").strip() or "Team B"

    team_a = prompt_team_stats(team_a_name)
    team_b = prompt_team_stats(team_b_name)
    heat_input = build_autofilled_input(team_a, team_b)
    result = compute_liveflow_heat_index(heat_input)

    payload = {
        "team_a": asdict(team_a),
        "team_b": asdict(team_b),
        "heat_input": asdict(heat_input),
        "heat_result": result,
    }

    print("\n=== AUTOFILLED PAYLOAD ===")
    print(json.dumps(payload, indent=2))

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
