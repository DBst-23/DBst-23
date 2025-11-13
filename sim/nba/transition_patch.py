from dataclasses import dataclass


@dataclass
class TransitionConfig:
    """
    Global config for NBA transition → totals adjustments.
    This turns halfcourt/transition postmortem data into a % bump
    on our simulated game total.
    """
    ENABLED: bool = True

    # Baseline league references (can be tuned later)
    FREQ_REF: float = 0.18   # ~18% of plays in transition
    EFF_REF: float = 1.20    # 1.20 pts/transition play

    # How much each component matters
    FREQ_WEIGHT: float = 0.60
    EFF_WEIGHT: float = 0.40

    # Hard cap on how much we let totals move (±8%)
    MAX_ADJ: float = 0.08


def _transition_multiplier(freq: float,
                           eff: float,
                           cfg: TransitionConfig = TransitionConfig()) -> float:
    """
    Turn one side's transition profile into a multiplier.
    freq = proportion of plays in transition (0.0–0.4)
    eff  = points per transition play (e.g. 1.05–1.40)
    """
    if not cfg.ENABLED:
        return 1.0

    if cfg.FREQ_REF <= 0 or cfg.EFF_REF <= 0:
        return 1.0

    # Relative deltas vs league baselines
    freq_delta = (freq / cfg.FREQ_REF) - 1.0
    eff_delta = (eff / cfg.EFF_REF) - 1.0

    raw_adj = cfg.FREQ_WEIGHT * freq_delta + cfg.EFF_WEIGHT * eff_delta

    # Clamp so we never explode the total
    clamped = max(-cfg.MAX_ADJ, min(cfg.MAX_ADJ, raw_adj))

    return 1.0 + clamped


def apply_transition_total_patch(
    base_total: float,
    off_freq: float,
    off_eff: float,
    def_freq: float,
    def_eff: float,
    cfg: TransitionConfig = TransitionConfig(),
) -> float:
    """
    Patch a **game total** using transition profiles for both teams.

    Parameters
    ----------
    base_total : model's raw projected total (e.g. 228.7)
    off_freq   : offense transition frequency for Team A (0–1)
    off_eff    : offense transition pts/play for Team A
    def_freq   : defense transition frequency allowed by Team B
    def_eff    : defense transition pts/play allowed by Team B

    Returns
    -------
    float : patched game total
    """
    if not cfg.ENABLED:
        return base_total

    off_mult = _transition_multiplier(off_freq, off_eff, cfg)
    def_mult = _transition_multiplier(def_freq, def_eff, cfg)

    # Simple blend – we can get fancier later if needed
    combined_mult = (off_mult + def_mult) / 2.0

    return base_total * combined_mult