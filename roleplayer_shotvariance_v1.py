# roleplayer_shotvariance_v1.py
from dataclasses import dataclass

@dataclass
class RPVConfig:
    ENABLED: bool = True
    USAGE_SPIKE_PROB: float = 0.12      # chance of usage spike game
    EFF_SPIKE_PROB: float = 0.10        # chance of hot shooting game
    USAGE_MULT: float = 1.35            # 35% more FGA in spike
    EFF_MULT: float = 1.10              # 10% bump to FG%/3P%
    MAX_SPIKE_ROLE_USG: float = 0.24    # avoid turning them into stars

def apply_roleplayer_variance(player_ctx: dict, cfg: RPVConfig = RPVConfig(), rng=None):
    """
    player_ctx expects:
      - 'role': 'bench'/'role'/'star'
      - 'usage_rate' (0–1)
      - 'fg_pct' (0–1)
      - 'three_pt_pct' (0–1)
    Returns updated player_ctx.
    """
    if not cfg.ENABLED:
        return player_ctx

    if player_ctx.get("role") not in ("bench", "role"):
        return player_ctx

    import random
    r = rng or random

    usage = player_ctx.get("usage_rate", 0.18)
    fg = player_ctx.get("fg_pct", 0.45)
    tp = player_ctx.get("three_pt_pct", 0.35)

    spike_used = False

    # Usage spike
    if r.random() < cfg.USAGE_SPIKE_PROB:
        usage = min(usage * cfg.USAGE_MULT, cfg.MAX_SPIKE_ROLE_USG)
        spike_used = True

    # Efficiency spike
    if r.random() < cfg.EFF_SPIKE_PROB:
        fg = min(fg * cfg.EFF_MULT, 0.70)
        tp = min(tp * cfg.EFF_MULT, 0.60)
        spike_used = True

    player_ctx["usage_rate"] = usage
    player_ctx["fg_pct"] = fg
    player_ctx["three_pt_pct"] = tp
    player_ctx["rpv_spike_flag"] = spike_used
    return player_ctx