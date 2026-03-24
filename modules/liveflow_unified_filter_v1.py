# LIVEFLOW UNIFIED FILTER V1

class LiveFlowUnifiedFilter:
    def __init__(self):
        self.totals_signals = {
            "pace_spike": False,
            "assist_surge": False,
            "three_pt_spike": False,
            "transition_loop": False,
            "halfcourt_lock": False,
            "foul_stagnation": False,
            "regression_window": False,
        }

        self.rebound_signals = {
            "rebound_spike": False,
            "controlled_center_env": False,
            "volatile_rebound_env": False,
            "minutes_stable": False,
            "player_is_center": False,
        }

        self.edge = 0.0

    def _over_score(self):
        return sum([
            self.totals_signals["pace_spike"],
            self.totals_signals["assist_surge"],
            self.totals_signals["three_pt_spike"],
            self.totals_signals["transition_loop"],
        ])

    def _under_score(self):
        return sum([
            self.totals_signals["halfcourt_lock"],
            self.totals_signals["foul_stagnation"],
            self.totals_signals["regression_window"],
        ])

    def classify_totals_environment(self):
        over_score = self._over_score()
        under_score = self._under_score()

        if over_score >= 2:
            return "OVER_ENVIRONMENT_CONFIRMED"
        if under_score >= 2:
            return "UNDER_ENVIRONMENT_CONFIRMED"
        return "NO_EDGE_ZONE"

    def classify_rebound_environment(self):
        if not self.rebound_signals["minutes_stable"]:
            return "NO_REBOUND_BET"
        if not self.rebound_signals["player_is_center"]:
            return "NO_REBOUND_BET"
        if self.rebound_signals["volatile_rebound_env"]:
            return "NO_REBOUND_BET"
        if self.rebound_signals["rebound_spike"]:
            return "REBOUND_OVER_HIGH"
        if self.rebound_signals["controlled_center_env"]:
            return "REBOUND_OVER_MEDIUM"
        return "NO_REBOUND_BET"

    def decision(self):
        if self.edge < 3:
            return {
                "decision": "NO_BET",
                "reason": "NO_EDGE"
            }

        totals_env = self.classify_totals_environment()
        rebound_env = self.classify_rebound_environment()

        if rebound_env == "REBOUND_OVER_HIGH":
            return {
                "decision": "PLAY_REBOUND_OVER",
                "confidence": "HIGH",
                "tag": "LIVE_REBOUND_SPIKE"
            }

        if rebound_env == "REBOUND_OVER_MEDIUM":
            return {
                "decision": "PLAY_REBOUND_OVER",
                "confidence": "MEDIUM",
                "tag": "LIVE_CONTROLLED_CENTER_ENV"
            }

        if totals_env == "OVER_ENVIRONMENT_CONFIRMED":
            return {
                "decision": "PLAY_TOTAL_OVER",
                "confidence": "MEDIUM",
                "tag": "LIVE_PACE_INFLATION"
            }

        if totals_env == "UNDER_ENVIRONMENT_CONFIRMED":
            return {
                "decision": "PLAY_TOTAL_UNDER",
                "confidence": "MEDIUM",
                "tag": "LIVE_HALFCOURT_SUPPRESSION"
            }

        return {
            "decision": "NO_BET",
            "reason": "NO_CLEAR_ALIGNMENT"
        }

# Example:
# f = LiveFlowUnifiedFilter()
# f.totals_signals["pace_spike"] = True
# f.totals_signals["assist_surge"] = True
# f.rebound_signals["minutes_stable"] = True
# f.rebound_signals["player_is_center"] = True
# f.rebound_signals["controlled_center_env"] = True
# f.edge = 6.0
# print(f.decision())
