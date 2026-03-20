from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


@dataclass
class ReboundOwnershipResult:
    ownership_score: float
    ownership_tier: str
    projected_share: float
    anchor_flag: bool
    lineup_competition_index: float
    notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ReboundOwnershipModel:
    """SharpEdge true rebound ownership model based on lineup role, tracking, and competition."""

    @classmethod
    def evaluate(cls, payload: Dict[str, Any]) -> ReboundOwnershipResult:
        notes: List[str] = []

        player_reb_chances = float(payload.get("player_reb_chances", 0.0))
        chance_conversion = float(payload.get("player_chance_conversion", 0.0)) / 100.0
        contested_rebounds = float(payload.get("contested_rebounds", 0.0))
        projected_minutes = float(payload.get("projected_minutes", 0.0))
        team_rebounds_projection = float(payload.get("team_rebounds_projection", 0.0))
        competing_big_minutes = float(payload.get("competing_big_minutes", 0.0))
        bench_big_minutes = float(payload.get("bench_big_minutes", 0.0))
        avg_rebound_distance = float(payload.get("avg_rebound_distance", 7.0))
        current_role_share = float(payload.get("current_role_share", 0.0))

        minutes_factor = clamp(projected_minutes / 32.0, 0.45, 1.20)
        chance_factor = clamp(player_reb_chances / 10.0, 0.30, 2.20)
        conversion_factor = clamp(chance_conversion, 0.40, 0.90)
        contested_factor = clamp((contested_rebounds / max(projected_minutes, 1.0)) * 6.5, 0.70, 1.20)
        distance_factor = clamp(1.08 - max(0.0, avg_rebound_distance - 5.5) * 0.05, 0.72, 1.08)

        competition_index = clamp((competing_big_minutes + bench_big_minutes) / max(projected_minutes + 1.0, 1.0), 0.20, 2.50)
        competition_penalty = clamp(1.18 - competition_index * 0.22, 0.55, 1.12)

        projected_rebounds = player_reb_chances * conversion_factor * minutes_factor * contested_factor * distance_factor * competition_penalty
        projected_share = clamp(projected_rebounds / max(team_rebounds_projection, 1.0), 0.03, 0.42)

        if current_role_share > 0:
            projected_share = round((projected_share * 0.70) + (current_role_share * 0.30), 3)
        else:
            projected_share = round(projected_share, 3)

        ownership_score = clamp((projected_share / 0.28) * 100.0, 5.0, 100.0)

        if projected_share >= 0.23 and competition_index <= 1.15:
            ownership_tier = "PRIMARY"
            anchor_flag = True
            notes.append("Player controls a primary share of the rebound ecosystem.")
        elif projected_share >= 0.17:
            ownership_tier = "SECONDARY"
            anchor_flag = False
            notes.append("Player has secondary rebound ownership and needs environment support.")
        else:
            ownership_tier = "FRAGILE"
            anchor_flag = False
            notes.append("Player lacks stable rebound ownership for over exposure.")

        if competition_index >= 1.45:
            notes.append("Heavy lineup competition is suppressing rebound ownership.")
        if avg_rebound_distance >= 8.0:
            notes.append("Long rebound profile adds variance to ownership stability.")
        if projected_minutes < 28:
            notes.append("Minutes base is below stable-anchor threshold.")

        return ReboundOwnershipResult(
            ownership_score=round(ownership_score, 1),
            ownership_tier=ownership_tier,
            projected_share=projected_share,
            anchor_flag=anchor_flag,
            lineup_competition_index=round(competition_index, 3),
            notes=notes,
        )


def evaluate_rebound_ownership(payload: Dict[str, Any]) -> Dict[str, Any]:
    return ReboundOwnershipModel.evaluate(payload).to_dict()


if __name__ == "__main__":
    sample = {
        "player_reb_chances": 18.8,
        "player_chance_conversion": 54.9,
        "contested_rebounds": 5.3,
        "projected_minutes": 30.5,
        "team_rebounds_projection": 46,
        "competing_big_minutes": 18,
        "bench_big_minutes": 10,
        "avg_rebound_distance": 4.8,
        "current_role_share": 0.224,
    }
    print(evaluate_rebound_ownership(sample))
