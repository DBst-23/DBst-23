from dataclasses import dataclass
from .transition_patch import compute_transition_delta

@dataclass
class TeamProfile:
    pace: float               # possessions per game
    off_rating: float         # points per 100 poss
    def_rating: float         # points allowed per 100 poss
    trans_freq: float         # transition frequency (0–1)
    trans_eff: float          # transition pts/poss (relative)
    def_trans_freq: float     # allowed transition freq
    def_trans_eff: float      # allowed transition eff

@dataclass
class GameInputs:
    home: TeamProfile
    away: TeamProfile

class NBATotalsEngine:

    @staticmethod
    def simulate_total(inputs: GameInputs):
        """
        Main NBA totals projection using:
        - pace
        - offensive + defensive ratings
        - transition patch overlay
        """

        # 1) Base possessions estimate
        base_pace = (inputs.home.pace + inputs.away.pace) / 2

        # 2) Base offensive expectation (points per possession)
        home_ppp = (inputs.home.off_rating + inputs.away.def_rating) / 200
        away_ppp = (inputs.away.off_rating + inputs.home.def_rating) / 200

        # 3) Apply transition patch
        transition_delta = compute_transition_delta(inputs)

        # 4) Raw total before modifiers
        raw_total = (home_ppp + away_ppp) * base_pace

        # 5) Final total
        final_total = raw_total + transition_delta

        return {
            "pace": base_pace,
            "home_ppp": home_ppp,
            "away_ppp": away_ppp,
            "transition_delta": transition_delta,
            "raw_total": raw_total,
            "final_total_mean": final_total,
            "final_total_median": final_total * 0.98,   # median slightly lower
        }