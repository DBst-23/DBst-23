from __future__ import annotations

from typing import Any, Dict


BIG_POSITIONS = {"C", "PF", "F-C", "C-F"}
FRAGILE_POSITIONS = {"PG", "SG", "SF", "G", "F", "G-F", "F-G"}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def compute_base_unit_multiplier(
    win_prob: float,
    edge: float,
    recommendation: str,
) -> float:
    multiplier = 1.0

    if win_prob >= 0.70:
        multiplier += 0.35
    elif win_prob >= 0.62:
        multiplier += 0.20
    elif win_prob >= 0.56:
        multiplier += 0.10
    elif win_prob < 0.52:
        multiplier -= 0.20

    if edge >= 2.0:
        multiplier += 0.20
    elif edge >= 1.0:
        multiplier += 0.10
    elif edge <= 0.0:
        multiplier -= 0.25

    recommendation = (recommendation or "").upper()
    if "NO_PLAY" in recommendation or "BLOCK" in recommendation:
        multiplier = 0.0
    elif "LOCK" in recommendation:
        multiplier += 0.10
    elif "THIN" in recommendation:
        multiplier -= 0.10

    return round(clamp(multiplier, 0.0, 1.75), 3)


def compute_chaos_sizing_modifier(
    player_position: str,
    chaos_active: bool,
    chaos_tag: str,
    chaos_override: str,
    kill_switch_active: bool,
) -> Dict[str, Any]:
    position = (player_position or "").upper()
    tag = (chaos_tag or "OREB_CHAOS_LOW").upper()
    override = (chaos_override or "NONE").upper()

    multiplier = 1.0
    sizing_tag = "STANDARD_SIZING"
    reason = "No chaos sizing adjustment applied"

    if kill_switch_active:
        return {
            "multiplier": 0.0,
            "sizing_tag": "KILL_SWITCH_ZERO_OUT",
            "reason": "Kill-switch active, no stake allowed",
        }

    if not chaos_active:
        return {
            "multiplier": multiplier,
            "sizing_tag": sizing_tag,
            "reason": reason,
        }

    if override == "FRAGILE_PROFILE_BLOCK" or position in FRAGILE_POSITIONS:
        return {
            "multiplier": 0.0,
            "sizing_tag": "CHAOS_FADE_ZERO_OUT",
            "reason": "OREB chaos active on fragile rebound profile",
        }

    if override == "ANCHOR_BIG_PROTECTED" or position in BIG_POSITIONS:
        if tag == "OREB_CHAOS_EXTREME":
            multiplier = 1.35
            sizing_tag = "CHAOS_BIG_MAX_BOOST"
            reason = "Extreme OREB chaos with protected anchor big"
        elif tag == "OREB_CHAOS_ELEVATED":
            multiplier = 1.22
            sizing_tag = "CHAOS_BIG_BOOST"
            reason = "Elevated OREB chaos with protected anchor big"
        else:
            multiplier = 1.10
            sizing_tag = "CHAOS_BIG_LIGHT_BOOST"
            reason = "Moderate OREB chaos with protected anchor big"
        return {
            "multiplier": round(multiplier, 3),
            "sizing_tag": sizing_tag,
            "reason": reason,
        }

    return {
        "multiplier": 0.90,
        "sizing_tag": "CHAOS_CAUTION",
        "reason": "OREB chaos active without anchor-big protection",
    }


def compute_recommended_stake(
    bankroll: float,
    base_unit_size: float,
    player_position: str,
    win_prob: float,
    edge: float,
    recommendation: str,
    chaos_active: bool,
    chaos_tag: str,
    chaos_override: str = "NONE",
    kill_switch_active: bool = False,
    max_units: float = 2.0,
) -> Dict[str, Any]:
    bankroll = float(bankroll)
    base_unit_size = float(base_unit_size)
    win_prob = float(win_prob)
    edge = float(edge)

    base_mult = compute_base_unit_multiplier(
        win_prob=win_prob,
        edge=edge,
        recommendation=recommendation,
    )
    chaos_mod = compute_chaos_sizing_modifier(
        player_position=player_position,
        chaos_active=chaos_active,
        chaos_tag=chaos_tag,
        chaos_override=chaos_override,
        kill_switch_active=kill_switch_active,
    )

    final_units = base_mult * float(chaos_mod["multiplier"])
    final_units = clamp(final_units, 0.0, max_units)

    recommended_stake = round(base_unit_size * final_units, 2)
    bankroll_pct = round((recommended_stake / bankroll) * 100.0, 3) if bankroll > 0 else 0.0

    if recommended_stake <= 0:
        final_decision = "NO_BET"
    elif final_units >= 1.5:
        final_decision = "PRESS_EDGE"
    elif final_units >= 1.0:
        final_decision = "STANDARD_FIRE"
    elif final_units >= 0.5:
        final_decision = "REDUCED_SIZE"
    else:
        final_decision = "MICRO_SIZE"

    return {
        "recommended_stake": recommended_stake,
        "recommended_units": round(final_units, 3),
        "bankroll_pct": bankroll_pct,
        "base_unit_multiplier": round(base_mult, 3),
        "chaos_multiplier": round(float(chaos_mod["multiplier"]), 3),
        "sizing_tag": chaos_mod["sizing_tag"],
        "final_decision": final_decision,
        "reason": chaos_mod["reason"],
    }


if __name__ == "__main__":
    print(
        compute_recommended_stake(
            bankroll=500.0,
            base_unit_size=10.0,
            player_position="C",
            win_prob=0.63,
            edge=1.4,
            recommendation="OREB_CHAOS_BIG_BOOST",
            chaos_active=True,
            chaos_tag="OREB_CHAOS_ELEVATED",
            chaos_override="ANCHOR_BIG_PROTECTED",
            kill_switch_active=False,
        )
    )
