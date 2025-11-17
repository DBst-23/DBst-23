# foul_risk_gate_v2.py
from dataclasses import dataclass

@dataclass
class FoulRiskConfig:
    ENABLED: bool = True
    EARLY_FOUL_THRESHOLD: int = 2          # fouls in 1st stint / 1Q
    HIGH_RISK_FOUL_RATE: float = 0.045     # fouls per minute flag
    MINUTES_PENALTY_PER_FOUL: float = 1.5  # minutes shaved off projection
    VOL_INFLATE_REB: float = 0.15          # rebound variance bump
    VOL_INFLATE_PTS: float = 0.12          # scoring variance bump

def apply_foul_risk_gate(player_ctx: dict, cfg: FoulRiskConfig = FoulRiskConfig()):
    """
    player_ctx expects:
      - 'pos' (str): position tag: 'big','wing','guard'
      - 'fouls_per_min' (float): historical foul rate
      - 'proj_minutes' (float): pre-foul-projected minutes
      - 'early_foul_count' (int): fouls picked up in early stint
      - 'var_reb' (float): current variance for rebounds
      - 'var_pts' (float): current variance for points
    Returns updated player_ctx.
    """
    if not cfg.ENABLED:
        return player_ctx

    # only hit bigs / rim protectors hardest
    if player_ctx.get("pos") not in ("big", "pf/c", "c"):
        return player_ctx

    early_fouls = player_ctx.get("early_foul_count", 0)
    foul_rate = player_ctx.get("fouls_per_min", 0.0)

    high_risk = (
        early_fouls >= cfg.EARLY_FOUL_THRESHOLD or
        foul_rate >= cfg.HIGH_RISK_FOUL_RATE
    )
    if not high_risk:
        return player_ctx

    # shave minutes
    minutes_before = player_ctx.get("proj_minutes", 0.0)
    penalty = cfg.MINUTES_PENALTY_PER_FOUL * max(0, early_fouls - 1)
    player_ctx["proj_minutes"] = max(0.0, minutes_before - penalty)

    # inflate variance bands for props
    player_ctx["var_reb"] = player_ctx.get("var_reb", 1.0) * (1.0 + cfg.VOL_INFLATE_REB)
    player_ctx["var_pts"] = player_ctx.get("var_pts", 1.0) * (1.0 + cfg.VOL_INFLATE_PTS)
    player_ctx["foul_risk_gate_v2_active"] = True
    return player_ctx