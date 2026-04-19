#!/usr/bin/env python3
"""
HALFTIME ENVIRONMENT CLASSIFIER

Classifies NBA halftime LiveFlow environments into:
- REAL_INFLATION
- FAKE_INFLATION
- REAL_SUPPRESSION
- FAKE_SUPPRESSION
- MIXED_NO_FIRE
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple
import json


@dataclass
class HalftimeTeamStats:
    team: str
    points: int
    fg_pct: float
    three_pct: float
    ftm: int
    fta: int
    rebounds: int
    offensive_rebounds: int
    assists: int
    turnovers: int
    second_chance_points: int = 0
    fastbreak_points: int = 0
    paint_points: int = 0
    leading_scorers: List[int] = None


@dataclass
class HalftimeEnvironmentInput:
    game: str
    closing_spread: float
    closing_total: float
    halftime_live_spread: float
    halftime_live_total: float
    halftime_score_team1: int
    halftime_score_team2: int
    team1_stats: HalftimeTeamStats
    team2_stats: HalftimeTeamStats


@dataclass
class HalftimeEnvironmentOutput:
    game: str
    environment_type: str
    confidence: float
    inflation_delta: float
    score_total_at_half: int
    notes: List[str]
    action_bias: str


def _safe_avg(values: List[float]) -> float:
    vals = [v for v in values if v is not None]
    return sum(vals) / len(vals) if vals else 0.0


def _count_double_digit_scorers(points_list: List[int]) -> int:
    return sum(1 for p in (points_list or []) if p >= 10)


def classify_environment(inp: HalftimeEnvironmentInput) -> HalftimeEnvironmentOutput:
    notes: List[str] = []
    inflation_delta = round(inp.halftime_live_total - inp.closing_total, 2)
    score_total = inp.halftime_score_team1 + inp.halftime_score_team2

    t1 = inp.team1_stats
    t2 = inp.team2_stats

    combined_assists = t1.assists + t2.assists
    combined_turnovers = t1.turnovers + t2.turnovers
    combined_fta = t1.fta + t2.fta
    combined_oreb = t1.offensive_rebounds + t2.offensive_rebounds
    avg_fg = _safe_avg([t1.fg_pct, t2.fg_pct])
    avg_three = _safe_avg([t1.three_pct, t2.three_pct])
    dbl_fig_scorers = _count_double_digit_scorers(t1.leading_scorers or []) + _count_double_digit_scorers(t2.leading_scorers or [])

    high_assist_environment = combined_assists >= 22
    balanced_scoring = dbl_fig_scorers >= 4
    whistle_heavy = combined_fta >= 26
    strong_extra_possessions = combined_oreb >= 9 or combined_turnovers >= 18
    hot_shooting = avg_fg >= 51.0 or avg_three >= 41.0
    cold_shooting = avg_fg <= 42.0 and avg_three <= 31.0

    continuation_score = 0
    regression_score = 0
    suppression_score = 0
    recovery_score = 0

    if inflation_delta >= 8:
        notes.append(f"halftime live total inflated by {inflation_delta} vs close")
        if high_assist_environment:
            continuation_score += 2
            notes.append("assist structure supports sustainable offense")
        else:
            regression_score += 1
            notes.append("assist profile not strong enough to fully validate inflation")

        if balanced_scoring:
            continuation_score += 2
            notes.append("multi-source scoring confirmed")
        else:
            regression_score += 1
            notes.append("scoring concentrated in limited sources")

        if whistle_heavy:
            regression_score += 1
            notes.append("free-throw volume may be inflating score")

        if strong_extra_possessions:
            continuation_score += 1
            notes.append("extra possessions support continuation")

        if hot_shooting and not high_assist_environment:
            regression_score += 2
            notes.append("hot shooting without strong ball movement suggests fragility")
        elif hot_shooting:
            continuation_score += 1
            notes.append("hot shooting supported by offensive structure")

        if continuation_score >= regression_score + 2:
            env = "REAL_INFLATION"
            confidence = min(0.90, 0.55 + 0.05 * continuation_score)
            action_bias = "DO_NOT_AUTO_FADE"
        elif regression_score >= continuation_score + 2:
            env = "FAKE_INFLATION"
            confidence = min(0.90, 0.55 + 0.05 * regression_score)
            action_bias = "LEAN_UNDER"
        else:
            env = "MIXED_NO_FIRE"
            confidence = 0.58
            action_bias = "NO_FIRE"

    elif inflation_delta <= -8:
        notes.append(f"halftime live total suppressed by {abs(inflation_delta)} vs close")
        if cold_shooting:
            recovery_score += 2
            notes.append("cold shooting suggests possible offensive rebound / scoring recovery")
        else:
            suppression_score += 1
            notes.append("shooting profile does not strongly indicate fake suppression")

        if strong_extra_possessions:
            recovery_score += 1
            notes.append("extra possessions suggest score may be artificially low")
        else:
            suppression_score += 1
            notes.append("low extra-possession pressure supports real suppression")

        if high_assist_environment:
            recovery_score += 1
            notes.append("offense still generating creation despite low score")
        else:
            suppression_score += 1
            notes.append("limited ball movement supports slow environment")

        if recovery_score >= suppression_score + 2:
            env = "FAKE_SUPPRESSION"
            confidence = min(0.90, 0.55 + 0.05 * recovery_score)
            action_bias = "LEAN_OVER"
        elif suppression_score >= recovery_score + 2:
            env = "REAL_SUPPRESSION"
            confidence = min(0.90, 0.55 + 0.05 * suppression_score)
            action_bias = "LEAN_UNDER"
        else:
            env = "MIXED_NO_FIRE"
            confidence = 0.58
            action_bias = "NO_FIRE"

    else:
        env = "MIXED_NO_FIRE"
        confidence = 0.52
        action_bias = "NO_FIRE"
        notes.append("repricing delta not extreme enough for strong halftime classification")

    return HalftimeEnvironmentOutput(
        game=inp.game,
        environment_type=env,
        confidence=round(confidence, 2),
        inflation_delta=inflation_delta,
        score_total_at_half=score_total,
        notes=notes,
        action_bias=action_bias,
    )


def output_to_json(output: HalftimeEnvironmentOutput) -> str:
    return json.dumps({"halftime_environment": asdict(output)}, indent=2)


if __name__ == "__main__":
    example = HalftimeEnvironmentInput(
        game="TOR @ CLE",
        closing_spread=-5.5,
        closing_total=216.5,
        halftime_live_spread=-8.5,
        halftime_live_total=228.5,
        halftime_score_team1=54,
        halftime_score_team2=61,
        team1_stats=HalftimeTeamStats(
            team="TOR",
            points=54,
            fg_pct=52.5,
            three_pct=53.3,
            ftm=4,
            fta=9,
            rebounds=15,
            offensive_rebounds=1,
            assists=16,
            turnovers=8,
            leading_scorers=[13, 11, 11, 11],
        ),
        team2_stats=HalftimeTeamStats(
            team="CLE",
            points=61,
            fg_pct=52.6,
            three_pct=47.1,
            ftm=13,
            fta=17,
            rebounds=18,
            offensive_rebounds=2,
            assists=12,
            turnovers=7,
            leading_scorers=[15, 13, 11, 9],
        ),
    )
    result = classify_environment(example)
    print(output_to_json(result))
