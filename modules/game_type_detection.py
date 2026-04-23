"""
SharpEdge NBA Game Type Detection Module V1

Purpose:
- classify NBA games into reusable environment buckets
- support live and postmortem tagging
- connect totals / spread / team-total logic to game texture

Current supported game archetypes:
1. COLLAPSE_UNDER_ENVIRONMENT
2. CONTROLLED_EFFICIENCY_ENVIRONMENT
3. REACTIVE_REBOUND_ENVIRONMENT
4. PHYSICAL_REBOUND_DOMINANCE_ENVIRONMENT
5. SPREAD_INFLATION_FADE
6. TT_SPLIT_EDGE

The module is intentionally rule-based so it can be audited and tuned quickly.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class GameTypeResult:
    primary_game_type: str
    tags: List[str]
    scores: Dict[str, float]
    betting_implications: Dict[str, str]
    notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _safe_div(a: float, b: float) -> float:
    return a / b if b else 0.0


def detect_game_types(
    *,
    halftime_total_points: int,
    final_total_points: int | None = None,
    favorite_halftime_points: int,
    underdog_halftime_points: int,
    favorite_final_points: int | None = None,
    underdog_final_points: int | None = None,
    live_full_game_total: float | None = None,
    live_favorite_team_total: float | None = None,
    live_underdog_team_total: float | None = None,
    live_spread: float | None = None,
    favorite_off_rtg_1h: float | None = None,
    underdog_off_rtg_1h: float | None = None,
    favorite_ts_1h: float | None = None,
    underdog_ts_1h: float | None = None,
    favorite_tov_1h: int | None = None,
    underdog_tov_1h: int | None = None,
    favorite_oreb_final: int | None = None,
    underdog_oreb_final: int | None = None,
    favorite_reb_final: int | None = None,
    underdog_reb_final: int | None = None,
    favorite_boxouts: float | None = None,
    underdog_boxouts: float | None = None,
    favorite_fg_pct_final: float | None = None,
    underdog_fg_pct_final: float | None = None,
    favorite_3p_pct_final: float | None = None,
    underdog_3p_pct_final: float | None = None,
) -> GameTypeResult:
    """
    Classify a game environment using live + postmortem signals.

    Percentages should be passed in normal percent units, e.g. 45.9 not 0.459.
    """

    scores: Dict[str, float] = {
        "COLLAPSE_UNDER_ENVIRONMENT": 0.0,
        "CONTROLLED_EFFICIENCY_ENVIRONMENT": 0.0,
        "REACTIVE_REBOUND_ENVIRONMENT": 0.0,
        "PHYSICAL_REBOUND_DOMINANCE_ENVIRONMENT": 0.0,
        "SPREAD_INFLATION_FADE": 0.0,
        "TT_SPLIT_EDGE": 0.0,
    }
    notes: List[str] = []

    second_half_needed_for_over = None
    if live_full_game_total is not None:
        second_half_needed_for_over = live_full_game_total - halftime_total_points

    halftime_margin = favorite_halftime_points - underdog_halftime_points

    # Collapse under environment
    if final_total_points is not None and favorite_final_points is not None and underdog_final_points is not None:
        low_conversion_team = False
        if favorite_fg_pct_final is not None and favorite_fg_pct_final < 38.0:
            low_conversion_team = True
        if underdog_fg_pct_final is not None and underdog_fg_pct_final < 38.0:
            low_conversion_team = True

        heavy_possession_noise = False
        if favorite_oreb_final is not None and underdog_oreb_final is not None:
            if favorite_oreb_final + underdog_oreb_final >= 24:
                heavy_possession_noise = True

        if low_conversion_team:
            scores["COLLAPSE_UNDER_ENVIRONMENT"] += 4.0
            notes.append("At least one team finished with severe shotmaking failure.")
        if heavy_possession_noise:
            scores["COLLAPSE_UNDER_ENVIRONMENT"] += 2.0
            notes.append("Game had rebound/extra-possession noise without efficient scoring carryover.")
        if final_total_points <= 190:
            scores["COLLAPSE_UNDER_ENVIRONMENT"] += 2.0
            notes.append("Final total closed in clear under-collapse territory.")

    # Controlled efficiency environment
    if favorite_ts_1h is not None and underdog_ts_1h is not None:
        if favorite_ts_1h >= 60.0 and underdog_ts_1h >= 58.0:
            scores["CONTROLLED_EFFICIENCY_ENVIRONMENT"] += 3.0
            notes.append("Both teams were efficient in the first half.")
        elif favorite_ts_1h >= 60.0 or underdog_ts_1h >= 58.0:
            scores["CONTROLLED_EFFICIENCY_ENVIRONMENT"] += 1.5

    if halftime_total_points >= 118 and halftime_total_points <= 126:
        scores["CONTROLLED_EFFICIENCY_ENVIRONMENT"] += 2.0
        notes.append("Halftime total sat in the efficient-but-not-chaotic range.")

    if second_half_needed_for_over is not None and 103 <= second_half_needed_for_over <= 108:
        scores["CONTROLLED_EFFICIENCY_ENVIRONMENT"] += 1.0

    # Reactive rebound environment
    if favorite_boxouts is not None and underdog_boxouts is not None:
        total_boxouts = favorite_boxouts + underdog_boxouts
        if total_boxouts <= 6:
            scores["REACTIVE_REBOUND_ENVIRONMENT"] += 3.0
            notes.append("Very low team box-out volume suggests reactive rebounding.")
        elif total_boxouts <= 10:
            scores["REACTIVE_REBOUND_ENVIRONMENT"] += 1.5

    if favorite_reb_final is not None and underdog_reb_final is not None:
        reb_margin = abs(favorite_reb_final - underdog_reb_final)
        if reb_margin <= 6:
            scores["REACTIVE_REBOUND_ENVIRONMENT"] += 1.5

    # Physical rebound dominance environment
    if favorite_reb_final is not None and underdog_reb_final is not None:
        reb_margin = abs(favorite_reb_final - underdog_reb_final)
        if reb_margin >= 12:
            scores["PHYSICAL_REBOUND_DOMINANCE_ENVIRONMENT"] += 3.0
            notes.append("Large rebound margin indicates one side controlled the glass physically.")

    if favorite_oreb_final is not None and underdog_oreb_final is not None:
        total_oreb = favorite_oreb_final + underdog_oreb_final
        if total_oreb >= 26:
            scores["PHYSICAL_REBOUND_DOMINANCE_ENVIRONMENT"] += 2.0
            notes.append("High offensive-rebound environment increased physicality pressure.")

    if favorite_boxouts is not None and underdog_boxouts is not None:
        if favorite_boxouts + underdog_boxouts >= 10:
            scores["PHYSICAL_REBOUND_DOMINANCE_ENVIRONMENT"] += 1.0

    # Spread inflation fade
    if live_spread is not None and live_spread >= 12.0:
        scores["SPREAD_INFLATION_FADE"] += 2.0
        notes.append("Large live spread raised inflation risk.")
        if halftime_margin <= 10:
            scores["SPREAD_INFLATION_FADE"] += 1.0
        if live_underdog_team_total is not None and live_underdog_team_total >= 102.0:
            scores["SPREAD_INFLATION_FADE"] += 2.0
            notes.append("Underdog still had enough scoring life to threaten a backdoor / non-cover.")

    # TT split edge
    if live_favorite_team_total is not None and live_underdog_team_total is not None:
        if live_favorite_team_total >= 120.0 and live_underdog_team_total >= 104.0:
            scores["TT_SPLIT_EDGE"] += 3.0
            notes.append("Favorite TT inflated while underdog TT remained live.")
        if halftime_margin >= 6 and underdog_halftime_points >= 55:
            scores["TT_SPLIT_EDGE"] += 1.5

    # Choose primary game type
    primary_game_type = max(scores, key=scores.get)

    betting_implications = {
        "full_game_total": "neutral",
        "favorite_team_total": "neutral",
        "underdog_team_total": "neutral",
        "spread": "neutral",
    }

    if primary_game_type == "COLLAPSE_UNDER_ENVIRONMENT":
        betting_implications.update(
            {
                "full_game_total": "prefer_under",
                "favorite_team_total": "prefer_under_if_inflated",
                "underdog_team_total": "avoid_over_without_real shot-quality recovery",
                "spread": "prefer_structural side over team-total bounceback",
            }
        )
    elif primary_game_type == "CONTROLLED_EFFICIENCY_ENVIRONMENT":
        betting_implications.update(
            {
                "full_game_total": "slight_under_if_market_overreacts",
                "favorite_team_total": "prefer_under_if first-half efficiency inflated it",
                "underdog_team_total": "consider_over_if underdog offense is still functional",
                "spread": "be cautious on large favorite numbers",
            }
        )
    elif primary_game_type == "REACTIVE_REBOUND_ENVIRONMENT":
        betting_implications.update(
            {
                "full_game_total": "do not assume rebounds force the under by themselves",
                "favorite_team_total": "neutral",
                "underdog_team_total": "neutral",
                "spread": "neutral",
            }
        )
    elif primary_game_type == "PHYSICAL_REBOUND_DOMINANCE_ENVIRONMENT":
        betting_implications.update(
            {
                "full_game_total": "lean_under_if one side also has shot-quality control",
                "favorite_team_total": "prefer_side or under over fake bounceback overs",
                "underdog_team_total": "fade weak-offense bounceback overs",
                "spread": "support structurally stronger rebounding side",
            }
        )
    elif primary_game_type == "SPREAD_INFLATION_FADE":
        betting_implications.update(
            {
                "full_game_total": "secondary",
                "favorite_team_total": "secondary",
                "underdog_team_total": "consider_over if offense still live",
                "spread": "fade inflated favorite spread",
            }
        )
    elif primary_game_type == "TT_SPLIT_EDGE":
        betting_implications.update(
            {
                "full_game_total": "secondary to team totals",
                "favorite_team_total": "prefer_under",
                "underdog_team_total": "prefer_over",
                "spread": "avoid oversized favorite spread",
            }
        )

    tags = [name for name, score in scores.items() if score >= 2.5]
    if not tags:
        tags = [primary_game_type]

    return GameTypeResult(
        primary_game_type=primary_game_type,
        tags=tags,
        scores={k: round(v, 2) for k, v in scores.items()},
        betting_implications=betting_implications,
        notes=notes,
    )


def build_orl_det_example() -> Dict[str, Any]:
    return detect_game_types(
        halftime_total_points=92,
        final_total_points=181,
        favorite_halftime_points=46,
        underdog_halftime_points=46,
        favorite_final_points=98,
        underdog_final_points=83,
        live_full_game_total=201.5,
        live_favorite_team_total=103.5,
        live_underdog_team_total=96.5,
        live_spread=4.5,
        favorite_off_rtg_1h=96.2,
        underdog_off_rtg_1h=90.5,
        favorite_ts_1h=59.9,
        underdog_ts_1h=44.0,
        favorite_tov_1h=8,
        underdog_tov_1h=2,
        favorite_oreb_final=17,
        underdog_oreb_final=13,
        favorite_reb_final=57,
        underdog_reb_final=42,
        favorite_boxouts=6.0,
        underdog_boxouts=7.0,
        favorite_fg_pct_final=45.9,
        underdog_fg_pct_final=32.5,
        favorite_3p_pct_final=23.1,
        underdog_3p_pct_final=25.0,
    ).to_dict()


def build_phx_okc_example() -> Dict[str, Any]:
    return detect_game_types(
        halftime_total_points=122,
        final_total_points=227,
        favorite_halftime_points=65,
        underdog_halftime_points=57,
        favorite_final_points=120,
        underdog_final_points=107,
        live_full_game_total=227.5,
        live_favorite_team_total=122.5,
        live_underdog_team_total=105.5,
        live_spread=15.5,
        favorite_off_rtg_1h=132.7,
        underdog_off_rtg_1h=116.3,
        favorite_ts_1h=62.7,
        underdog_ts_1h=62.3,
        favorite_tov_1h=4,
        underdog_tov_1h=11,
        favorite_oreb_final=12,
        underdog_oreb_final=15,
        favorite_reb_final=40,
        underdog_reb_final=44,
        favorite_boxouts=0.0,
        underdog_boxouts=5.0,
        favorite_fg_pct_final=47.3,
        underdog_fg_pct_final=45.9,
        favorite_3p_pct_final=35.0,
        underdog_3p_pct_final=35.5,
    ).to_dict()


if __name__ == "__main__":
    print("ORL/DET Example")
    print(build_orl_det_example())
    print()
    print("PHX/OKC Example")
    print(build_phx_okc_example())
