from __future__ import annotations

from typing import Any, Dict

from modules.oreb_chaos_detector import evaluate_oreb_chaos


def apply_oreb_chaos_to_liveflow(live_packet: Dict[str, Any]) -> Dict[str, Any]:
    """
    Integrates OREB chaos logic into LiveFlow decision packets.

    Expected keys in live_packet:
    - environment: dict with team/opponent rebound and second-chance metrics
    - pick_profile: dict with market, player, side, base_unit, confidence, tags
    """
    environment = dict(live_packet.get("environment", {}) or {})
    pick_profile = dict(live_packet.get("pick_profile", {}) or {})

    chaos = evaluate_oreb_chaos(environment)
    base_unit = float(pick_profile.get("base_unit", 1.0))
    side = str(pick_profile.get("side", "Higher")).lower()
    player_tier = str(pick_profile.get("player_tier", "conditional")).lower()
    market = str(pick_profile.get("market", "Rebounds"))

    action = "ALLOW"
    adjusted_unit = base_unit * float(chaos.get("sizing_multiplier", 1.0))
    notes = list(chaos.get("notes", []))
    tags = list(pick_profile.get("tags", []))
    tags.append(f"OREB_CHAOS_{chaos.get('chaos_level', 'LOW')}")
    tags.append(f"OREB_TYPE_{str(chaos.get('chaos_type', 'neutral')).upper()}")

    if market.lower() == "rebounds" and side == "higher":
        if chaos.get("kill_switch_flag") and player_tier != "anchor":
            action = "BLOCK"
            adjusted_unit = 0.0
            notes.append("LiveFlow block: non-anchor rebound over in kill-switch environment.")
            tags.append("OREB_KILL_SWITCH_BLOCK")
        elif chaos.get("suppression_flag") and player_tier != "anchor":
            action = "DOWNGRADE"
            adjusted_unit = min(adjusted_unit, base_unit * 0.75)
            notes.append("LiveFlow downgrade: opponent rebound control suppresses conditional over.")
            tags.append("OREB_SUPPRESSION_DOWNGRADE")
        elif chaos.get("boost_flag") and player_tier == "anchor":
            action = "BOOST"
            adjusted_unit = max(adjusted_unit, base_unit * 1.10)
            notes.append("LiveFlow boost: anchor rebound over in favorable OREB chaos environment.")
            tags.append("OREB_ANCHOR_BOOST")
    elif market.lower() == "rebounds" and side == "lower":
        if chaos.get("suppression_flag"):
            action = "BOOST_UNDER"
            adjusted_unit = max(adjusted_unit, base_unit * 1.05)
            notes.append("LiveFlow under boost: opponent-dominant rebound ecosystem supports under.")
            tags.append("OREB_UNDER_BOOST")

    output = dict(live_packet)
    output["oreb_chaos"] = chaos
    output["pick_profile"] = {
        **pick_profile,
        "adjusted_unit": round(adjusted_unit, 2),
        "liveflow_action": action,
        "tags": tags,
    }
    output["notes"] = notes
    return output


if __name__ == "__main__":
    sample = {
        "environment": {
            "team_oreb": 8,
            "opp_oreb": 12,
            "team_rebounds": 35,
            "opp_rebounds": 47,
            "team_second_chance_points": 6,
            "opp_second_chance_points": 19,
        },
        "pick_profile": {
            "player": "Bobby Portis",
            "market": "Rebounds",
            "side": "Higher",
            "base_unit": 1.0,
            "player_tier": "conditional",
            "tags": ["LIVEFLOW"],
        },
    }
    print(apply_oreb_chaos_to_liveflow(sample))
