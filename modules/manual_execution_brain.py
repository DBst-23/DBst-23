from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from modules.master_decision_engine import MasterDecisionEngine
from modules.live_execution_bot_v2 import LiveExecutionBotV2


class ManualExecutionBrain:
    """SharpEdge manual execution brain.

    Runs the full decision stack, creates a review ticket,
    and supports simulated execution only after explicit human approval.
    """

    @staticmethod
    def _utc_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    @classmethod
    def evaluate_pick(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        result = MasterDecisionEngine.evaluate(payload)
        result["manual_execution_brain"] = {
            "evaluated_at": cls._utc_iso(),
            "manual_approval_required": True,
            "simulated_only": True,
        }
        return result

    @classmethod
    def build_review_ticket(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        result = cls.evaluate_pick(payload)
        master = result.get("master_decision", {})
        sizing = result.get("sizing", {})
        autograde = result.get("autograde", {})
        ownership = result.get("ownership_model", {})
        safety = result.get("safety_filters", {})

        return {
            "created_at": cls._utc_iso(),
            "status": "READY_FOR_MANUAL_REVIEW" if master.get("ready_for_execution") else master.get("final_action", "FADE"),
            "player": payload.get("player"),
            "market": payload.get("market"),
            "side": payload.get("side"),
            "line": payload.get("line"),
            "confidence_score": autograde.get("confidence_score", result.get("confidence_score", 0)),
            "decision_score": master.get("final_decision_score", 0),
            "grade": autograde.get("grade", master.get("execution_tier", "C")),
            "recommended_units": sizing.get("recommended_units", result.get("recommended_units", 0.0)),
            "recommendation": sizing.get("recommendation", master.get("final_action", "FADE")),
            "ownership_tier": ownership.get("ownership_tier"),
            "projected_share": ownership.get("projected_share"),
            "blocked": bool(result.get("blocked") or autograde.get("block_before_execution")),
            "block_reason": autograde.get("block_reason", "") if autograde.get("block_before_execution") else "; ".join(safety.get("reasons", [])),
            "manual_approval_required": True,
            "result": result,
        }

    @classmethod
    def simulate_after_manual_approval(cls, payload: Dict[str, Any], human_approved: bool = False) -> Dict[str, Any]:
        ticket = cls.build_review_ticket(payload)

        if ticket.get("blocked"):
            return {
                "status": "REJECTED",
                "reason": ticket.get("block_reason") or "Blocked by SharpEdge decision stack",
                "ticket": ticket,
            }

        if not human_approved:
            return {
                "status": "PENDING_MANUAL_REVIEW",
                "reason": "Manual approval required before simulated execution.",
                "ticket": ticket,
            }

        sim_packet = {
            **payload,
            "confidence_score": ticket.get("confidence_score", 0),
            "recommended_units": ticket.get("recommended_units", 0.0),
            "blocked": False,
        }
        sim_result = LiveExecutionBotV2.execute(sim_packet)
        return {
            "status": sim_result.get("status", "UNKNOWN"),
            "simulated": True,
            "ticket": ticket,
            "simulation_result": sim_result,
        }


def review_ready_pick(result: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "READY_FOR_MANUAL_REVIEW",
        "message": "Use the review ticket for human review and manual placement.",
        "result": result,
    }


def log_rejected_pick(result: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "REJECTED_LOGGED",
        "logged_at": datetime.now(timezone.utc).isoformat(),
        "result": result,
    }


if __name__ == "__main__":
    payload = {
        "player": "Evan Mobley",
        "market": "Rebounds",
        "side": "Higher",
        "line": 10.5,
        "open_line": 9.5,
        "current_line": 10.5,
        "public_pct": 43,
        "current_stat": 0,
        "live_minutes": 1,
        "projected_minutes": 34,
        "projected_team_rebounds": 44,
        "team_rebounds_projection": 44,
        "win_prob": 0.61,
        "edge": 1.3,
        "stability_score": 0.83,
        "fragility_score": 0.18,
        "blowout_probability": 0.22,
        "oreb_sizing_multiplier": 1.12,
        "oreb_suppression_flag": False,
        "player_reb_chances": 18.8,
        "player_chance_conversion": 54.9,
        "contested_rebounds": 5.3,
        "competing_big_minutes": 16,
        "bench_big_minutes": 10,
        "avg_rebound_distance": 4.8,
        "current_role_share": 0.224,
        "base_unit": 1.0,
        "max_units": 2.5,
        "confidence_score": 74,
    }

    result = ManualExecutionBrain.evaluate_pick(payload)
    if result["master_decision"]["ready_for_execution"]:
        print(review_ready_pick(result))
    else:
        print(log_rejected_pick(result))
