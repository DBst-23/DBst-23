from __future__ import annotations

from typing import Any, Dict, List


def compute_live_rci(team_players_live: List[Dict[str, Any]]) -> float:
    """
    Live Rebound Competition Index (RCI)

    Lower RCI:
        More concentrated rebound share
    Higher RCI:
        More fragmented rebound share
    """
    active = [
        p for p in team_players_live
        if p.get("live_minutes", 0) >= 6 or p.get("expected_minutes", 0) >= 18
    ]

    if not active:
        return 0.5

    weighted: List[float] = []
    for p in active:
        live_minutes = max(float(p.get("live_minutes", 0)), 1.0)
        live_rebounds = float(p.get("live_rebounds", 0))
        expected_minutes = max(float(p.get("expected_minutes", 0)), 1.0)
        rebound_rate = float(p.get("rebound_rate", 0))

        live_rate = live_rebounds / live_minutes
        blended_rate = (0.55 * live_rate) + (0.45 * rebound_rate)

        weighted.append(blended_rate * (expected_minutes / 36.0))

    total = sum(weighted)
    if total <= 0:
        return 0.5

    concentration = max(weighted) / total
    return round(1.0 - concentration, 3)


def compute_live_usage_minutes_boost(player_live: Dict[str, Any]) -> float:
    """
    Usage × Minutes rebound boost

    Captures multi-stat players whose involvement increases rebound floor.
    """
    live_minutes = float(player_live.get("player_live_minutes", 0))
    live_points = float(player_live.get("player_live_points", 0))
    live_assists = float(player_live.get("player_live_assists", 0))

    minutes_weight = min(live_minutes / 36.0, 1.0)
    points_signal = min(live_points / 20.0, 1.0)
    assist_signal = min(live_assists / 8.0, 1.0)

    involvement = (0.60 * points_signal) + (0.40 * assist_signal)
    boost = involvement * minutes_weight

    return round(boost, 3)


def compute_live_rebound_pace_factor(live_state: Dict[str, Any]) -> float:
    """
    Estimates whether the current game environment is generating
    above- or below-baseline rebound volume.
    """
    team_rebounds_for = float(live_state.get("team_rebounds_for", 0))
    team_rebounds_against = float(live_state.get("team_rebounds_against", 0))
    time_remaining_sec = float(live_state.get("time_remaining_sec", 0))

    total_rebounds = team_rebounds_for + team_rebounds_against
    total_minutes_elapsed = 48.0 - (time_remaining_sec / 60.0)

    if total_minutes_elapsed <= 0:
        return 1.0

    rebounds_per_min = total_rebounds / total_minutes_elapsed

    baseline = 1.85
    factor = rebounds_per_min / baseline

    return round(max(0.88, min(1.15, factor)), 3)


def compute_live_risk_penalty(
    player_live: Dict[str, Any],
    live_state: Dict[str, Any],
) -> float:
    """
    Penalizes projection for foul trouble and blowout risk.
    """
    penalty = 1.0

    fouls = int(player_live.get("player_live_fouls", 0))
    quarter = int(live_state.get("quarter", 1))
    spread_live = abs(float(live_state.get("spread_live", 0)))

    if quarter <= 2 and fouls >= 3:
        penalty *= 0.88
    elif quarter == 3 and fouls >= 4:
        penalty *= 0.82

    if spread_live >= 18:
        penalty *= 0.90
    elif spread_live >= 12:
        penalty *= 0.95

    return round(penalty, 3)


def project_live_rebounds(
    player_live: Dict[str, Any],
    team_players_live: List[Dict[str, Any]],
    pregame_mean: float,
    pregame_median: float,
    line_live: float,
    expected_minutes: float,
    live_state: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Main live rebound projection engine.
    """
    live_minutes = float(player_live.get("player_live_minutes", 0))
    live_rebounds = float(player_live.get("player_live_rebounds", 0))

    minutes_remaining = max(float(expected_minutes) - live_minutes, 0.0)

    base_rate = float(pregame_mean) / max(float(expected_minutes), 1.0)
    live_rate = live_rebounds / max(live_minutes, 1.0)

    blended_rate = (0.45 * base_rate) + (0.55 * live_rate)

    live_rci = compute_live_rci(team_players_live)
    usage_boost = compute_live_usage_minutes_boost(player_live)
    pace_factor = compute_live_rebound_pace_factor(live_state)
    risk_penalty = compute_live_risk_penalty(player_live, live_state)

    # RCI adjustment
    if live_rci > 0.60:
        blended_rate *= 0.92
    elif live_rci < 0.40:
        blended_rate *= 1.05

    # Usage × minutes adjustment
    if usage_boost > 0.30:
        blended_rate *= 1.08
    elif usage_boost > 0.18:
        blended_rate *= 1.03

    blended_rate *= pace_factor
    blended_rate *= risk_penalty

    expected_remaining = blended_rate * minutes_remaining
    live_mean = live_rebounds + expected_remaining
    live_median = round(live_mean - 0.4)

    edge = live_mean - float(line_live)

    if edge >= 2.0:
        win_prob = 0.74
    elif edge >= 1.0:
        win_prob = 0.64
    elif edge >= 0.5:
        win_prob = 0.58
    elif edge >= 0.0:
        win_prob = 0.53
    elif edge >= -0.5:
        win_prob = 0.47
    elif edge >= -1.0:
        win_prob = 0.40
    else:
        win_prob = 0.30

    return {
        "live_rci": round(live_rci, 3),
        "usage_boost": round(usage_boost, 3),
        "pace_factor": round(pace_factor, 3),
        "risk_penalty": round(risk_penalty, 3),
        "mean": round(live_mean, 2),
        "median": int(live_median),
        "win_prob": round(win_prob, 3),
        "edge": round(edge, 2),
        "pregame_mean": round(float(pregame_mean), 2),
        "pregame_median": round(float(pregame_median), 2),
        "line_live": round(float(line_live), 2),
        "minutes_remaining": round(minutes_remaining, 2),
    }


def classify_liveflow_pick(result: Dict[str, Any]) -> str:
    """
    Converts numeric output into a SharpEdge LIVE-FLOW decision tier.
    """
    win_prob = float(result.get("win_prob", 0.5))

    if win_prob >= 0.70:
        return "LIVE_LOCK"
    if win_prob >= 0.60:
        return "LIVE_STRONG"
    if win_prob >= 0.52:
        return "LIVE_THIN_EDGE"
    if win_prob >= 0.45:
        return "LIVE_NO_PLAY"
    return "LIVE_FADE"


def liveflow_card(player_name: str, result: Dict[str, Any], line: float) -> Dict[str, Any]:
    """
    Standardized SharpEdge LIVE-FLOW output format.
    """
    return {
        "player": player_name,
        "line": float(line),
        "mean": result.get("mean"),
        "median": result.get("median"),
        "win_prob": result.get("win_prob"),
        "edge": result.get("edge"),
        "live_rci": result.get("live_rci"),
        "usage_boost": result.get("usage_boost"),
        "pace_factor": result.get("pace_factor"),
        "risk_penalty": result.get("risk_penalty"),
        "tier": classify_liveflow_pick(result),
    }