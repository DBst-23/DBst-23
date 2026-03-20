from __future__ import annotations

from typing import Any, Dict

from modules.rebound_ownership_model import evaluate_rebound_ownership
from modules.liveflow_safety_filters_v2 import evaluate_liveflow_safety_filters_v2
from modules.pick_autograder import evaluate_pick_grade
from modules.confidence_curve_sizing import evaluate_confidence_sizing


def build_unified_pick_packet(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    SharpEdge unified gate:
    1. Compute rebound ownership
    2. Inject ownership into safety filters
    3. Apply safety penalties to confidence
    4. Run grader
    5. Run sizing
    Returns a single execution-ready packet.
    """

    packet = dict(payload)

    ownership = evaluate_rebound_ownership(packet)
    packet["ownership_model"] = ownership

    # Ownership drives role + share going forward
    packet["predicted_share"] = ownership.get("projected_share", packet.get("predicted_share", 0.0))
    packet["role_tier"] = (
        "anchor"
        if ownership.get("anchor_flag")
        else ("secondary" if ownership.get("ownership_tier") == "SECONDARY" else "fragile")
    )

    safety = evaluate_liveflow_safety_filters_v2(packet)
    packet["safety_filters"] = safety

    base_confidence = int(packet.get("confidence_score", 70))
    adjusted_confidence = max(0, base_confidence - int(safety.get("confidence_penalty", 0)))
    packet["confidence_score"] = adjusted_confidence
    packet["blocked"] = bool(safety.get("block_pick", False))

    grade_payload = {
        **packet,
        "predicted_share": packet.get("predicted_share", 0.0),
        "role_tier": packet.get("role_tier", "conditional"),
        "oreb_kill_switch_flag": packet.get("oreb_kill_switch_flag", False) or safety.get("block_pick", False),
    }
    autograde = evaluate_pick_grade(grade_payload)
    packet["autograde"] = autograde

    sizing = evaluate_confidence_sizing(
        {
            "confidence_score": autograde.get("confidence_score", adjusted_confidence),
            "base_unit": float(packet.get("base_unit", 1.0)),
            "max_units": float(packet.get("max_units", 2.5)),
        }
    )
    packet["sizing"] = sizing
    packet["recommended_units"] = sizing.get("recommended_units", 0.0)

    packet["approval_status"] = "BLOCKED" if packet.get("blocked") or autograde.get("block_before_execution") else "READY"
    return packet


if __name__ == "__main__":
    sample = {
        "market": "Rebounds",
        "side": "Higher",
        "current_stat": 6,
        "line": 7.5,
        "projected_team_rebounds": 31,
        "team_rebounds_projection": 31,
        "projected_minutes": 26,
        "live_minutes": 18,
        "game_phase": "halftime",
        "live_margin": -19,
        "win_prob": 0.47,
        "edge": -0.2,
        "stability_score": 0.58,
        "fragility_score": 0.61,
        "blowout_probability": 0.64,
        "oreb_sizing_multiplier": 0.75,
        "oreb_suppression_flag": True,
        "player_reb_chances": 8.2,
        "player_chance_conversion": 53.1,
        "contested_rebounds": 0.7,
        "competing_big_minutes": 42,
        "bench_big_minutes": 18,
        "avg_rebound_distance": 7.6,
        "current_role_share": 0.16,
        "base_unit": 1.0,
        "max_units": 2.5,
        "confidence_score": 74,
    }
    print(build_unified_pick_packet(sample))
