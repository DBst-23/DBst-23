from __future__ import annotations

from typing import Any, Dict, List, Optional

from modules.rebound_workflow_bridge import run_pregame_rebound_workflow
from modules.liveflow_rebound_guard import (
    build_liveflow_card_guarded,
    project_live_rebounds_guarded,
)


def run_liveflow_rebound_workflow_guarded(
    player_name: str,
    player_live: Dict[str, Any],
    team_players_live: List[Dict[str, Any]],
    pregame_mean: float,
    pregame_median: float,
    line_live: float,
    expected_minutes: float,
    live_state: Dict[str, Any],
) -> Dict[str, Any]:
    result = project_live_rebounds_guarded(
        player_name=player_name,
        player_live=player_live,
        team_players_live=team_players_live,
        pregame_mean=float(pregame_mean),
        pregame_median=float(pregame_median),
        line_live=float(line_live),
        expected_minutes=float(expected_minutes),
        live_state=live_state,
    )
    return build_liveflow_card_guarded(player_name=player_name, result=result, line=float(line_live))


def run_full_rebound_workflow_guarded(
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
        output["live"] = run_liveflow_rebound_workflow_guarded(
            player_name=player_name,
            player_live=player_live,
            team_players_live=team_players_live,
            pregame_mean=pregame["mean"],
            pregame_median=pregame["median"],
            line_live=live_line,
            expected_minutes=expected_minutes,
            live_state=live_state,
        )

    return output
