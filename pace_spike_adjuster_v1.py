"""
pace_spike_adjuster_v1.py
SharpEdge NBA Engine – Pace Spike Dampener Module

Purpose:
---------
This module reduces overreaction to sudden pace spikes that occur due to:
- 2H tempo accelerations
- transition surges
- momentum runs (8–0, 10–2)
- foul-induced stoppage/restart cycles
- end-of-quarter acceleration
- OT pace inflation

It applies a dynamic dampener to possession projection curves and
total-points projection curves to stabilize model estimates.

Patch ID:
---------
PACE_SPIKE_ADJUSTER_V1 (Nov 2025)
"""

class PaceSpikeAdjusterV1:
    def __init__(self):
        # How aggressive the dampener is (0.0–1.0)
        self.max_dampen = 0.18  # caps spike influence at ~18%
        self.run_threshold = 7   # scoring run detection
        self.transition_threshold = 1.35  # over baseline transition rate
        self.quarter_spike_penalty = {
            3: 0.10,   # Q3 spike dampener
            4: 0.15,   # Q4 spike dampener
            "OT": 0.20 # OT spike dampener
        }

    def detect_scoring_run(self, scoring_sequence):
        """
        scoring_sequence: list of possession outcomes (+1, +2, +3, +0)
        Returns True if either team has a run >= run_threshold.
        """
        current = 0
        for pts in scoring_sequence:
            current += pts
            if current >= self.run_threshold:
                return True
            if pts <= 0:
                current = 0
        return False

    def apply_transition_dampen(self, baseline_transition_rate, observed_rate):
        """
        Dampens transition-based pace inflation when it exceeds threshold.
        """
        if observed_rate <= baseline_transition_rate * self.transition_threshold:
            return 1.0

        # Excess transition inflation
        excess = (observed_rate / baseline_transition_rate) - 1
        dampen = min(self.max_dampen, excess * 0.5)
        return 1.0 - dampen

    def adjust_possessions(self, projected_possessions, quarter, scoring_sequence,
                           baseline_transition_rate, observed_transition_rate,
                           is_overtime=False):
        """
        Main adjustment pipeline.
        """
        damp_factor = 1.0

        # OT inflation first
        if is_overtime:
            damp_factor *= (1 - self.quarter_spike_penalty["OT"])

        # Q3 / Q4 dampen rules
        if quarter in self.quarter_spike_penalty:
            damp_factor *= (1 - self.quarter_spike_penalty[quarter])

        # scoring run detection damp
        if self.detect_scoring_run(scoring_sequence):
            damp_factor *= (1 - 0.12)

        # transition spike damp
        trans_damp = self.apply_transition_dampen(
            baseline_transition_rate,
            observed_transition_rate
        )
        damp_factor *= trans_damp

        # final adjusted possessions
        adjusted = projected_possessions * damp_factor
        return max(adjusted, projected_possessions * 0.82)  # floor safeguard