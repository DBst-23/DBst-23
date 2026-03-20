from typing import Dict, Any

from modules.liveflow_safety_filters import evaluate_liveflow_safety_filters


class LiveExecutionBotV2:

    @staticmethod
    def execute(pick_packet: Dict[str, Any]):

        # 🔐 STEP 1: Run safety filters BEFORE anything
        safety = evaluate_liveflow_safety_filters(pick_packet)

        # Attach safety output
        pick_packet.update(safety)

        # 🚫 HARD BLOCK (NEW SYSTEM)
        if safety.get("block_pick"):
            return {
                "status": "REJECTED",
                "reason": "Blocked by LiveFlow Safety Filters",
                "safety": safety
            }

        # Existing block flag
        if pick_packet.get("blocked"):
            return {
                "status": "REJECTED",
                "reason": "Blocked by legacy SharpEdge gate"
            }

        confidence = pick_packet.get("confidence_score", 0)
        units = pick_packet.get("recommended_units", 0)

        return {
            "status": "EXECUTED",
            "confidence": confidence,
            "units": units,
            "message": "Executed after passing LiveFlow safety filters",
            "safety_passed": True
        }


if __name__ == "__main__":
    sample = {
        "market": "Rebounds",
        "side": "Higher",
        "role_tier": "secondary",
        "current_stat": 6,
        "line": 7.5,
        "projected_team_rebounds": 31,
        "predicted_share": 0.16,
        "stability_score": 0.58,
        "win_prob": 0.47,
        "live_minutes": 18,
        "game_phase": "halftime",
        "confidence_score": 82,
        "recommended_units": 1.5
    }

    print(LiveExecutionBotV2.execute(sample))
