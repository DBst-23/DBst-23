from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class BankrollScalingResult:
    bankroll: float
    risk_per_bet: float
    max_unit: float
    recommended_unit: float
    tier: str


class BankrollScaler:

    @staticmethod
    def scale(bankroll, drawdown, win_rate):

        if drawdown > 0.25:
            risk = 0.005
            tier = "DEFENSIVE"
        elif win_rate > 0.60:
            risk = 0.02
            tier = "AGGRESSIVE"
        else:
            risk = 0.012
            tier = "BALANCED"

        max_unit = bankroll * risk

        return BankrollScalingResult(
            bankroll=bankroll,
            risk_per_bet=risk,
            max_unit=round(max_unit,2),
            recommended_unit=round(max_unit * 0.5,2),
            tier=tier
        )


if __name__ == "__main__":
    print(asdict(BankrollScaler.scale(1000, 0.1, 0.58)))
