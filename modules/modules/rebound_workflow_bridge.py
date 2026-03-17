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
    """
    Normalizes team player inputs for pregame RCI processing.

    Expected player keys:
    {
        "name": str,
        "expected_minutes": float,
        "rebound_rate": float
    }
    """
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
    """
    Normalizes live team rebound competitor inputs.

    Expected player keys:
    {
        "name": str,
        "live_minutes": float,
        "live_rebounds": float,
        "expected_minutes": float,
        "rebound_rate": float
    }
    """
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


def run_pregame_rebound_workflow(
    player: Dict[str, Any],
    team_players: List[Dict[str, Any]],
    base_projection: Dict[str, float],
    line: float,
    direction: str = "over",
) -> Dict[str, Any]:
    """
    Pregame bridge:
    - applies RCI logic
    - applies usage × minutes boost
    - blocks fragile unders
    - tags elite rebound spots

    player expected keys:
    {
        "name": str,
        "minutes": float,
        "usage_rate": float,
        "assist_rate": float
    }

    team_players expected keys:
    {
        "name": str,
        "expected_minutes": float,
        "rebound_rate": float
    }

    base_projection expected keys:
    {
        "mean": float,
        "median": float,
        "prob": float
    }
    """
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

    edge_vs_line = round(adjusted["mean"] - float(line), 2)

    if direction == "under":
        actionable_prob = round(1.0 - adjusted["prob"], 3)
    else:
        actionable_prob = adjusted["prob"]

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
        "edge": edge_vs_line if direction == "over" else round(float(line) - adjusted["mean"], 2),
        "rci": adjusted["rci"],
        "boost": adjusted["boost"],
        "environment": adjusted["environment"],
        "block_under": block_under,
        "elite_rebound_spot": elite_tag,
        "recommendation": recommendation,
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
    """
    Live bridge:
    - normalizes live player/team input
    - runs live rebound projection
    - returns SharpEdge liveflow card

    player_live expected keys:
    {
        "player_live_minutes": float,
        "player_live_rebounds": float,
        "player_live_points": float,
        "player_live_assists": float,
        "player_live_fouls": float
    }
    """
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

    card = liveflow_card(player_name=player_name, result=result, line=float(line_live))
    card["mode"] = "live"
    card["recommendation"] = classify_liveflow_pick(result)

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
    """
    Combined bridge:
    - returns pregame output
    - optionally returns live output if live inputs are provided
    """
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
    # Example pregame input
    player_pregame = {
        "name": "Josh Giddey",
        "minutes": 34,
        "usage_rate": 24.0,
        "assist_rate": 31.0,
    }

    team_players_pregame = [
        {"name": "Josh Giddey", "expected_minutes": 34, "rebound_rate": 0.31},
        {"name": "Matas Buzelis", "expected_minutes": 32, "rebound_rate": 0.22},
        {"name": "Jalen Smith", "expected_minutes": 28, "rebound_rate": 0.23},
        {"name": "Leonard Miller", "expected_minutes": 21, "rebound_rate": 0.21},
        {"name": "Tre Jones", "expected_minutes": 27, "rebound_rate": 0.11},
    ]

    base_projection = {
        "mean": 9.4,
        "median": 9.0,
        "prob": 0.61,
    }

    # Example live input
    player_live = {
        "player_live_minutes": 18,
        "player_live_rebounds": 7,
        "player_live_points": 8,
        "player_live_assists": 6,
        "player_live_fouls": 1,
    }

    team_players_live = [
        {"name": "Josh Giddey", "live_minutes": 18, "live_rebounds": 7, "expected_minutes": 34, "rebound_rate": 0.31},
        {"name": "Matas Buzelis", "live_minutes": 17, "live_rebounds": 4, "expected_minutes": 32, "rebound_rate": 0.22},
        {"name": "Jalen Smith", "live_minutes": 15, "live_rebounds": 3, "expected_minutes": 28, "rebound_rate": 0.23},
        {"name": "Leonard Miller", "live_minutes": 14, "live_rebounds": 4, "expected_minutes": 21, "rebound_rate": 0.21},
    ]

    live_state = {
        "quarter": 2,
        "time_remaining_sec": 360,
        "team_rebounds_for": 24,
        "team_rebounds_against": 18,
        "team_off_rebounds": 7,
        "team_def_rebounds": 17,
        "spread_live": -8.5,
        "game_total_live": 236.5,
    }

    result = run_full_rebound_workflow(
        player_name="Josh Giddey",
        player_pregame=player_pregame,
        team_players_pregame=team_players_pregame,
        base_projection=base_projection,
        pregame_line=8.5,
        direction="over",
        player_live=player_live,
        team_players_live=team_players_live,
        live_state=live_state,
        live_line=10.5,
        expected_minutes=34,
    )

    print(result)