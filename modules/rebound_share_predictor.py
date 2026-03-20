from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


@dataclass
class ReboundShareInputs:
    projected_minutes: float
    player_reb_chances: float
    player_chance_conversion: float
    contested_rebounds: float
    avg_rebound_distance: float
    team_rebounds_projection: float
    team_big_minutes: float
    competing_big_minutes: float
    bench_big_minutes: float = 0.0
    usage_drag: float = 0.0


@dataclass
class ReboundShareResult:
    predicted_rebounds: float
    predicted_share: float
    role_tier: str
    fragility_score: float
    recommended_tier: str
    notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ReboundSharePredictor:
    """SharpEdge Rebound Share Predictor v1.0"""

    @classmethod
    def predict(cls, inputs: ReboundShareInputs) -> ReboundShareResult:
        notes: List[str] = []

        minutes_factor = clamp(inputs.projected_minutes / 34.0, 0.35, 1.20)
        chance_volume = inputs.player_reb_chances * minutes_factor
        conversion = clamp(inputs.player_chance_conversion / 100.0, 0.35, 0.95)
        contested_factor = clamp(inputs.contested_rebounds / max(inputs.projected_minutes, 1.0) * 6.0, 0.70, 1.18)
        distance_penalty = clamp(1.08 - max(0.0, inputs.avg_rebound_distance - 6.0) * 0.045, 0.78, 1.08)

        team_big_load = max(inputs.team_big_minutes, 1.0)
        competition_ratio = clamp(inputs.competing_big_minutes / team_big_load, 0.0, 1.4)
        competition_penalty = clamp(1.06 - competition_ratio * 0.18, 0.72, 1.08)
        bench_chaos_penalty = clamp(1.02 - (inputs.bench_big_minutes / 30.0) * 0.10, 0.84, 1.02)
        usage_penalty = clamp(1.0 - inputs.usage_drag * 0.08, 0.88, 1.0)

        predicted_rebounds = chance_volume * conversion * contested_factor * distance_penalty * competition_penalty * bench_chaos_penalty * usage_penalty
        predicted_share = clamp(predicted_rebounds / max(inputs.team_rebounds_projection, 1.0), 0.03, 0.45)

        fragility_score = 0.0
        if competition_ratio >= 0.95:
            fragility_score += 0.25
            notes.append("Heavy frontcourt competition reduces stable rebound share.")
        if inputs.bench_big_minutes >= 18:
            fragility_score += 0.20
            notes.append("Bench-big minutes create rebound-share redistribution risk.")
        if inputs.avg_rebound_distance >= 8.0:
            fragility_score += 0.15
            notes.append("Long rebound profile increases variance.")
        if inputs.projected_minutes <= 28:
            fragility_score += 0.20
            notes.append("Minutes base is below anchor threshold.")
        if conversion <= 0.52:
            fragility_score += 0.10
            notes.append("Rebound chance conversion is only average.")

        fragility_score = round(clamp(fragility_score, 0.0, 1.0), 3)

        if predicted_share >= 0.24 and fragility_score <= 0.25:
            role_tier = "anchor"
            recommended_tier = "core"
            notes.append("Projected as central rebound anchor.")
        elif predicted_share >= 0.17 and fragility_score <= 0.50:
            role_tier = "secondary"
            recommended_tier = "conditional"
            notes.append("Projected as secondary rebounder; environment matters.")
        else:
            role_tier = "fragile"
            recommended_tier = "fade_or_single_only"
            notes.append("Rebound role is fragile or too distributed for card-core use.")

        return ReboundShareResult(
            predicted_rebounds=round(predicted_rebounds, 2),
            predicted_share=round(predicted_share, 3),
            role_tier=role_tier,
            fragility_score=fragility_score,
            recommended_tier=recommended_tier,
            notes=notes,
        )


def evaluate_rebound_share(payload: Dict[str, Any]) -> Dict[str, Any]:
    inputs = ReboundShareInputs(
        projected_minutes=float(payload.get("projected_minutes", 0.0)),
        player_reb_chances=float(payload.get("player_reb_chances", 0.0)),
        player_chance_conversion=float(payload.get("player_chance_conversion", 0.0)),
        contested_rebounds=float(payload.get("contested_rebounds", 0.0)),
        avg_rebound_distance=float(payload.get("avg_rebound_distance", 0.0)),
        team_rebounds_projection=float(payload.get("team_rebounds_projection", 0.0)),
        team_big_minutes=float(payload.get("team_big_minutes", 0.0)),
        competing_big_minutes=float(payload.get("competing_big_minutes", 0.0)),
        bench_big_minutes=float(payload.get("bench_big_minutes", 0.0)),
        usage_drag=float(payload.get("usage_drag", 0.0)),
    )
    return ReboundSharePredictor.predict(inputs).to_dict()


if __name__ == "__main__":
    sample = {
        "projected_minutes": 32,
        "player_reb_chances": 18.8,
        "player_chance_conversion": 54.9,
        "contested_rebounds": 5.3,
        "avg_rebound_distance": 4.8,
        "team_rebounds_projection": 46,
        "team_big_minutes": 48,
        "competing_big_minutes": 16,
        "bench_big_minutes": 10,
        "usage_drag": 0.2,
    }
    print(evaluate_rebound_share(sample))
