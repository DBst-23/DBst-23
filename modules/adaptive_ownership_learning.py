from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


@dataclass
class OwnershipLearningResult:
    updated_weights: Dict[str, float]
    learning_rate: float
    ownership_delta: float
    miss_classification: str
    notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AdaptiveOwnershipLearning:
    """SharpEdge adaptive learning layer for rebound ownership model calibration."""

    DEFAULT_WEIGHTS = {
        "reb_chances": 0.34,
        "chance_conversion": 0.18,
        "contested_rebounds": 0.17,
        "minutes": 0.14,
        "competition_penalty": 0.10,
        "distance_penalty": 0.07,
    }

    @classmethod
    def update_from_postmortem(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        weights = dict(payload.get("current_weights") or cls.DEFAULT_WEIGHTS)
        projected = float(payload.get("projected_rebounds", 0.0))
        actual = float(payload.get("actual_rebounds", 0.0))
        role_tier = str(payload.get("role_tier", "secondary")).lower()
        competition_index = float(payload.get("lineup_competition_index", 1.0))
        team_rebounds = float(payload.get("team_rebounds_actual", 0.0))
        live_environment = str(payload.get("environment_type", "neutral")).lower()

        error = actual - projected
        abs_error = abs(error)
        learning_rate = clamp(0.03 + abs_error * 0.01, 0.03, 0.12)
        notes: List[str] = []

        if abs_error <= 0.75:
            miss_classification = "ON_TARGET"
            notes.append("Projection was close enough; only light weight maintenance applied.")
        elif error > 0:
            miss_classification = "UNDERPROJECTED"
            notes.append("Actual rebounds beat projection; increase ownership weight on strongest drivers.")
        else:
            miss_classification = "OVERPROJECTED"
            notes.append("Projection overshot actual result; reduce fragile ownership assumptions.")

        # reb chances + contested get stronger when we underproject real anchor outcomes
        if error > 0:
            weights["reb_chances"] += learning_rate * 0.40
            weights["contested_rebounds"] += learning_rate * 0.25
            weights["minutes"] += learning_rate * 0.15
            if role_tier == "anchor":
                weights["competition_penalty"] -= learning_rate * 0.20
                notes.append("Anchor role outperformed; competition penalty softened.")
        else:
            weights["chance_conversion"] -= learning_rate * 0.20
            weights["minutes"] -= learning_rate * 0.10
            weights["competition_penalty"] += learning_rate * 0.35
            weights["distance_penalty"] += learning_rate * 0.15
            notes.append("Miss suggests rebound share was more fragile than projected.")

        if competition_index >= 1.35:
            weights["competition_penalty"] += learning_rate * 0.20
            notes.append("Heavy lineup competition reinforced in ownership weights.")

        if team_rebounds and team_rebounds < 36:
            weights["minutes"] -= learning_rate * 0.08
            weights["chance_conversion"] -= learning_rate * 0.05
            notes.append("Low team rebound environment reduces confidence in non-anchor overs.")

        if live_environment == "opponent_dominant":
            weights["competition_penalty"] += learning_rate * 0.18
            notes.append("Opponent-dominant rebound environment logged into future ownership assumptions.")

        # normalize to 1.0 while keeping all weights positive
        for key, value in list(weights.items()):
            weights[key] = max(0.01, value)
        total = sum(weights.values())
        normalized = {k: round(v / total, 4) for k, v in weights.items()}

        return OwnershipLearningResult(
            updated_weights=normalized,
            learning_rate=round(learning_rate, 3),
            ownership_delta=round(error, 2),
            miss_classification=miss_classification,
            notes=notes,
        ).to_dict()


if __name__ == "__main__":
    sample = {
        "projected_rebounds": 8.4,
        "actual_rebounds": 6,
        "role_tier": "secondary",
        "lineup_competition_index": 1.42,
        "team_rebounds_actual": 35,
        "environment_type": "opponent_dominant",
    }
    print(AdaptiveOwnershipLearning.update_from_postmortem(sample))
