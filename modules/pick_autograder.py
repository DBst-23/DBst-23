from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


@dataclass
class PickGradeResult:
    confidence_score: int
    grade: str
    block_before_execution: bool
    block_reason: str
    component_scores: Dict[str, float]
    notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PickAutoGrader:
    """SharpEdge auto-grades picks and blocks weak slips before execution."""

    @classmethod
    def grade_pick(cls, payload: Dict[str, Any]) -> PickGradeResult:
        notes: List[str] = []

        win_prob = float(payload.get("win_prob", 0.50))
        edge = float(payload.get("edge", 0.0))
        share = float(payload.get("predicted_share", 0.0))
        fragility = float(payload.get("fragility_score", 0.50))
        stability = float(payload.get("stability_score", 0.50))
        blowout_prob = float(payload.get("blowout_probability", 0.50))
        chaos_mult = float(payload.get("oreb_sizing_multiplier", 1.0))
        kill_flag = bool(payload.get("oreb_kill_switch_flag", False))
        suppression_flag = bool(payload.get("oreb_suppression_flag", False))
        role_tier = str(payload.get("role_tier", "conditional")).lower()
        side = str(payload.get("side", "Higher")).lower()

        win_prob_score = clamp((win_prob - 0.50) / 0.20, 0.0, 1.0) * 30.0
        edge_score = clamp(edge / 3.0, -1.0, 1.0) * 15.0
        share_score = clamp((share - 0.10) / 0.18, 0.0, 1.0) * 18.0
        stability_score_component = clamp(stability, 0.0, 1.0) * 15.0
        fragility_score_component = (1.0 - clamp(fragility, 0.0, 1.0)) * 10.0
        chaos_score = clamp((chaos_mult - 0.75) / 0.45, 0.0, 1.0) * 7.0
        blowout_penalty = clamp(blowout_prob, 0.0, 1.0) * 10.0

        raw_score = (
            win_prob_score
            + edge_score
            + share_score
            + stability_score_component
            + fragility_score_component
            + chaos_score
            - blowout_penalty
        )

        if role_tier == "anchor":
            raw_score += 5.0
            notes.append("Anchor rebound role bonus applied.")
        elif role_tier == "fragile":
            raw_score -= 8.0
            notes.append("Fragile rebound role penalty applied.")

        if side == "lower" and suppression_flag:
            raw_score += 4.0
            notes.append("Under supported by suppression environment.")
        elif side == "higher" and suppression_flag and role_tier != "anchor":
            raw_score -= 10.0
            notes.append("Over penalized by suppression environment.")

        if kill_flag and role_tier != "anchor":
            raw_score -= 25.0
            notes.append("Kill-switch penalty applied to non-anchor profile.")

        confidence_score = int(round(clamp(raw_score, 0.0, 100.0)))

        if confidence_score >= 85:
            grade = "S"
        elif confidence_score >= 72:
            grade = "A"
        elif confidence_score >= 58:
            grade = "B"
        else:
            grade = "C"

        block = False
        block_reason = ""

        if kill_flag and role_tier != "anchor":
            block = True
            block_reason = "OREB kill-switch active on non-anchor profile"
        elif stability < 0.50:
            block = True
            block_reason = "Minute stability below execution threshold"
        elif side == "higher" and suppression_flag and role_tier == "fragile":
            block = True
            block_reason = "Fragile over in suppression environment"
        elif confidence_score < 58:
            block = True
            block_reason = "Confidence score below SharpEdge minimum"

        components = {
            "win_prob_score": round(win_prob_score, 2),
            "edge_score": round(edge_score, 2),
            "share_score": round(share_score, 2),
            "stability_score": round(stability_score_component, 2),
            "fragility_score_component": round(fragility_score_component, 2),
            "chaos_score": round(chaos_score, 2),
            "blowout_penalty": round(blowout_penalty, 2),
        }

        if block:
            notes.append(f"Auto-blocked before execution: {block_reason}.")
        else:
            notes.append("Pick cleared pre-execution gate.")

        return PickGradeResult(
            confidence_score=confidence_score,
            grade=grade,
            block_before_execution=block,
            block_reason=block_reason,
            component_scores=components,
            notes=notes,
        )


def evaluate_pick_grade(payload: Dict[str, Any]) -> Dict[str, Any]:
    return PickAutoGrader.grade_pick(payload).to_dict()
