from __future__ import annotations

from typing import Any, Dict, List

from modules.liveflow_rebound_engine import (
    classify_liveflow_pick,
    liveflow_card,
    project_live_rebounds,
)
from modules.rebound_kill_switch import (
    apply_kill_switch_to_live_result,
    compute_rebound_kill_switch,
    should_block_live_rebound_entry,
)


def project_live_rebounds_guarded(
    player_name: str,
    player_live: Dict[str, Any],
    team_players_live: List[Dict[str, Any]],
    pregame_mean: float,
    pregame_median: float,
    line_live: float,
    expected_minutes: float,
    live_state: Dict[str, Any],
) -> Dict[str, Any]:
    base_result = project_live_rebounds(
        player_live=player_live,
        team_players_live=team_players_live,
        pregame_mean=pregame_mean,
        pregame_median=pregame_median,
        line_live=line_live,
        expected_minutes=expected_minutes,
        live_state=live_state,
    )

    guard_state = compute_rebound_kill_switch(
        player_name=player_name,
        team_players_live=team_players_live,
        live_state=live_state,
    )

    adjusted_result = apply_kill_switch_to_live_result(base_result, guard_state)
    decision = should_block_live_rebound_entry(adjusted_result, guard_state)

    adjusted_result["guard_state"] = guard_state
    adjusted_result["decision"] = decision
    return adjusted_result


def build_liveflow_card_guarded(
    player_name: str,
    result: Dict[str, Any],
    line: float,
) -> Dict[str, Any]:
    card = liveflow_card(player_name=player_name, result=result, line=line)
    card["tier"] = classify_liveflow_pick(result)
    card["guard_active"] = bool(result.get("guard_state", {}).get("active", False))
    card["guard_tag"] = result.get("guard_state", {}).get("tag", "REBOUND_EDGE_ZONE_OPEN")
    card["guard_reason"] = result.get("guard_state", {}).get("reason", "Guard conditions not met")
    card["guard_conditions"] = result.get("guard_state", {}).get("conditions", {})
    card["decision"] = result.get("decision", {})

    if card["guard_active"]:
        card["tier"] = "NO_PLAY_GUARDED"

    return card
