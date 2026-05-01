from dataclasses import dataclass
from typing import Optional, Dict, Any

from .nba_pace_model import (
    predict_pace,
    GamePaceInputs,
    TeamPaceProfile,
    PaceContext,
)
from .transition_patch import apply_transition_total_patch
from .sim.nba.hv_totals_guardrail import HVInputs, compute_hv_guardrail, hv_to_dict


@dataclass
class TeamProfile:
    pace: float               # possessions per game
    off_rating: float         # points per 100 poss
    def_rating: float         # points allowed per 100 poss
    trans_freq: float         # transition frequency (0-1)
    trans_eff: float          # transition pts/poss or relative efficiency
    def_trans_freq: float     # allowed transition frequency
    def_trans_eff: float      # allowed transition efficiency

    last10_pace: Optional[float] = None
    long_reb_three_rate: float = 0.40
    home_away_adj: float = 0.0
    spread: float = 0.0
    is_b2b: bool = False


@dataclass
class GameInputs:
    home: TeamProfile
    away: TeamProfile
    hv_inputs: Optional[HVInputs] = None
    context: Optional[PaceContext] = None


class NBATotalsEngine:
    """
    Main NBA totals projection engine.

    Uses:
    - structured pace model (`GamePaceInputs`)
    - offensive/defensive efficiency blend
    - transition total patch
    - high-volatility totals guardrail
    """

    @staticmethod
    def _to_pace_profile(team: TeamProfile) -> TeamPaceProfile:
        return TeamPaceProfile(
            base_pace=team.pace,
            last10_pace=team.last10_pace if team.last10_pace is not None else team.pace,
            home_away_adj=team.home_away_adj,
            transition_freq_off=team.trans_freq,
            transition_eff_off=team.trans_eff,
            transition_freq_def=team.def_trans_freq,
            transition_eff_def=team.def_trans_eff,
            long_reb_three_rate=team.long_reb_three_rate,
        )

    @staticmethod
    def simulate_total(inputs: GameInputs) -> Dict[str, Any]:
        context = inputs.context or PaceContext(
            is_back_to_back_home=inputs.home.is_b2b,
            is_back_to_back_away=inputs.away.is_b2b,
            projected_close_spread=abs(inputs.home.spread),
        )

        pace_inputs = GamePaceInputs(
            home=NBATotalsEngine._to_pace_profile(inputs.home),
            away=NBATotalsEngine._to_pace_profile(inputs.away),
            context=context,
        )

        base_pace = predict_pace(pace_inputs)

        home_ppp = (inputs.home.off_rating + inputs.away.def_rating) / 200.0
        away_ppp = (inputs.away.off_rating + inputs.home.def_rating) / 200.0
        raw_total = (home_ppp + away_ppp) * base_pace

        transition_patched_total = apply_transition_total_patch(
            base_total=raw_total,
            off_freq=inputs.home.trans_freq,
            off_eff=inputs.home.trans_eff,
            def_freq=inputs.away.def_trans_freq,
            def_eff=inputs.away.def_trans_eff,
        )
        transition_delta = transition_patched_total - raw_total

        hv_result = compute_hv_guardrail(transition_patched_total, inputs.hv_inputs)
        final_mean = transition_patched_total + hv_result.volatility_boost
        final_median = final_mean * 0.98

        output: Dict[str, Any] = {
            "pace": base_pace,
            "home_ppp": home_ppp,
            "away_ppp": away_ppp,
            "raw_total": raw_total,
            "transition_patched_total": transition_patched_total,
            "transition_delta": transition_delta,
            "final_total_mean": final_mean,
            "final_total_median": final_median,
        }
        output.update(hv_to_dict(hv_result))
        return output
