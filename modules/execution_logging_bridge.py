from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import hashlib
import json


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_execution_entry_id(sport: str, market: str, player: str, timestamp_iso: Optional[str] = None) -> str:
    ts = timestamp_iso or utc_now_iso()
    compact_date = ts[:10].replace("-", "_")
    player_slug = "_".join(str(player).upper().split())[:24]
    market_slug = "_".join(str(market).upper().split())[:16]
    return f"EXEC_{compact_date}_{sport.upper()}_{market_slug}_{player_slug}"


def compute_audit_hash(payload: Dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build_github_execution_record(
    execution_result: Dict[str, Any],
    sport: str = "NBA",
    platform: str = "Underdog",
    mode: str = "LiveFlow",
) -> Dict[str, Any]:
    timestamp = execution_result.get("timestamp") or utc_now_iso()
    player = str(execution_result.get("player", ""))
    market = str(execution_result.get("market", "Rebounds"))
    entry_id = build_execution_entry_id(sport=sport, market=market, player=player, timestamp_iso=timestamp)

    fill = execution_result.get("fill", {})
    market_move = execution_result.get("market_move", {})
    metadata = execution_result.get("metadata", {})

    record = {
        "entry_id": entry_id,
        "timestamp": timestamp,
        "date": timestamp[:10],
        "sport": sport,
        "platform": platform,
        "mode": mode,
        "player": player,
        "market": market,
        "side": execution_result.get("side", "Over"),
        "line": float(execution_result.get("line", 0.0)),
        "entry_odds": int(execution_result.get("entry_odds", -115)),
        "execution_allowed": bool(execution_result.get("execution_allowed", False)),
        "fill_status": fill.get("fill_status", "UNKNOWN"),
        "requested_stake": round(float(fill.get("requested_stake", 0.0)), 2),
        "filled_stake": round(float(fill.get("filled_stake", 0.0)), 2),
        "rejected_stake": round(float(fill.get("rejected_stake", 0.0)), 2),
        "closing_odds": market_move.get("closing_odds"),
        "entry_implied_prob": market_move.get("entry_implied_prob"),
        "closing_implied_prob": market_move.get("closing_implied_prob"),
        "clv_delta": market_move.get("clv_delta"),
        "metadata": metadata,
        "archive_status": "archived",
    }
    record["audit_hash"] = compute_audit_hash(record)
    return record


def to_jsonl_line(record: Dict[str, Any]) -> str:
    return json.dumps(record, sort_keys=False) + "\n"


def build_github_execution_batch(records: List[Dict[str, Any]]) -> str:
    return "".join(to_jsonl_line(record) for record in records)


def build_airtable_execution_record(
    execution_record: Dict[str, Any],
    result_status: str = "PENDING",
    bet_quality: str = "LiveFlow Active",
    card_type: str = "2-Pick Champion",
    bet_category: str = "Live Bet",
) -> Dict[str, Any]:
    filled_stake = float(execution_record.get("filled_stake", 0.0))
    market = str(execution_record.get("market", "Rebounds"))

    payout = 0.0
    entry_odds = int(execution_record.get("entry_odds", -115))
    if filled_stake > 0:
        if entry_odds > 0:
            payout = filled_stake + (filled_stake * (entry_odds / 100.0))
        else:
            payout = filled_stake + (filled_stake * (100.0 / abs(entry_odds)))

    return {
        "Name": f"AUTO-EXEC {execution_record.get('player', '')} {execution_record.get('side', '')} {execution_record.get('line', '')} {market}",
        "DATE": execution_record.get("date"),
        "SPORT": execution_record.get("sport", "NBA"),
        "CARD_TYPE": card_type,
        "STAKE": round(filled_stake, 2),
        "PAYOUT": round(payout, 2),
        "RESULT": result_status,
        "PROFIT": 0,
        "ODDS": execution_record.get("entry_odds", -115),
        "MARKET": market,
        "BOOK": execution_record.get("platform", "Underdog"),
        "UNIT_SIZE": round(float(execution_record.get("metadata", {}).get("recommended_units", 0.0)), 2),
        "EDGE_SCORE": round(float(execution_record.get("metadata", {}).get("win_prob", 0.0)) * 100),
        "BET_CATEGORY": bet_category,
        "BET_QUALITY": bet_quality,
    }


def build_sync_payload(
    execution_results: List[Dict[str, Any]],
    sport: str = "NBA",
    platform: str = "Underdog",
    mode: str = "LiveFlow",
) -> Dict[str, Any]:
    github_records: List[Dict[str, Any]] = []
    airtable_records: List[Dict[str, Any]] = []

    for result in execution_results:
        github_record = build_github_execution_record(
            execution_result=result,
            sport=sport,
            platform=platform,
            mode=mode,
        )
        github_records.append(github_record)
        airtable_records.append(build_airtable_execution_record(github_record))

    return {
        "github_records": github_records,
        "github_jsonl": build_github_execution_batch(github_records),
        "airtable_records": airtable_records,
    }


if __name__ == "__main__":
    sample_execution = {
        "timestamp": utc_now_iso(),
        "player": "Rudy Gobert",
        "market": "Rebounds",
        "side": "Over",
        "line": 12.5,
        "entry_odds": -118,
        "execution_allowed": True,
        "fill": {
            "requested_stake": 18.5,
            "filled_stake": 18.13,
            "rejected_stake": 0.37,
            "fill_status": "PARTIAL_FILL",
        },
        "market_move": {
            "closing_odds": -129,
            "entry_implied_prob": 0.5413,
            "closing_implied_prob": 0.5633,
            "clv_delta": 11,
        },
        "metadata": {
            "recommended_units": 1.85,
            "win_prob": 0.63,
            "edge": 1.4,
            "sizing_tag": "CHAOS_BIG_BOOST",
        },
    }

    print(build_sync_payload([sample_execution]))
