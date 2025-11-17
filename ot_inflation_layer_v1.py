# ot_inflation_layer_v1.py
from dataclasses import dataclass

@dataclass
class OTConfig:
    ENABLED: bool = True
    BASE_POSSESSIONS_PER_OT: float = 6.0    # per team
    POSSESSIONS_VAR: float = 2.0            # +/- randomness
    POINTS_PER_POSS: float = 1.08           # league OT baseline
    POINTS_VAR: float = 0.10                # scoring variance multiplier

def apply_ot_inflation(game_ctx: dict, num_ot: int, cfg: OTConfig = OTConfig()):
    """
    game_ctx expects:
      - 'pred_total_median'
      - 'pred_total_sigma' (optional)
      - 'possessions_per_team' (optional)
    Returns updated game_ctx.
    """
    if not cfg.ENABLED or num_ot <= 0:
        return game_ctx

    import math

    base_total = game_ctx.get("pred_total_median", 0.0)
    base_sigma = game_ctx.get("pred_total_sigma", 12.0)

    # possessions added
    poss_add_per_team = cfg.BASE_POSSESSIONS_PER_OT + cfg.POSSESSIONS_VAR * (num_ot - 1)
    total_extra_poss = 2 * poss_add_per_team * num_ot

    # extra points ~ poss * ppp
    extra_points_mean = total_extra_poss * cfg.POINTS_PER_POSS
    extra_points_sigma = extra_points_mean * cfg.POINTS_VAR

    game_ctx["pred_total_median"] = base_total + extra_points_mean
    game_ctx["pred_total_sigma"] = math.sqrt(base_sigma**2 + extra_points_sigma**2)
    game_ctx["ot_inflation_applied"] = True
    game_ctx["num_ot"] = num_ot
    return game_ctx