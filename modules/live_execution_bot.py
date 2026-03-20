from typing import Dict, Any


class LiveExecutionBot:

    @staticmethod
    def execute(pick_packet: Dict[str, Any]):

        if pick_packet.get("blocked"):
            return {
                "status": "REJECTED",
                "reason": "Blocked by SharpEdge pre-execution gate"
            }

        confidence = pick_packet.get("confidence_score", 0)
        units = pick_packet.get("recommended_units", 0)

        return {
            "status": "EXECUTED",
            "confidence": confidence,
            "units": units,
            "message": "Bet executed via simulated sportsbook API"
        }


if __name__ == "__main__":
    print(LiveExecutionBot.execute({"confidence_score": 82, "recommended_units": 1.5, "blocked": False}))
