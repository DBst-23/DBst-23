# UNIFIED PROP FILTER V1

class UnifiedPropFilter:
    def __init__(self):
        # Totals environment
        self.totals_env = None  # OVER / UNDER / NONE
        
        # Rebound environment
        self.rebound_env = None  # SPIKE / STABLE / CONTROLLED / VOLATILE
        
        # Minutes stability
        self.minutes_stable = False
        
        # Player role
        self.player_type = None  # CENTER / WING / GUARD
        
        # Line vs projection
        self.edge = 0.0  # % edge
        
    def evaluate(self):
        
        # HARD BLOCK CONDITIONS
        if not self.minutes_stable:
            return {
                "decision": "NO_BET",
                "reason": "MINUTES_UNSTABLE"
            }
        
        if self.edge < 3:
            return {
                "decision": "NO_BET",
                "reason": "NO_EDGE"
            }
        
        # REBOUND LOGIC
        if self.player_type == "CENTER":
            
            if self.rebound_env == "SPIKE":
                return {
                    "decision": "PLAY_OVER",
                    "confidence": "HIGH",
                    "tag": "REBOUND_SPIKE_ENV"
                }
            
            if self.rebound_env == "CONTROLLED":
                return {
                    "decision": "PLAY_OVER",
                    "confidence": "MEDIUM",
                    "tag": "CONTROLLED_CENTER_EDGE"
                }
            
            if self.rebound_env == "VOLATILE":
                return {
                    "decision": "NO_BET",
                    "reason": "HIGH_VARIANCE_ENV"
                }
        
        # TOTALS LOGIC
        if self.totals_env == "UNDER":
            return {
                "decision": "LEAN_UNDER",
                "confidence": "MEDIUM",
                "tag": "HALFCOURT_SUPPRESSION"
            }
        
        if self.totals_env == "OVER":
            return {
                "decision": "LEAN_OVER",
                "confidence": "MEDIUM",
                "tag": "PACE_INFLATION"
            }
        
        return {
            "decision": "NO_BET",
            "reason": "NO_CLEAR_ALIGNMENT"
        }
