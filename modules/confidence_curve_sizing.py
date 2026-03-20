from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


@dataclass
class ConfidenceSizingResult:
    confidence_score: int
    grade: str
    unit_multiplier: float
    recommended_units: float
    recommendation: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ConfidenceCurveSizer:
    """Maps SharpEdge confidence score to unit sizing."""

    @staticmethod
    def size_from_confidence(confidence_score: int, base_unit: float = 1.0, max_units: float = 2.5) -> ConfidenceSizingResult:
        score = int(clamp(confidence_score, 0, 100))

        if score >= 90:
            grade = "S"
            multiplier = 2.0
            recommendation = "FULL_SEND"
        elif score >= 85:
            grade = "S"
            multiplier = 1.75
            recommendation = "PRESS_EDGE"
        elif score >= 72:
            grade = "A"
            multiplier = 1.35
            recommendation = "CORE_PLAY"
        elif score >= 58:
            grade = "B"
            multiplier = 0.85
            recommendation = "CONDITIONAL_PLAY"
        else:
            grade = "C"
            multiplier = 0.0
            recommendation = "NO_BET"

        recommended_units = round(min(base_unit * multiplier, max_units), 2)

        return ConfidenceSizingResult(
            confidence_score=score,
            grade=grade,
            unit_multiplier=round(multiplier, 2),
            recommended_units=recommended_units,
            recommendation=recommendation,
        )


def evaluate_confidence_sizing(payload: Dict[str, Any]) -> Dict[str, Any]:
    return ConfidenceCurveSizer.size_from_confidence(
        confidence_score=int(payload.get("confidence_score", 0)),
        base_unit=float(payload.get("base_unit", 1.0)),
        max_units=float(payload.get("max_units", 2.5)),
    ).to_dict()


if __name__ == "__main__":
    print(evaluate_confidence_sizing({"confidence_score": 86, "base_unit": 1.0, "max_units": 2.5}))
