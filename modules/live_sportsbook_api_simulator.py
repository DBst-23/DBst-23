from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import random


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def american_to_implied_prob(odds: int) -> float:
    if odds > 0:
        return 100.0 / (odds + 100.0)
    return abs(odds) / (abs(odds) + 100.0)


def implied_prob_to_american(prob: float) -> int:
    prob = max(0.01, min(0.99, prob))
    if prob >= 0.5:
        return int(round(-(prob / (1.0 - prob)) * 100))
    return int(round(((1.0 - prob) / prob) * 100))


def simulate_market_move(
    entry_odds: int,
    minutes_to_settle: int,
    volatility: float = 0.08,
    drift: float = 0.0,
) -> Dict[str, Any]:
    base_prob = american_to_implied_prob(entry_odds)
    move_scale = min(0.18, volatility * max(0.5, minutes_to_settle / 30.0))
    closing_prob = max(0.01, min(0.99, base_prob + drift + random.uniform(-move_scale, move_scale)))
    closing_odds = implied_prob_to_american(closing_prob)

    if entry_odds > 0:
        clv_delta = entry_odds - closing_odds
    else:
        clv_delta = abs(closing_odds) - abs(entry_odds)

    return {
        "entry_odds": entry_odds,
        "closing_odds": closing_odds,
        "entry_implied_prob": round(base_prob, 4),
        "closing_implied_prob": round(closing_prob, 4),
        "clv_delta": clv_delta,
    }


def simulate_fill(
    requested_stake: float,
    max_book_limit: float,
    slippage_pct: float = 0.0,
) -> Dict[str, Any]:
    requested_stake = float(requested_stake)
    max_book_limit = float(max_book_limit)
    slippage_pct = max(0.0, float(slippage_pct))

    accepted_stake = min(requested_stake, max_book_limit)
    filled_stake = round(accepted_stake * (1.0 - slippage_pct), 2)
    rejected_stake = round(requested_stake - filled_stake, 2)

    if filled_stake <= 0:
        fill_status = "REJECTED"
    elif filled_stake < requested_stake:
        fill_status = "PARTIAL_FILL"
    else:
        fill_status = "FILLED"

    return {
        "requested_stake": round(requested_stake, 2),
        "filled_stake": filled_stake,
        "rejected_stake": rejected_stake,
        "fill_status": fill_status,
    }


def simulate_bet_execution(
    player: str,
    market: str,
    side: str,
    line: float,
    entry_odds: int,
    requested_stake: float,
    max_book_limit: float,
    minutes_to_settle: int,
    volatility: float = 0.08,
    drift: float = 0.0,
    slippage_pct: float = 0.0,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    fill = simulate_fill(
        requested_stake=requested_stake,
        max_book_limit=max_book_limit,
        slippage_pct=slippage_pct,
    )
    market_move = simulate_market_move(
        entry_odds=entry_odds,
        minutes_to_settle=minutes_to_settle,
        volatility=volatility,
        drift=drift,
    )

    execution_allowed = fill["fill_status"] != "REJECTED"

    return {
        "timestamp": utc_now_iso(),
        "player": player,
        "market": market,
        "side": side,
        "line": float(line),
        "entry_odds": int(entry_odds),
        "execution_allowed": execution_allowed,
        "fill": fill,
        "market_move": market_move,
        "metadata": metadata or {},
    }


def simulate_execution_batch(execution_packets: List[Dict[str, Any]]) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []
    approved = 0
    blocked = 0

    for packet in execution_packets:
        if not packet.get("execution_allowed", False):
            blocked += 1
            results.append(
                {
                    "player": packet.get("player", ""),
                    "execution_allowed": False,
                    "execution_action": packet.get("execution_action", "DO_NOT_BET"),
                    "reason": packet.get("decision", {}).get("reason", "Blocked upstream"),
                }
            )
            continue

        approved += 1
        sizing = packet.get("sizing", {})
        projection = packet.get("projection", {})
        result = simulate_bet_execution(
            player=packet.get("player", ""),
            market=packet.get("market", "Rebounds"),
            side=packet.get("side", "Over"),
            line=float(packet.get("line_live", packet.get("line", 0.0))),
            entry_odds=int(packet.get("entry_odds", -115)),
            requested_stake=float(sizing.get("recommended_stake", 0.0)),
            max_book_limit=float(packet.get("max_book_limit", 25.0)),
            minutes_to_settle=int(packet.get("minutes_to_settle", 30)),
            volatility=float(packet.get("volatility", 0.08)),
            drift=float(packet.get("drift", 0.0)),
            slippage_pct=float(packet.get("slippage_pct", 0.0)),
            metadata={
                "recommended_units": sizing.get("recommended_units", 0.0),
                "win_prob": projection.get("win_prob", 0.0),
                "edge": projection.get("edge", 0.0),
                "sizing_tag": sizing.get("sizing_tag", "STANDARD_SIZING"),
            },
        )
        results.append(result)

    return {
        "approved_count": approved,
        "blocked_count": blocked,
        "results": results,
    }


if __name__ == "__main__":
    sample_packets = [
        {
            "player": "Rudy Gobert",
            "market": "Rebounds",
            "side": "Over",
            "line_live": 12.5,
            "entry_odds": -118,
            "execution_allowed": True,
            "sizing": {"recommended_stake": 18.5, "recommended_units": 1.85, "sizing_tag": "CHAOS_BIG_BOOST"},
            "projection": {"win_prob": 0.63, "edge": 1.4},
            "max_book_limit": 25.0,
            "minutes_to_settle": 28,
            "volatility": 0.07,
            "drift": 0.01,
            "slippage_pct": 0.02,
        },
        {
            "player": "Wing Player",
            "execution_allowed": False,
            "execution_action": "DO_NOT_BET",
            "decision": {"reason": "NO_PLAY_OREB_CHAOS_FADE"},
        },
    ]

    print(simulate_execution_batch(sample_packets))
