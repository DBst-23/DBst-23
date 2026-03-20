from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


@dataclass
class SafetyFilterResultV2:
    halftime_trap_flag: bool
    team_rebound_floor_fail: bool
    non_anchor_over_block: bool
    blowout_flag: bool
    minute_gate_fail: bool
    block_pick: bool
    downgrade_pick: bool
    confidence_penalty: int
    reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class LiveFlowSafetyFiltersV2:

    TEAM_REBOUND_FLOOR = 36
    HALFTIME_NEAR_LINE_WINDOW = 2.0
    NON_ANCHOR_MIN_SHARE = 0.18
    NON_ANCHOR_MIN_STABILITY = 0.62
    MINUTE_FLOOR = 28
    BLOWOUT_MARGIN = 15

    @classmethod
    def evaluate(cls, payload: Dict[str, Any]) -> SafetyFilterResultV2:
        reasons: List[str] = []

        market = str(payload.get("market", "Rebounds")).lower()
        side = str(payload.get("side", "Higher")).lower()
        role_tier = str(payload.get("role_tier", "conditional")).lower()

        current_stat = float(payload.get("current_stat", 0.0))
        line = float(payload.get("line", 0.0))
        projected_team_rebounds = float(payload.get("projected_team_rebounds", 0.0))
        predicted_share = float(payload.get("predicted_share", 0.0))
        stability_score = float(payload.get("stability_score", 0.0))
        win_prob = float(payload.get("win_prob", 0.5))
        live_minutes = float(payload.get("live_minutes", 0.0))
        game_phase = str(payload.get("game_phase", "pregame")).lower()
        live_margin = float(payload.get("live_margin", 0.0))
        projected_minutes = float(payload.get("projected_minutes", 0.0))

        halftime_trap_flag = False
        team_rebound_floor_fail = False
        non_anchor_over_block = False
        blowout_flag = False
        minute_gate_fail = False
        block_pick = False
        downgrade_pick = False
        confidence_penalty = 0

        if market == "rebounds" and side == "higher":

            remaining_to_clear = line - current_stat

            if game_phase in {"halftime", "q3"} and remaining_to_clear <= cls.HALFTIME_NEAR_LINE_WINDOW:
                if role_tier != "anchor" and predicted_share < 0.20:
                    halftime_trap_flag = True
                    confidence_penalty += 12
                    reasons.append("HALFTIME_TRAP")

            if projected_team_rebounds < cls.TEAM_REBOUND_FLOOR and role_tier != "anchor":
                team_rebound_floor_fail = True
                confidence_penalty += 10
                reasons.append("LOW_REBOUND_ENVIRONMENT")

            if role_tier != "anchor" and (predicted_share < cls.NON_ANCHOR_MIN_SHARE or stability_score < cls.NON_ANCHOR_MIN_STABILITY):
                non_anchor_over_block = True
                confidence_penalty += 20
                reasons.append("NON_ANCHOR_BLOCK")

            if abs(live_margin) >= cls.BLOWOUT_MARGIN:
                blowout_flag = True
                confidence_penalty += 14
                reasons.append("BLOWOUT_VOLATILITY")

            if projected_minutes < cls.MINUTE_FLOOR:
                minute_gate_fail = True
                confidence_penalty += 12
                reasons.append("MINUTE_INSTABILITY")

            if non_anchor_over_block or (halftime_trap_flag and team_rebound_floor_fail) or (blowout_flag and role_tier != "anchor"):
                block_pick = True

            elif minute_gate_fail or team_rebound_floor_fail:
                downgrade_pick = True

            if win_prob < 0.55 and (halftime_trap_flag or blowout_flag):
                block_pick = True
                reasons.append("WEAK_PROBABILITY_BLOCK")

        return SafetyFilterResultV2(
            halftime_trap_flag=halftime_trap_flag,
            team_rebound_floor_fail=team_rebound_floor_fail,
            non_anchor_over_block=non_anchor_over_block,
            blowout_flag=blowout_flag,
            minute_gate_fail=minute_gate_fail,
            block_pick=block_pick,
            downgrade_pick=downgrade_pick,
            confidence_penalty=confidence_penalty,
            reasons=reasons,
        )


def evaluate_liveflow_safety_filters_v2(payload: Dict[str, Any]) -> Dict[str, Any]:
    return LiveFlowSafetyFiltersV2.evaluate(payload).to_dict()
