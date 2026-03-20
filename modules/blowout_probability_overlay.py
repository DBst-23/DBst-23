from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class BlowoutResult:
    blowout_probability: float
    blowout_flag: bool
    minutes_risk: str
    pace_collapse: bool
    recommendation: str

class BlowoutOverlay:

    @staticmethod
    def evaluate(spread, pace_diff, rotation_tightness):

        prob = min(0.95, max(0.05, (abs(spread) / 20.0) + (pace_diff * 0.1)))

        blowout_flag = prob >= 0.60
        pace_collapse = pace_diff < -3

        if blowout_flag and rotation_tightness < 0.6:
            minutes_risk = "HIGH"
            rec = "DOWNGRADE_OVERS"
        elif blowout_flag:
            minutes_risk = "MEDIUM"
            rec = "MONITOR"
        else:
            minutes_risk = "LOW"
            rec = "SAFE"

        return BlowoutResult(
            blowout_probability=round(prob,3),
            blowout_flag=blowout_flag,
            minutes_risk=minutes_risk,
            pace_collapse=pace_collapse,
            recommendation=rec
        )


if __name__ == "__main__":
    print(asdict(BlowoutOverlay.evaluate(12, -2, 0.5)))
