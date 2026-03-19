from __future__ import annotations

from typing import Any, Dict, List, Optional

from modules.rebound_workflow_bridge_guarded import (
    run_liveflow_rebound_workflow_guarded,
)
from modules.rebound_workflow_bridge import run_pregame_rebound_workflow
from modules.oreb_chaos_detector import (
    adjust_player_for_oreb_chaos,
    detect_oreb_chaos_pregame,
)


def run_pregame_rebound_workflow_chaos_guarded(
    player: Dict[str, Any],
    team_players: List[Dict[str, Any]],
    base_projection: Dict[str, float],
    line: float,
    direction: str = "over",
    environment: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    pregame = run_pregame_rebound_workflow(
        player=player,
        team_players=team_players,
        base_projection=base_projection,
        line=line,
        direction=direction,
    )

    env = environment or {}
    chaos = detect_oreb_chaos_pregame(env)

    adjusted = adjust_player_for_oreb_chaos(
        player=player,
        projection={
            "mean": pregame["mean"],
            "median": pregame["median"],
            "win_prob": pregame.get("actionable_prob", pregame.get("base_prob", 0.5)),
            "tags": list(pregame.get("overlays", [])),
        },
        chaos_result=chaos,
    )

    pregame["mean"] = adjusted["mean"]
    pregame["median"] = adjusted["median"]
    pregame["actionable_prob"] = adjusted["win_prob"]
    pregame["edge"] = round(
        (float(line) - adjusted["mean"]) if direction.lower() == "under" else (adjusted["mean"] - float(line)),
        2,
    )
    pregame["oreb_chaos_active"] = adjusted.get("oreb_chaos_active", False)
    pregame["oreb_chaos_tag"] = adjusted.get("oreb_chaos_tag", chaos.get("tag", "OREB_CHAOS_LOW"))
    pregame["oreb_chaos_score"] = adjusted.get("oreb_chaos_score", chaos.get("score", 0.0))
    pregame["oreb_chaos_reason"] = chaos.get("reason", "")
    pregame["overlays"] = adjusted.get("tags", pregame.get("overlays", []))

    if chaos.get("active") and direction.lower() == "over":
        position = str(player.get("position", "")).upper()
        if position in {"PG", "SG", "SF", "G", "F", "G-F", "F-G"}:
            pregame["recommendation"] = "NO_PLAY_OREB_CHAOS_FADE"
        elif pregame["actionable_prob"] >= 0.60:
            pregame["recommendation"] = "OREB_CHAOS_BIG_BOOST"

    return pregame


def run_full_rebound_workflow_chaos_guarded(
    player_name: str,
    player_pregame: Dict[str, Any],
    team_players_pregame: List[Dict[str, Any]],
    base_projection: Dict[str, float],
    pregame_line: float,
    direction: str = "over",
    pregame_environment: Optional[Dict[str, Any]] = None,
    player_live: Optional[Dict[str, Any]] = None,
    team_players_live: Optional[List[Dict[str, Any]]] = None,
    live_state: Optional[Dict[str, Any]] = None,
    live_line: Optional[float] = None,
    expected_minutes: Optional[float] = None,
) -> Dict[str, Any]:
    pregame = run_pregame_rebound_workflow_chaos_guarded(
        player=player_pregame,
        team_players=team_players_pregame,
        base_projection=base_projection,
        line=pregame_line,
        direction=direction,
        environment=pregame_environment,
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
