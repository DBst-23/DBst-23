from dataclasses import dataclass


@dataclass
class EdgeStrengthProfile:
    player: str
    stat: str
    line: float
    mean_projection: float
    median_projection: float
    win_probability: float
    market_support_score: float      # 0.0 to 1.0
    minutes_stability_score: float   # 0.0 to 1.0
    role_clarity_score: float        # 0.0 to 1.0
    volatility_penalty: float        # 0.0 to 1.0
    ceiling_penalty: float           # 0.0 to 1.0


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def score_edge(profile: EdgeStrengthProfile) -> dict:
    mean_gap = abs(profile.mean_projection - profile.line)
    median_gap = abs(profile.median_projection - profile.line)

    mean_component = clamp(mean_gap / 2.0, 0.0, 1.0) * 20
    median_component = clamp(median_gap / 2.0, 0.0, 1.0) * 15
    win_prob_component = clamp((profile.win_probability - 0.50) / 0.20, 0.0, 1.0) * 25
    market_component = clamp(profile.market_support_score, 0.0, 1.0) * 10
    minutes_component = clamp(profile.minutes_stability_score, 0.0, 1.0) * 10
    role_component = clamp(profile.role_clarity_score, 0.0, 1.0) * 15

    volatility_deduction = clamp(profile.volatility_penalty, 0.0, 1.0) * 10
    ceiling_deduction = clamp(profile.ceiling_penalty, 0.0, 1.0) * 15

    raw_score = (
        mean_component
        + median_component
        + win_prob_component
        + market_component
        + minutes_component
        + role_component
        - volatility_deduction
        - ceiling_deduction
    )

    final_score = round(clamp(raw_score, 0.0, 100.0), 1)

    if final_score >= 85:
        tier = "TIER_1_CORE"
    elif final_score >= 70:
        tier = "TIER_2_PLAYABLE"
    elif final_score >= 55:
        tier = "TIER_3_THIN"
    else:
        tier = "PASS"

    return {
        "player": profile.player,
        "stat": profile.stat,
        "line": profile.line,
        "score": final_score,
        "tier": tier,
        "mean_gap": round(mean_gap, 3),
        "median_gap": round(median_gap, 3),
        "win_probability": profile.win_probability,
    }
