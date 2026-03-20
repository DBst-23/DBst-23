from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


@dataclass
class SafetyFilterResult:
    halftime_trap_flag: bool
    team_rebound_floor_fail: bool
    non_anchor_over_block: bool
    block_pick: bool
    downgrade_pick: bool
    confidence_penalty: int
    reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class LiveFlowSafetyFilters:
    """SharpEdge LiveFlow safety filters for rebound props."""

    TEAM_REBOUND_FLOOR = 36
    HALFTIME_NEAR_LINE_WINDOW = 2.0
    NON_ANCHOR_MIN_SHARE = 0.18
    NON_ANCHOR_MIN_STABILITY = 0.62

    @classmethod
    def evaluate(cls, payload: Dict[str, Any]) -> SafetyFilterResult:
        reasons: List[str] = []

        market = str(payload.get("market", "Rebounds")).lower()
        side = str(payload.get("side", "Higher")).lower()
        role_tier = str(payload.get("role_tier", "conditional")).lower()

        current_stat = float(payload.get("current_stat", 0.0))
        line = float(payload.get("line", 0.0))
        projected_team_rebounds = float(payload.get("projected_team_rebounds", 0.0))
        final_team_rebounds_floor = float(payload.get("team_rebound_floor", cls.TEAM_REBOUND_FLOOR))
        predicted_share = float(payload.get("predicted_share", 0.0))
        stability_score = float(payload.get("stability_score", 0.0))
        win_prob = float(payload.get("win_prob", 0.5))
        live_minutes = float(payload.get("live_minutes", 0.0))
        game_phase = str(payload.get("game_phase", "pregame")).lower()

        halftime_trap_flag = False
        team_rebound_floor_fail = False
        non_anchor_over_block = False
        block_pick = False
        downgrade_pick = False
        confidence_penalty = 0

        if market == "rebounds" and side == "higher":
            remaining_to_clear = line - current_stat

            if game_phase in {"halftime", "q3", "3q"} and remaining_to_clear <= cls.HALFTIME_NEAR_LINE_WINDOW:
                if role_tier != "anchor" and predicted_share < 0.20:
                    halftime_trap_flag = True
                    downgrade_pick = True
                    confidence_penalty += 12
                    reasons.append("HALFTIME_COUNT_TRAP: player is close to the line but does not own anchor rebound share.")

            if projected_team_rebounds and projected_team_rebounds < final_team_rebounds_floor:
                if role_tier != "anchor":
                    team_rebound_floor_fail = True
                    downgrade_pick = True
                    confidence_penalty += 10
                    reasons.append("TEAM_REBOUND_FLOOR_FAIL: projected team rebound pool is too weak for a non-anchor over.")

            if role_tier != "anchor":
                if predicted_share < cls.NON_ANCHOR_MIN_SHARE or stability_score < cls.NON_ANCHOR_MIN_STABILITY:
                    non_anchor_over_block = True
                    block_pick = True
                    confidence_penalty += 20
                    reasons.append("NON_ANCHOR_OVER_BLOCK: rebound share or minute stability is below SharpEdge execution threshold.")

            if live_minutes and live_minutes < 20 and current_stat >= line - 1 and role_tier != "anchor":
                downgrade_pick = True
                confidence_penalty += 6
                reasons.append("EARLY_PACE_ILLUSION: fast first-half count arrived before stable minute proof.")

            if win_prob < 0.55 and (halftime_trap_flag or team_rebound_floor_fail):
                block_pick = True
                confidence_penalty += 8
                reasons.append("EXECUTION_BLOCK: weak probability plus live trap environment.")

        return SafetyFilterResult(
            halftime_trap_flag=halftime_trap_flag,
            team_rebound_floor_fail=team_rebound_floor_fail,
            non_anchor_over_block=non_anchor_over_block,
            block_pick=block_pick,
            downgrade_pick=downgrade_pick,
            confidence_penalty=confidence_penalty,
            reasons=reasons,
        )


def evaluate_liveflow_safety_filters(payload: Dict[str, Any]) -> Dict[str, Any]:
    return LiveFlowSafetyFilters.evaluate(payload).to_dict()


if __name__ == "__main__":
    sample = {
        "market": "Rebounds",
        "side": "Higher",
        "role_tier": "secondary",
        "current_stat": 6,
        "line": 7.5,
        "projected_team_rebounds": 31,
        "predicted_share": 0.16,
        "stability_score": 0.58,
        "win_prob": 0.47,
        "live_minutes": 18,
        "game_phase": "halftime",
    }
    print(evaluate_liveflow_safety_filters(sample))
