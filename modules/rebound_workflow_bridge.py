from __future__ import annotations

from typing import Any, Dict, List, Optional

from modules.rebound_distribution_engine import (
    adjust_rebound_projection,
    compute_usage_minutes_boost,
    is_elite_rebound_spot,
    should_block_under,
)

from modules.liveflow_rebound_engine import (
    classify_liveflow_pick,
    liveflow_card,
    project_live_rebounds,
)


def build_pregame_team_players(
    team_players: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []

    for p in team_players:
        normalized.append(
            {
                "name": p.get("name", ""),
                "expected_minutes": float(p.get("expected_minutes", 0)),
                "rebound_rate": float(p.get("rebound_rate", 0)),
            }
        )

    return normalized


def build_live_team_players(
    team_players_live: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []

    for p in team_players_live:
        normalized.append(
            {
                "name": p.get("name", ""),
                "live_minutes": float(p.get("live_minutes", 0)),
                "live_rebounds": float(p.get("live_rebounds", 0)),
                "expected_minutes": float(p.get("expected_minutes", 0)),
                "rebound_rate": float(p.get("rebound_rate", 0)),
            }
        )

    return normalized


def compute_oreb_spike_overlay(
    team_off_rebounds: float,
    baseline_off_rebounds: float = 10.0,
) -> Dict[str, Any]:
    """
    Detects offensive rebound spike environments.
    """
    if baseline_off_rebounds <= 0:
        baseline_off_rebounds = 10.0

    ratio = team_off_rebounds / baseline_off_rebounds

    if ratio >= 1.8:
        return {
            "active": True,
            "tag": "OREB_SPIKE",
            "mean_multiplier": 1.12,
            "prob_boost": 0.07,
        }
    elif ratio >= 1.4:
        return {
            "active": True,
            "tag": "OREB_ELEVATED",
            "mean_multiplier": 1.08,
            "prob_boost": 0.04,
        }

    return {
        "active": False,
        "tag": "OREB_NORMAL",
        "mean_multiplier": 1.00,
        "prob_boost": 0.00,
    }


def compute_role_expansion_overlay(
    player_name: str,
    player_position: str,
    offensive_rebounds: float,
    live_points: float,
    live_assists: float,
) -> Dict[str, Any]:
    """
    Flags guards/wings or multi-stat players whose rebound role expands in-game.
    """
    position = (player_position or "").upper()

    guard_wing_positions = {"PG", "SG", "SF", "G", "F", "GF", "WG"}

    if position in guard_wing_positions and offensive_rebounds >= 3:
        return {
            "active": True,
            "tag": "ROLE_EXPANSION_OREB",
            "mean_multiplier": 1.10,
            "prob_boost": 0.06,
        }

    if live_points >= 12 and live_assists >= 4:
        return {
            "active": True,
            "tag": "ROLE_EXPANSION_USAGE",
            "mean_multiplier": 1.06,
            "prob_boost": 0.04,
        }

    return {
        "active": False,
        "tag": "ROLE_NORMAL",
        "mean_multiplier": 1.00,
        "prob_boost": 0.00,
    }


def apply_rebound_volatility_overlays(
    mean: float,
    prob: float,
    oreb_overlay: Dict[str, Any],
    role_overlay: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Applies OREB spike and role expansion overlays to rebound outputs.
    """
    adjusted_mean = mean
    adjusted_prob = prob
    tags: List[str] = []

    if oreb_overlay.get("active"):
        adjusted_mean *= float(oreb_overlay["mean_multiplier"])
        adjusted_prob += float(oreb_overlay["prob_boost"])
        tags.append(str(oreb_overlay["tag"]))

    if role_overlay.get("active"):
        adjusted_mean *= float(role_overlay["mean_multiplier"])
        adjusted_prob += float(role_overlay["prob_boost"])
        tags.append(str(role_overlay["tag"]))

    adjusted_prob = max(0.01, min(0.99, adjusted_prob))

    return {
        "mean": round(adjusted_mean, 2),
        "prob": round(adjusted_prob, 3),
        "tags": tags,
    }


def run_pregame_rebound_workflow(
    player: Dict[str, Any],
    team_players: List[Dict[str, Any]],
    base_projection: Dict[str, float],
    line: float,
    direction: str = "over",
) -> Dict[str, Any]:
    direction = direction.lower().strip()
    if direction not in {"over", "under"}:
        raise ValueError("direction must be 'over' or 'under'")

    normalized_team = build_pregame_team_players(team_players)
    adjusted = adjust_rebound_projection(
        player=player,
        team_players=normalized_team,
        projection=base_projection,
    )

    boost = compute_usage_minutes_boost(player)
    block_under = should_block_under(player, boost)
    elite_tag = is_elite_rebound_spot(adjusted["rci"], adjusted["boost"])

    pregame_oreb_overlay = compute_oreb_spike_overlay(
        team_off_rebounds=float(player.get("team_off_rebounds_projection", 10.0)),
        baseline_off_rebounds=float(player.get("baseline_off_rebounds", 10.0)),
    )

    pregame_role_overlay = compute_role_expansion_overlay(
        player_name=str(player.get("name", "")),
        player_position=str(player.get("position", "")),
        offensive_rebounds=float(player.get("projected_offensive_rebounds", 0)),
        live_points=float(player.get("projected_points", 0)),
        live_assists=float(player.get("projected_assists", 0)),
    )

    if direction == "under":
        actionable_prob = round(1.0 - adjusted["prob"], 3)
    else:
        actionable_prob = adjusted["prob"]

    overlay_result = apply_rebound_volatility_overlays(
        mean=float(adjusted["mean"]),
        prob=float(actionable_prob),
        oreb_overlay=pregame_oreb_overlay,
        role_overlay=pregame_role_overlay,
    )

    adjusted["mean"] = overlay_result["mean"]
    actionable_prob = overlay_result["prob"]

    edge_vs_line = round(adjusted["mean"] - float(line), 2)

    if direction == "under":
        final_edge = round(float(line) - adjusted["mean"], 2)
    else:
        final_edge = edge_vs_line

    if direction == "under" and block_under:
        recommendation = "BLOCK_UNDER"
    elif actionable_prob >= 0.70:
        recommendation = "LOCK"
    elif actionable_prob >= 0.60:
        recommendation = "STRONG"
    elif actionable_prob >= 0.52:
        recommendation = "THIN_EDGE"
    else:
        recommendation = "NO_PLAY"

    return {
        "mode": "pregame",
        "player": player.get("name", ""),
        "direction": direction,
        "line": float(line),
        "mean": adjusted["mean"],
        "median": adjusted["median"],
        "base_prob": adjusted["prob"],
        "actionable_prob": actionable_prob,
        "edge": final_edge,
        "rci": adjusted["rci"],
        "boost": adjusted["boost"],
        "environment": adjusted["environment"],
        "block_under": block_under,
        "elite_rebound_spot": elite_tag,
        "recommendation": recommendation,
        "overlays": overlay_result["tags"],
        "oreb_overlay": pregame_oreb_overlay["tag"],
        "role_overlay": pregame_role_overlay["tag"],
    }


def run_liveflow_rebound_workflow(
    player_name: str,
    player_live: Dict[str, Any],
    team_players_live: List[Dict[str, Any]],
    pregame_mean: float,
    pregame_median: float,
    line_live: float,
    expected_minutes: float,
    live_state: Dict[str, Any],
) -> Dict[str, Any]:
    normalized_team = build_live_team_players(team_players_live)

    result = project_live_rebounds(
        player_live=player_live,
        team_players_live=normalized_team,
        pregame_mean=float(pregame_mean),
        pregame_median=float(pregame_median),
        line_live=float(line_live),
        expected_minutes=float(expected_minutes),
        live_state=live_state,
    )

    oreb_overlay = compute_oreb_spike_overlay(
        team_off_rebounds=float(live_state.get("team_off_rebounds", 0)),
        baseline_off_rebounds=float(live_state.get("baseline_off_rebounds", 10.0)),
    )

    role_overlay = compute_role_expansion_overlay(
        player_name=player_name,
        player_position=str(player_live.get("player_position", "")),
        offensive_rebounds=float(player_live.get("player_live_offensive_rebounds", 0)),
        live_points=float(player_live.get("player_live_points", 0)),
        live_assists=float(player_live.get("player_live_assists", 0)),
    )

    overlay_result = apply_rebound_volatility_overlays(
        mean=float(result["mean"]),
        prob=float(result["win_prob"]),
        oreb_overlay=oreb_overlay,
        role_overlay=role_overlay,
    )

    result["mean"] = overlay_result["mean"]
    result["win_prob"] = overlay_result["prob"]
    result["edge"] = round(result["mean"] - float(line_live), 2)

    card = liveflow_card(player_name=player_name, result=result, line=float(line_live))
    card["mode"] = "live"
    card["recommendation"] = classify_liveflow_pick(result)
    card["overlays"] = overlay_result["tags"]
    card["oreb_overlay"] = oreb_overlay["tag"]
    card["role_overlay"] = role_overlay["tag"]

    return card


def run_full_rebound_workflow(
    player_name: str,
    player_pregame: Dict[str, Any],
    team_players_pregame: List[Dict[str, Any]],
    base_projection: Dict[str, float],
    pregame_line: float,
    direction: str = "over",
    player_live: Optional[Dict[str, Any]] = None,
    team_players_live: Optional[List[Dict[str, Any]]] = None,
    live_state: Optional[Dict[str, Any]] = None,
    live_line: Optional[float] = None,
    expected_minutes: Optional[float] = None,
) -> Dict[str, Any]:
    pregame = run_pregame_rebound_workflow(
        player=player_pregame,
        team_players=team_players_pregame,
        base_projection=base_projection,
        line=pregame_line,
        direction=direction,
    )

    output: Dict[str, Any] = {
        "player": player_name,
        "pregame": pregame,
    }

    if (
        player_live is not None
        and team_players_live is not None
        and live_state is not None
        and live_line is not None
        and expected_minutes is not None
    ):
        live = run_liveflow_rebound_workflow(
            player_name=player_name,
            player_live=player_live,
            team_players_live=team_players_live,
            pregame_mean=pregame["mean"],
            pregame_median=pregame["median"],
            line_live=live_line,
            expected_minutes=expected_minutes,
            live_state=live_state,
        )
        output["live"] = live

    return output


if __name__ == "__main__":
    player_pregame = {
        "name": "Stephon Castle",
        "position": "SG",
        "minutes": 34,
        "usage_rate": 23.0,
        "assist_rate": 21.0,
        "team_off_rebounds_projection": 12.0,
        "baseline_off_rebounds": 10.0,
        "projected_offensive_rebounds": 1.2,
        "projected_points": 17.0,
        "projected_assists": 5.0,
    }

    team_players_pregame = [
        {"name": "Stephon Castle", "expected_minutes": 34, "rebound_rate": 0.18},
        {"name": "Victor Wembanyama", "expected_minutes": 34, "rebound_rate": 0.34},
        {"name": "Keldon Johnson", "expected_minutes": 24, "rebound_rate": 0.18},
        {"name": "Charles Bryant", "expected_minutes": 20, "rebound_rate": 0.19},
    ]

    base_projection = {
        "mean": 6.4,
        "median": 6.0,
        "prob": 0.56,
    }

    player_live = {
        "player_position": "SG",
        "player_live_minutes": 18,
        "player_live_rebounds": 4,
        "player_live_offensive_rebounds": 4,
        "player_live_points": 12,
        "player_live_assists": 5,
        "player_live_fouls": 2,
    }

    team_players_live = [
        {"name": "Stephon Castle", "live_minutes": 18, "live_rebounds": 4, "expected_minutes": 34, "rebound_rate": 0.18},
        {"name": "Victor Wembanyama", "live_minutes": 17, "live_rebounds": 8, "expected_minutes": 34, "rebound_rate": 0.34},
        {"name": "Keldon Johnson", "live_minutes": 13, "live_rebounds": 4, "expected_minutes": 24, "rebound_rate": 0.18},
        {"name": "Charles Bryant", "live_minutes": 11, "live_rebounds": 4, "expected_minutes": 20, "rebound_rate": 0.19},
    ]

    live_state = {
        "quarter": 2,
        "time_remaining_sec": 720,
        "team_rebounds_for": 26,
        "team_rebounds_against": 15,
        "team_off_rebounds": 12,
        "team_def_rebounds": 14,
        "spread_live": -14.5,
        "game_total_live": 231.5,
        "baseline_off_rebounds": 10.0,
    }

    result = run_full_rebound_workflow(
        player_name="Stephon Castle",
        player_pregame=player_pregame,
        team_players_pregame=team_players_pregame,
        base_projection=base_projection,
        pregame_line=6.5,
        direction="over",
        player_live=player_live,
        team_players_live=team_players_live,
        live_state=live_state,
        live_line=6.5,
        expected_minutes=34,
    )

    print(result)