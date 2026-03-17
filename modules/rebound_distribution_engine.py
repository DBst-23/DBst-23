from __future__ import annotations

from typing import List, Dict, Any


# ================================
# REBOUND COMPETITION INDEX (RCI)
# ================================

def compute_rebound_competition_index(team_players: List[Dict[str, Any]]) -> float:
    """
    Calculates how concentrated or fragmented rebounds are across a team.

    Lower RCI → concentrated (good for overs)
    Higher RCI → fragmented (bad for overs)
    """

    active_players = [
        p for p in team_players
        if p.get("expected_minutes", 0) >= 18
    ]

    if not active_players:
        return 0.5

    weighted_rebounders = []

    for p in active_players:
        rebound_rate = float(p.get("rebound_rate", 0))
        expected_minutes = float(p.get("expected_minutes", 0))

        weight = rebound_rate * (expected_minutes / 36.0)
        weighted_rebounders.append(weight)

    total_rebound_share = sum(weighted_rebounders)

    if total_rebound_share <= 0:
        return 0.5

    concentration_score = max(weighted_rebounders) / total_rebound_share

    rci = 1 - concentration_score
    return round(rci, 3)


# ================================
# REBOUND DISTRIBUTION CLASSIFIER
# ================================

def classify_rebound_environment(rci: float) -> str:
    """
    Classifies rebound environment based on RCI.
    """

    if rci <= 0.35:
        return "CONCENTRATED"
    elif rci <= 0.60:
        return "BALANCED"
    else:
        return "FRAGMENTED"


# ================================
# USAGE × MINUTES BOOST (PREGAME)
# ================================

def compute_usage_minutes_boost(player: Dict[str, Any]) -> float:
    """
    Calculates player involvement to adjust rebound projections.
    """

    minutes = float(player.get("minutes", 0))
    usage_rate = float(player.get("usage_rate", 0)) / 100.0
    assist_rate = float(player.get("assist_rate", 0)) / 100.0

    involvement_score = (0.6 * usage_rate) + (0.4 * assist_rate)
    minutes_weight = minutes / 36.0

    boost = involvement_score * minutes_weight
    return round(boost, 3)


# ================================
# PROJECTION ADJUSTMENT ENGINE
# ================================

def adjust_rebound_projection(
    player: Dict[str, Any],
    team_players: List[Dict[str, Any]],
    projection: Dict[str, float],
) -> Dict[str, float]:
    """
    Adjusts rebound projection using:
    - RCI (team competition)
    - Usage × Minutes boost (player role)
    """

    rci = compute_rebound_competition_index(team_players)
    boost = compute_usage_minutes_boost(player)

    adjusted = projection.copy()

    # Apply RCI penalty
    if rci > 0.60:
        adjusted["mean"] *= 0.92
        adjusted["median"] -= 0.5
        adjusted["prob"] -= 0.06

    elif rci < 0.35:
        adjusted["mean"] *= 1.05
        adjusted["median"] += 0.5
        adjusted["prob"] += 0.04

    # Apply usage boost
    if boost > 0.30:
        adjusted["mean"] *= 1.08
        adjusted["median"] += 0.7
        adjusted["prob"] += 0.07

    elif boost > 0.18:
        adjusted["mean"] *= 1.03
        adjusted["median"] += 0.3
        adjusted["prob"] += 0.03

    # Conflict resolver (fragmentation + high usage)
    if rci > 0.60 and boost > 0.30:
        adjusted["mean"] *= 1.02
        adjusted["prob"] += 0.02

    return {
        "mean": round(adjusted["mean"], 2),
        "median": round(adjusted["median"], 1),
        "prob": round(adjusted["prob"], 3),
        "rci": rci,
        "boost": boost,
        "environment": classify_rebound_environment(rci),
    }


# ================================
# UNDER SUPPRESSION FILTER
# ================================

def should_block_under(player: Dict[str, Any], boost: float) -> bool:
    """
    Prevents bad UNDER bets on high-involvement players.
    """

    minutes = float(player.get("minutes", 0))

    if minutes >= 28 and boost > 0.28:
        return True

    return False


# ================================
# ELITE OVER TAG
# ================================

def is_elite_rebound_spot(rci: float, boost: float) -> bool:
    """
    Identifies elite rebound opportunities.
    """

    if boost > 0.30 and rci < 0.55:
        return True

    return False