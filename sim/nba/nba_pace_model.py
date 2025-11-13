from dataclasses import dataclass


@dataclass
class PaceContext:
    """
    Game-level pace context modifiers.
    All fields are optional and can be left at defaults.
    """
    is_back_to_back_home: bool = False
    is_back_to_back_away: bool = False
    altitude_game: bool = False  # e.g. DEN / UTA type environments
    projected_close_spread: float = 5.0  # smaller spread → tighter, higher pace late
    playoff_intensity: bool = False


@dataclass
class TeamPaceProfile:
    """
    Minimal pace profile for one team.
    All rates are per-game or per-possession fractions.
    """
    base_pace: float                  # possessions per game (season baseline)
    last10_pace: float                # possessions per game (last 10)
    home_away_adj: float              # +1 / -1 style tweak, or 0 if unknown
    transition_freq_off: float        # 0.0–1.0 fraction of plays in transition (offense)
    transition_eff_off: float         # pts per transition play (1.0–1.5 typical)
    transition_freq_def: float        # allowed transition freq
    transition_eff_def: float         # allowed transition eff
    long_reb_three_rate: float        # fraction of FGA that are 3s or long mid (0.0–1.0)


@dataclass
class GamePaceInputs:
    home: TeamPaceProfile
    away: TeamPaceProfile
    context: PaceContext = PaceContext()


def _blend_baseline_pace(home: TeamPaceProfile, away: TeamPaceProfile) -> float:
    """
    Blend season and last-10 pace for both teams and average.
    """
    home_blend = 0.65 * home.base_pace + 0.35 * home.last10_pace
    away_blend = 0.65 * away.base_pace + 0.35 * away.last10_pace
    return (home_blend + away_blend) / 2.0


def _transition_pressure_adjustment(home: TeamPaceProfile, away: TeamPaceProfile) -> float:
    """
    Compute a small +/- % adjustment based on how much both teams
    want to run and how leaky they are in transition.
    Returns a multiplier like 0.96–1.08.
    """
    # Offensive desire to run
    off_pressure_home = home.transition_freq_off * home.transition_eff_off
    off_pressure_away = away.transition_freq_off * away.transition_eff_off

    # Defensive leakiness
    def_leak_home = home.transition_freq_def * home.transition_eff_def
    def_leak_away = away.transition_freq_def * away.transition_eff_def

    # Long rebound environment from 3s / long mid
    long_reb_env = (home.long_reb_three_rate + away.long_reb_three_rate) / 2.0

    # Normalize against rough league anchors
    # (freq ~0.16, eff ~1.20, long_reb_three_rate ~0.45)
    anchor_freq_eff = 0.16 * 1.20
    off_delta = ((off_pressure_home + off_pressure_away) / (2 * anchor_freq_eff)) - 1.0
    def_delta = ((def_leak_home + def_leak_away) / (2 * anchor_freq_eff)) - 1.0
    long_reb_delta = (long_reb_env / 0.45) - 1.0

    # Weight them
    raw = 0.45 * off_delta + 0.35 * def_delta + 0.20 * long_reb_delta

    # Clamp so pace multiplier never goes crazy
    raw = max(-0.10, min(0.10, raw))
    return 1.0 + raw


def _context_adjustment_multiplier(ctx: PaceContext) -> float:
    """
    Adjust for game-level context: back-to-back, altitude, spread, playoffs.
    Returns a multiplier like 0.95–1.05.
    """
    adj = 0.0

    # Back-to-back tends to shave a bit of pace overall
    if ctx.is_back_to_back_home:
        adj -= 0.02
    if ctx.is_back_to_back_away:
        adj -= 0.02

    # Altitude games tend to play slightly faster due to fatigue & early-clock shots
    if ctx.altitude_game:
        adj += 0.02

    # Close spread games: more fouling & late-game possessions
    # Large spread: more garbage time / low urgency
    if ctx.projected_close_spread <= 4.0:
        adj += 0.02
    elif ctx.projected_close_spread >= 10.0:
        adj -= 0.01

    # Playoff intensity can either slow or tighten, here we assume mild slowdown
    if ctx.playoff_intensity:
        adj -= 0.02

    adj = max(-0.05, min(0.05, adj))
    return 1.0 + adj


def predict_pace(inputs: GamePaceInputs) -> float:
    """
    Predict possessions per team for an NBA game using:
      - blended season + last-10 pace
      - transition pressure & long rebound environment
      - game-level context (B2B, spread, altitude, playoffs)
    """
    base = _blend_baseline_pace(inputs.home, inputs.away)

    trans_mult = _transition_pressure_adjustment(inputs.home, inputs.away)
    ctx_mult = _context_adjustment_multiplier(inputs.context)

    raw_pace = base * trans_mult * ctx_mult

    # Clamp to a realistic band for most NBA games
    # This is per-team possessions.
    return max(92.0, min(110.0, raw_pace))