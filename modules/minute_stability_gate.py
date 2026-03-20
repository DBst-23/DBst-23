from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class MinuteStabilityResult:
    stability_score: float
    stability_level: str
    risk_flag: bool
    minutes_projection: float
    recommendation: str

class MinuteStabilityGate:

    @staticmethod
    def evaluate(projected_minutes, foul_risk, rotation_volatility):

        base = projected_minutes / 36.0
        foul_penalty = 1 - foul_risk * 0.3
        rotation_penalty = 1 - rotation_volatility * 0.4

        score = base * foul_penalty * rotation_penalty

        if score >= 0.75:
            level = "STABLE"
            risk = False
            rec = "GREEN"
        elif score >= 0.55:
            level = "MODERATE"
            risk = True
            rec = "YELLOW"
        else:
            level = "UNSTABLE"
            risk = True
            rec = "RED"

        return MinuteStabilityResult(
            stability_score=round(score,3),
            stability_level=level,
            risk_flag=risk,
            minutes_projection=projected_minutes,
            recommendation=rec
        )


if __name__ == "__main__":
    print(asdict(MinuteStabilityGate.evaluate(28, 0.3, 0.5)))
