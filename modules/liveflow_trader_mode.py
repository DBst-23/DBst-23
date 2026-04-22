from typing import Dict, Any


def build_liveflow_bet_slip(
    game_label: str,
    market_type: str,
    side: str,
    line: float,
    odds_format: str,
    kelly_result: Dict[str, Any],
    confidence_result: Dict[str, Any],
    middle_band: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Build a standardized LiveFlow execution slip from Kelly sizing output.
    This does not place a real wager. It creates an execution-ready payload.
    """

    total_stake = float(kelly_result.get("recommended_total_stake", 0.0) or 0.0)
    each_leg = float(kelly_result.get("recommended_each_leg", 0.0) or 0.0)
    confidence_tier = confidence_result.get("confidence_tier", "PASS")
    confidence_score = confidence_result.get("confidence_score", 0)
    should_fire = total_stake > 0 and confidence_tier in {"LOCK", "STRONG", "LEAN"}

    slip = {
        "game_label": game_label,
        "market_type": market_type,
        "side": side,
        "line": line,
        "odds_format": odds_format,
        "execution_mode": "LIVEFLOW_TRADER_MODE",
        "confidence_tier": confidence_tier,
        "confidence_score": confidence_score,
        "recommended_total_stake": round(total_stake, 2),
        "recommended_each_leg": round(each_leg, 2),
        "should_fire": should_fire,
        "ticket_type": "single_leg",
        "notes": [],
    }

    if middle_band:
        slip["middle_band"] = middle_band
        slip["ticket_type"] = "middle_structure"
        slip["notes"].append("Middle band active: use split-stake structure if second line is available.")

    if should_fire:
        slip["notes"].append("Execution approved by Kelly + confidence layer.")
    else:
        slip["notes"].append("No execution approval. Edge or sizing too weak.")

    return slip
