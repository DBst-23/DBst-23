from dataclasses import dataclass


@dataclass
class TransitionConfig:
    """
    Config for transition + pace volatility adjustments.
    """
    ENABLED: bool = True

    # Baseline possessions per team we normalize to
    BASE_PACE: float = 98.0

    # How strongly live-rebound and steal-based transition
    # increase pace and scoring opportunities.
    LIVE_REB_FREQ_BOOST: float = 0.35
    STEAL_FREQ_BOOST: float = 0.25

    # How much high 3PA volume amplifies pace inflation.
    THREE_VOL_BOOST: float = 0.20

    # Hard cap on how far we let the multiplier move
    # away from 1.0 in either direction (±15%).
    MAX_PACE_DELTA: float = 0.15


def transition_pace_multiplier(
    poss_per_team: float,
    live_reb_trans_freq: float,
    steal_trans_freq: float,
    three_rate: float,
    cfg: TransitionConfig = TransitionConfig(),
) -> float:
    """
    Compute a pace multiplier based on:
      - overall possessions per team
      - how often teams run off live rebounds
      - how often they run off steals
      - how three-heavy the shot profile is

    The result is a capped multiplier that can bump totals
    up or down but never lets volatility completely explode.
    """
    if not cfg.ENABLED:
        return 1.0

    # Normalize pace to a baseline season value.
    base_ratio = poss_per_team / cfg.BASE_PACE

    # Volatility terms
    live_term = cfg.LIVE_REB_FREQ_BOOST * live_reb_trans_freq
    steal_term = cfg.STEAL_FREQ_BOOST * steal_trans_freq
    three_term = cfg.THREE_VOL_BOOST * three_rate

    raw_multiplier = base_ratio * (1.0 + live_term + steal_term + three_term)

    # Clamp to keep sims realistic.
    lower = 1.0 - cfg.MAX_PACE_DELTA
    upper = 1.0 + cfg.MAX_PACE_DELTA
    return max(lower, min(upper, raw_multiplier)) 