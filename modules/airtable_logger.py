from __future__ import annotations

import requests
from datetime import datetime, timezone
from typing import Any, Dict


class AirtableLogger:
    """Logs SharpEdge review tickets and outcomes to Airtable via REST API."""

    @staticmethod
    def _headers(api_key: str) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _utc_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    @classmethod
    def build_airtable_record(cls, ticket: Dict[str, Any]) -> Dict[str, Any]:
        result = ticket.get("result", {})
        master = result.get("master_decision", {})
        autograde = result.get("autograde", {})
        sizing = result.get("sizing", {})
        ownership = result.get("ownership_model", {})
        safety = result.get("safety_filters", {})

        return {
            "fields": {
                "created_at": ticket.get("created_at", cls._utc_iso()),
                "player": ticket.get("player"),
                "market": ticket.get("market"),
                "side": ticket.get("side"),
                "line": ticket.get("line"),
                "status": ticket.get("status"),
                "blocked": ticket.get("blocked", False),
                "block_reason": ticket.get("block_reason", ""),
                "confidence_score": ticket.get("confidence_score", 0),
                "decision_score": ticket.get("decision_score", 0),
                "grade": ticket.get("grade", "C"),
                "recommended_units": ticket.get("recommended_units", 0.0),
                "recommendation": ticket.get("recommendation", "FADE"),
                "ownership_tier": ticket.get("ownership_tier", ownership.get("ownership_tier")),
                "projected_share": ticket.get("projected_share", ownership.get("projected_share", 0.0)),
                "approval_status": result.get("approval_status", ticket.get("status")),
                "final_action": master.get("final_action", "FADE"),
                "execution_tier": master.get("execution_tier", ticket.get("grade", "C")),
                "safety_reasons": "; ".join(safety.get("reasons", [])),
                "confidence_penalty": safety.get("confidence_penalty", 0),
                "autograde_notes": "; ".join(autograde.get("notes", [])),
                "sizing_recommendation": sizing.get("recommendation", ticket.get("recommendation", "FADE")),
            }
        }

    @classmethod
    def log_record(cls, api_key: str, base_id: str, table_name: str, ticket: Dict[str, Any]) -> Dict[str, Any]:
        url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
        payload = cls.build_airtable_record(ticket)
        try:
            response = requests.post(url, headers=cls._headers(api_key), json=payload, timeout=15)
            return {
                "status": "success" if response.ok else "failed",
                "status_code": response.status_code,
                "response": response.json(),
            }
        except Exception as exc:
            return {"status": "failed", "error": str(exc)}


if __name__ == "__main__":
    sample_ticket = {
        "created_at": AirtableLogger._utc_iso(),
        "player": "Evan Mobley",
        "market": "Rebounds",
        "side": "Higher",
        "line": 10.5,
        "status": "READY_FOR_MANUAL_REVIEW",
        "blocked": False,
        "confidence_score": 84,
        "decision_score": 88,
        "grade": "A",
        "recommended_units": 1.35,
        "recommendation": "CORE_PLAY",
        "ownership_tier": "PRIMARY",
        "projected_share": 0.241,
        "result": {
            "approval_status": "READY",
            "master_decision": {"final_action": "EXECUTE", "execution_tier": "A"},
            "safety_filters": {"reasons": [], "confidence_penalty": 0},
            "autograde": {"notes": ["Pick cleared pre-execution gate."]},
            "sizing": {"recommendation": "CORE_PLAY"},
        },
    }
    print(AirtableLogger.build_airtable_record(sample_ticket))
