from __future__ import annotations

from typing import Any, Dict, List


def count_secondary_rebounders(
    team_players_live: List[Dict[str, Any]],
    primary_player_name: str,
    threshold: float = 2.0,
) -> int:
    count = 0
    for player in team_players_live:
        if str(player.get("name", "")) == primary_player_name:
            continue
        if float(player.get("live_rebounds", 0.0)) >= threshold:
            count += 1
    return count


def compute_rebound_kill_switch(
    player_name: str,
    team_players_live: List[Dict[str, Any]],
    live_state: Dict[str, Any],
) -> Dict[str, Any]:
    fg_pct_for = float(live_state.get("fg_pct_for", 0.0))
    fg_pct_against = float(live_state.get("fg_pct_against", 0.0))
    team_rebounds_for = float(live_state.get("team_rebounds_for", 0.0))
    team_rebounds_against = float(live_state.get("team_rebounds_against", 0.0))

    rebound_gap = abs(team_rebounds_for - team_rebounds_against)

    secondary_for = int(
        live_state.get(
            "secondary_rebounders_for",
            count_secondary_rebounders(team_players_live, player_name),
        )
    )
    secondary_against = int(live_state.get("secondary_rebounders_against", 0))

    conditions = {
        "both_teams_above_50_fg": fg_pct_for >= 0.50 and fg_pct_against >= 0.50,
        "balanced_rebound_pool": rebound_gap <= 5,
        "secondary_rebounders_live": secondary_for >= 3 and secondary_against >= 3,
    }

    active = all(conditions.values())

    return {
        "active": active,
        "tag": "NO_REBOUND_EDGE_ZONE" if active else "REBOUND_EDGE_ZONE_OPEN",
        "reason": "Balanced rebounds + high efficiency + distributed board share" if active else "Kill-switch conditions not met",
        "conditions": conditions,
        "fg_pct_for": round(fg_pct_for, 3),
        "fg_pct_against": round(fg_pct_against, 3),
        "rebound_gap": round(rebound_gap, 2),
        "secondary_rebounders_for": secondary_for,
        "secondary_rebounders_against": secondary_against,
        "prob_multiplier": 0.90 if active else 1.00,
        "mean_multiplier": 0.97 if active else 1.00,
    }


def apply_kill_switch_to_live_result(result: Dict[str, Any], kill_switch: Dict[str, Any]) -> Dict[str, Any]:
    adjusted = dict(result)

    if not kill_switch.get("active"):
        adjusted["kill_switch_active"] = False
        adjusted["kill_switch_tag"] = kill_switch.get("tag", "REBOUND_EDGE_ZONE_OPEN")
        adjusted["kill_switch_reason"] = kill_switch.get("reason", "Kill-switch conditions not met")
        return adjusted

    adjusted["mean"] = round(
        float(adjusted.get("mean", 0.0)) * float(kill_switch.get("mean_multiplier", 1.0)),
        2,
    )
    adjusted["win_prob"] = round(
        max(0.01, min(0.99, float(adjusted.get("win_prob", 0.0)) * float(kill_switch.get("prob_multiplier", 1.0)))),
        3,
    )
    adjusted["edge"] = round(float(adjusted["mean"]) - float(adjusted.get("line", 0.0)), 2)
    adjusted["kill_switch_active"] = True
    adjusted["kill_switch_tag"] = kill_switch["tag"]
    adjusted["kill_switch_reason"] = kill_switch["reason"]
    return adjusted


def should_block_live_rebound_entry(result: Dict[str, Any], kill_switch: Dict[str, Any], min_prob_threshold: float = 0.54) -> Dict[str, Any]:
    if kill_switch.get("active"):
        return {
            "block": True,
            "recommendation": "NO_PLAY_KILL_SWITCH",
            "tag": kill_switch.get("tag", "NO_REBOUND_EDGE_ZONE"),
            "reason": kill_switch.get("reason", "Kill-switch active"),
        }

    win_prob = float(result.get("win_prob", 0.0))
    if win_prob < min_prob_threshold:
        return {
            "block": True,
            "recommendation": "NO_PLAY_THIN_EDGE",
            "tag": "THIN_EDGE_BLOCK",
            "reason": f"Win probability below threshold ({win_prob:.3f} < {min_prob_threshold:.3f})",
        }

    return {
        "block": False,
        "recommendation": "PLAY_ALLOWED",
        "tag": "LIVE_REBOUND_EDGE_ACTIVE",
        "reason": "Kill-switch not active and probability threshold satisfied",
    }
