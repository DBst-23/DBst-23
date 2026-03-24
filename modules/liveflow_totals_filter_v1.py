# LIVEFLOW TOTALS FILTER V1

class LiveFlowTotalsFilter:
    def __init__(self):
        self.signals = {
            "pace_spike": False,
            "assist_surge": False,
            "three_pt_spike": False,
            "transition_loop": False,
            "halfcourt_lock": False,
            "foul_stagnation": False,
            "regression_window": False
        }

    def evaluate_over_signals(self):
        over_signals = [
            self.signals["pace_spike"],
            self.signals["assist_surge"],
            self.signals["three_pt_spike"],
            self.signals["transition_loop"]
        ]
        return sum(over_signals)

    def evaluate_under_signals(self):
        under_signals = [
            self.signals["halfcourt_lock"],
            self.signals["foul_stagnation"],
            self.signals["regression_window"]
        ]
        return sum(under_signals)

    def classify_environment(self):
        over_score = self.evaluate_over_signals()
        under_score = self.evaluate_under_signals()

        if over_score >= 2:
            return "OVER_ENVIRONMENT_CONFIRMED"
        elif under_score >= 2:
            return "UNDER_ENVIRONMENT_CONFIRMED"
        else:
            return "NO_EDGE_ZONE"

    def decision(self):
        env = self.classify_environment()

        if env == "OVER_ENVIRONMENT_CONFIRMED":
            return {
                "bet": "OVER_ONLY",
                "block": "UNDERS"
            }
        elif env == "UNDER_ENVIRONMENT_CONFIRMED":
            return {
                "bet": "UNDER_ONLY",
                "block": "OVERS"
            }
        else:
            return {
                "bet": "NO_BET",
                "block": "ALL"
            }

# Example usage:
# filter = LiveFlowTotalsFilter()
# filter.signals["pace_spike"] = True
# filter.signals["assist_surge"] = True
# print(filter.decision())
