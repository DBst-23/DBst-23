"""
High-Volatility Totals Guardrail Module (HV-TGM)

Goal:
- Detect high-variance game environments for NBA totals
- Adjust the projected total upward slightly when volatility is high
- Optionally cap UNDER recommendations in those environments
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class HVInputs:
    """
    Inputs describing the volatility context of a game.

    These can be fed from CTG data, league_summary, or
    manually for retro/backtest work.

    All values are designed to be *soft* – this module
    is a guardrail, not the primary model.
    """
    # Flags (True/False)
    high_shot_makers: bool = False          # multiple 3-level scorers, high ORtg guys
    high_transition_risk: bool = False      # both teams like to run, vulnerable in transition
    low_tov_environment: bool = False       # both teams project < 13% TOV%
    high_three_volume_matchup: bool = False # both sides launch a ton of 3s
    recent_extreme_overs: int = 0           # last N games with +20 vs closing total

    # Percentile tiers (0.0 – 1.0)
    pace_tier: float = 0.5                  # 0.5 = league average, >0.7 = fast environment
    halfcourt_offense_tier: float = 0.5     # how strong the combined halfcourt offense is
    halfcourt_defense_weak_tier: float = 0.5# how weak the combined halfcourt defense is


@dataclass
class HVResult:
    risk_score: float
    volatility_boost: float
    under_cap_active: bool


def compute_hv_guardrail(base_total: float, hv: Optional[HVInputs]) -> HVResult:
    """
    Compute a volatility risk score and a small upward adjustment
    to the projected total in high-variance environments.

    - base_total: model's raw projected total (before guardrail)
    - hv: HVInputs describing the matchup context

    Returns:
        HVResult with:
          - risk_score (0–~6 range)
          - volatility_boost (points added to total)
          - under_cap_active (True = do NOT take unders unless edge is very strong)
    """
    if hv is None:
        # No context provided -> no adjustment
        return HVResult(
            risk_score=0.0,
            volatility_boost=0.0,
            under_cap_active=False,
        )

    score = 0.0

    # 1) Flag-based contributions
    if hv.high_shot_makers:
        score += 1.2
    if hv.high_transition_risk:
        score += 1.0
    if hv.low_tov_environment:
        score += 0.8
    if hv.high_three_volume_matchup:
        score += 1.0

    # Recent crazy overs (+20 vs closing) matter a lot
    if hv.recent_extreme_overs >= 1:
        score += 0.7
    if hv.recent_extreme_overs >= 2:
        score += 0.5

    # 2) Percentile-based contributions
    # Pace – reward very fast games
    if hv.pace_tier > 0.70:
        score += 0.6
    if hv.pace_tier > 0.85:
        score += 0.4

    # Strong halfcourt offense AND weak halfcourt defense together are dangerous
    combined_halfcourt = 0.5 * (hv.halfcourt_offense_tier + hv.halfcourt_defense_weak_tier)
    if combined_halfcourt > 0.65:
        score += 0.6
    if combined_halfcourt > 0.80:
        score += 0.5

    # Clamp score to a reasonable range
    score = max(0.0, min(score, 6.0))

    # 3) Translate score into a volatility boost in points
    # Rough rule: each point of score ~ 1.5–2.0 pts on total, capped.
    boost = base_total * (0.015 * score)  # 1.5% of base_total per score unit
    max_boost = 8.0                       # never add more than 8 points from guardrail
    boost = max(0.0, min(boost, max_boost))

    # 4) Under-cap logic
    # If risk_score is high, we mark unders as "dangerous unless edge >= ~62%"
    under_cap = score >= 3.0

    return HVResult(
        risk_score=score,
        volatility_boost=boost,
        under_cap_active=under_cap,
    )


def hv_to_dict(result: HVResult) -> Dict[str, Any]:
    """
    Helper to convert HVResult into a plain dict
    for logging / JSON export.
    """
    return {
        "hv_risk_score": result.risk_score,
        "hv_volatility_boost": result.volatility_boost,
        "hv_under_cap_active": result.under_cap_active,
    }