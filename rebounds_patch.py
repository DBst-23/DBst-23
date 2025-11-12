from dataclasses import dataclass

@dataclass
class RebConfig:
    ENABLED: bool = True
    PACE_REF: float = 96.0
    PACE_ELASTICITY: float = 0.70   # elasticity raised from 0.65 → 0.70
    SHOT_MIX_WEIGHT: float = 0.25
    FOUL_RISK_DAMP: float = 0.10


def dynamic_reb_chances(base_chances, poss_per_team, long_reb_share, foul_gate_on, cfg: RebConfig):
    """Compute rebound chances adjusted for pace, shot mix, and foul risk."""
    if not cfg.ENABLED:
        return base_chances
    pace_ratio = (poss_per_team / cfg.PACE_REF) ** cfg.PACE_ELASTICITY
    mix_boost = 1.0 + cfg.SHOT_MIX_WEIGHT * (long_reb_share - 0.35)
    foul_damp = (1.0 - cfg.FOUL_RISK_DAMP) if foul_gate_on else 1.0
    return base_chances * pace_ratio * mix_boost * foul_damp