from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List
import uuid


@dataclass
class SportsbookOrder:
    sportsbook: str
    market: str
    player: str
    side: str
    line: float
    odds: int
    stake: float
    units: float
    confidence_score: int
    correlation_group: str = ""


class SportsbookAPISim:
    """SharpEdge sportsbook API simulator for PrizePicks / Underdog style workflows."""

    @staticmethod
    def _utc_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def validate_order(order: Dict[str, Any]) -> Dict[str, Any]:
        required = ["sportsbook", "market", "player", "side", "line", "stake", "units", "confidence_score"]
        missing = [k for k in required if k not in order]
        if missing:
            return {"valid": False, "reason": f"Missing required fields: {', '.join(missing)}"}
        if float(order.get("stake", 0.0)) <= 0:
            return {"valid": False, "reason": "Stake must be positive"}
        if int(order.get("confidence_score", 0)) < 58:
            return {"valid": False, "reason": "Confidence below SharpEdge execution threshold"}
        return {"valid": True, "reason": "Order validated"}

    @classmethod
    def submit_order(cls, order: Dict[str, Any]) -> Dict[str, Any]:
        validation = cls.validate_order(order)
        if not validation["valid"]:
            return {
                "status": "REJECTED",
                "reason": validation["reason"],
                "timestamp": cls._utc_iso(),
                "order": order,
            }

        order_id = f"SIM-{uuid.uuid4().hex[:10].upper()}"
        return {
            "status": "ACCEPTED",
            "timestamp": cls._utc_iso(),
            "order_id": order_id,
            "sportsbook": order["sportsbook"],
            "order": order,
            "message": f"Simulated order accepted by {order['sportsbook']} API",
        }

    @classmethod
    def batch_submit_orders(cls, orders: List[Dict[str, Any]]) -> Dict[str, Any]:
        results = [cls.submit_order(order) for order in orders]
        accepted = sum(1 for r in results if r["status"] == "ACCEPTED")
        rejected = len(results) - accepted
        return {
            "timestamp": cls._utc_iso(),
            "accepted": accepted,
            "rejected": rejected,
            "results": results,
        }


if __name__ == "__main__":
    sample = {
        "sportsbook": "Underdog",
        "market": "Rebounds",
        "player": "Evan Mobley",
        "side": "Higher",
        "line": 10.5,
        "odds": -110,
        "stake": 17.5,
        "units": 1.75,
        "confidence_score": 86,
    }
    print(SportsbookAPISim.submit_order(sample))
