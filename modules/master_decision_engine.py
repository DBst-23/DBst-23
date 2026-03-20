from __future__ import annotations

from typing import Any, Dict

from modules.sharpedge_unified_gate import build_unified_pick_packet
from modules.line_movement_engine import detect_line_movement
from modules.rebound_pace_tracker import track_rebound_pace


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


class MasterDecisionEngine:
    """SharpEdge Master Decision Engine v1.0

    Combines:
    - ownership-integrated unified gate
    - safety filters
    - grading and sizing
    - line movement reaction
    - live rebound pace tracking
    - final decision score and readiness state
    """

    @staticmethod
    def evaluate(payload: Dict[str, Any]) -> Dict[str, Any]:
        packet = build_unified_pick_packet(payload)

        line_move = detect_line_movement(
            {
                "open_line": float(payload.get("open_line", payload.get("line", 0.0))),
                "current_line": float(payload.get("current_line", payload.get("line", 0.0))),
                "public_pct": float(payload.get("public_pct", 50.0)),
            }
        )
        packet["line_movement"] = line_move

        pace = track_rebound_pace(
            {
                "current_rebounds": float(payload.get("current_stat", 0.0)),
                "minutes_played": float(payload.get("live_minutes", 1.0)),
                "projected_minutes": float(payload.get("projected_minutes", 36.0)),
            }
        )
        packet["pace_tracker"] = pace

        base_score = float(packet.get("autograde", {}).get("confidence_score", packet.get("confidence_score", 0)))
        decision_score = base_score
        reasons = []

        if line_move.get("sharp_signal"):
            decision_score += 6
            reasons.append("Sharp line movement bonus applied.")
        if line_move.get("public_trap"):
            decision_score -= 8
            reasons.append("Public trap penalty applied.")

        pace_flag = pace.get("pace_flag", "NORMAL")
        side = str(payload.get("side", "Higher")).lower()
        role_tier = str(packet.get("role_tier", "conditional")).lower()

        if side == "higher" and pace_flag == "HIGH" and role_tier == "anchor":
            decision_score += 5
            reasons.append("High live rebound pace supports anchor over.")
        elif side == "higher" and pace_flag == "LOW":
            decision_score -= 7
            reasons.append("Low rebound pace penalizes over.")
        elif side == "lower" and pace_flag == "LOW":
            decision_score += 4
            reasons.append("Low rebound pace supports under.")

        if packet.get("blocked") or packet.get("approval_status") == "BLOCKED":
            decision_score = min(decision_score, 49)
            reasons.append("Unified gate blocked execution readiness.")

        decision_score = int(round(clamp(decision_score, 0, 100)))

        if decision_score >= 85:
            final_action = "EXECUTE"
            execution_tier = "S"
        elif decision_score >= 72:
            final_action = "EXECUTE"
            execution_tier = "A"
        elif decision_score >= 58:
            final_action = "REVIEW"
            execution_tier = "B"
        else:
            final_action = "FADE"
            execution_tier = "C"

        if packet.get("blocked"):
            final_action = "FADE"

        packet["master_decision"] = {
            "final_decision_score": decision_score,
            "final_action": final_action,
            "execution_tier": execution_tier,
            "reasons": reasons,
            "ready_for_execution": final_action == "EXECUTE" and not packet.get("blocked"),
        }
        return packet


if __name__ == "__main__":
    sample = {
        "market": "Rebounds",
        "side": "Higher",
        "line": 10.5,
        "open_line": 9.5,
        "current_line": 10.5,
        "public_pct": 43,
        "current_stat": 5,
        "live_minutes": 18,
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
    print(MasterDecisionEngine.evaluate(sample))
