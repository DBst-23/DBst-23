from __future__ import annotations

from typing import Any, Dict, List, Optional

from modules.rebound_kill_switch import (
    apply_kill_switch_to_live_result,
    compute_rebound_kill_switch,
    should_block_live_rebound_entry,
)
from modules.oreb_chaos_detector import detect_oreb_chaos_pregame


FRAGILE_POSITIONS = {"PG", "SG", "SF", "G", "F", "G-F", "F-G"}
BIG_POSITIONS = {"C", "PF", "F-C", "C-F"}


def compute_chaos_kill_switch(
    player_name: str,
    player_position: str,
    team_players_live: List[Dict[str, Any]],
    live_state: Dict[str, Any],
    pregame_environment: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Merge the LIVE-FLOW dead-zone kill switch with pregame OREB chaos context.

    Rules:
    1. Base kill-switch remains active for balanced/high-efficiency distributed pools.
    2. Pregame OREB chaos can hard-block fragile wing/guard rebound overs.
    3. Pregame OREB chaos can soften kill-switch pressure on elite interior anchors.
    """
    base_guard = compute_rebound_kill_switch(
        player_name=player_name,
        team_players_live=team_players_live,
        live_state=live_state,
    )

    chaos_environment = pregame_environment or {}
    chaos = detect_oreb_chaos_pregame(chaos_environment)
    position = str(player_position or "").upper()

    merged = dict(base_guard)
    merged["chaos_active"] = chaos.get("active", False)
    merged["chaos_tag"] = chaos.get("tag", "OREB_CHAOS_LOW")
    merged["chaos_score"] = chaos.get("score", 0.0)
    merged["chaos_reason"] = chaos.get("reason", "")

    if chaos.get("active") and position in FRAGILE_POSITIONS:
        merged["active"] = True
        merged["tag"] = "NO_PLAY_OREB_CHAOS_FADE"
        merged["reason"] = "Pregame OREB chaos active on fragile rebound profile"
        merged["prob_multiplier"] = min(float(merged.get("prob_multiplier", 1.0)), 0.86)
        merged["mean_multiplier"] = min(float(merged.get("mean_multiplier", 1.0)), 0.95)
        merged["chaos_override"] = "FRAGILE_PROFILE_BLOCK"
        return merged

    if chaos.get("active") and position in BIG_POSITIONS:
        merged["chaos_override"] = "ANCHOR_BIG_PROTECTED"
        if not base_guard.get("active"):
            merged["prob_multiplier"] = max(float(merged.get("prob_multiplier", 1.0)), 1.00)
            merged["mean_multiplier"] = max(float(merged.get("mean_multiplier", 1.0)), 1.00)
        else:
            merged["prob_multiplier"] = max(float(merged.get("prob_multiplier", 1.0)), 0.94)
            merged["mean_multiplier"] = max(float(merged.get("mean_multiplier", 1.0)), 0.98)
        return merged

    merged["chaos_override"] = "NONE"
    return merged



def apply_chaos_kill_switch_to_live_result(
    result: Dict[str, Any],
    chaos_guard: Dict[str, Any],
) -> Dict[str, Any]:
    adjusted = apply_kill_switch_to_live_result(result=result, kill_switch=chaos_guard)
    adjusted["chaos_active"] = chaos_guard.get("chaos_active", False)
    adjusted["chaos_tag"] = chaos_guard.get("chaos_tag", "OREB_CHAOS_LOW")
    adjusted["chaos_score"] = chaos_guard.get("chaos_score", 0.0)
    adjusted["chaos_reason"] = chaos_guard.get("chaos_reason", "")
    adjusted["chaos_override"] = chaos_guard.get("chaos_override", "NONE")
    return adjusted



def should_block_live_rebound_entry_chaos_aware(
    result: Dict[str, Any],
    chaos_guard: Dict[str, Any],
    min_prob_threshold: float = 0.54,
) -> Dict[str, Any]:
    decision = should_block_live_rebound_entry(
        result=result,
        kill_switch=chaos_guard,
        min_prob_threshold=min_prob_threshold,
    )

    if chaos_guard.get("chaos_override") == "FRAGILE_PROFILE_BLOCK":
        return {
            "block": True,
            "recommendation": "NO_PLAY_OREB_CHAOS_FADE",
            "tag": chaos_guard.get("tag", "NO_PLAY_OREB_CHAOS_FADE"),
            "reason": chaos_guard.get("reason", "Pregame chaos fade active"),
        }

    if chaos_guard.get("chaos_override") == "ANCHOR_BIG_PROTECTED" and not chaos_guard.get("active"):
        decision["chaos_note"] = "OREB chaos active but anchor big profile preserved"

    return decision
