from __future__ import annotations

from typing import Any, Dict, List
from collections import Counter, defaultdict


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default



def safe_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(value)
    except (TypeError, ValueError):
        return default



def normalize_result(result: str) -> str:
    result = str(result or "").strip().upper()
    if result in {"WIN", "WON", "HIT", "WIN_WITH_PUSH"}:
        return "WIN"
    if result in {"LOSS", "LOSE", "MISS"}:
        return "LOSS"
    if result in {"PUSH", "VOID"}:
        return "PUSH"
    return "UNKNOWN"



def summarize_settled_bets(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_staked = 0.0
    total_return = 0.0
    total_profit = 0.0
    result_counts = Counter()
    market_counter = Counter()
    mode_counter = Counter()
    book_counter = Counter()
    clv_values: List[float] = []
    edge_values: List[float] = []
    win_probs: List[float] = []

    for record in records:
        stake = safe_float(record.get("stake", record.get("filled_stake", 0.0)))
        ret = safe_float(record.get("return_actual", 0.0))
        profit = ret - stake if ret or stake else safe_float(record.get("profit", 0.0))

        total_staked += stake
        total_return += ret
        total_profit += profit

        result_counts[normalize_result(record.get("result", "UNKNOWN"))] += 1
        market_counter[str(record.get("market", "Unknown"))] += 1
        mode_counter[str(record.get("mode", "Unknown"))] += 1
        book_counter[str(record.get("platform", record.get("book", "Unknown")))] += 1

        clv = record.get("clv_delta")
        if clv is not None:
            clv_values.append(safe_float(clv))

        metadata = record.get("metadata", {}) or {}
        edge = metadata.get("edge", record.get("edge"))
        if edge is not None:
            edge_values.append(safe_float(edge))

        win_prob = metadata.get("win_prob", record.get("win_prob"))
        if win_prob is not None:
            win_probs.append(safe_float(win_prob))

    total_bets = len(records)
    resolved = result_counts["WIN"] + result_counts["LOSS"]
    accuracy = round((result_counts["WIN"] / resolved) * 100.0, 2) if resolved else 0.0
    roi = round((total_profit / total_staked) * 100.0, 2) if total_staked else 0.0
    avg_clv = round(sum(clv_values) / len(clv_values), 2) if clv_values else 0.0
    avg_edge = round(sum(edge_values) / len(edge_values), 3) if edge_values else 0.0
    avg_win_prob = round(sum(win_probs) / len(win_probs), 3) if win_probs else 0.0

    return {
        "total_bets": total_bets,
        "wins": result_counts["WIN"],
        "losses": result_counts["LOSS"],
        "pushes": result_counts["PUSH"],
        "unknown": result_counts["UNKNOWN"],
        "accuracy_pct": accuracy,
        "total_staked": round(total_staked, 2),
        "total_return": round(total_return, 2),
        "total_profit": round(total_profit, 2),
        "roi_pct": roi,
        "avg_clv_delta": avg_clv,
        "avg_edge": avg_edge,
        "avg_win_prob": avg_win_prob,
        "markets": dict(market_counter),
        "modes": dict(mode_counter),
        "books": dict(book_counter),
    }



def build_clv_buckets(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    buckets = {
        "positive_clv": 0,
        "flat_clv": 0,
        "negative_clv": 0,
        "missing_clv": 0,
    }

    for record in records:
        clv = record.get("clv_delta")
        if clv is None:
            buckets["missing_clv"] += 1
            continue
        clv_f = safe_float(clv)
        if clv_f > 0:
            buckets["positive_clv"] += 1
        elif clv_f < 0:
            buckets["negative_clv"] += 1
        else:
            buckets["flat_clv"] += 1

    return buckets



def build_accuracy_by_market(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    market_stats: Dict[str, Dict[str, float]] = defaultdict(lambda: {"wins": 0, "losses": 0, "pushes": 0})

    for record in records:
        market = str(record.get("market", "Unknown"))
        result = normalize_result(record.get("result", "UNKNOWN"))
        if result == "WIN":
            market_stats[market]["wins"] += 1
        elif result == "LOSS":
            market_stats[market]["losses"] += 1
        elif result == "PUSH":
            market_stats[market]["pushes"] += 1

    output: Dict[str, Any] = {}
    for market, stats in market_stats.items():
        resolved = stats["wins"] + stats["losses"]
        output[market] = {
            "wins": int(stats["wins"]),
            "losses": int(stats["losses"]),
            "pushes": int(stats["pushes"]),
            "accuracy_pct": round((stats["wins"] / resolved) * 100.0, 2) if resolved else 0.0,
        }
    return output



def build_roi_by_mode(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    mode_stats: Dict[str, Dict[str, float]] = defaultdict(lambda: {"stake": 0.0, "return": 0.0})

    for record in records:
        mode = str(record.get("mode", "Unknown"))
        stake = safe_float(record.get("stake", record.get("filled_stake", 0.0)))
        ret = safe_float(record.get("return_actual", 0.0))
        mode_stats[mode]["stake"] += stake
        mode_stats[mode]["return"] += ret

    output: Dict[str, Any] = {}
    for mode, stats in mode_stats.items():
        stake = stats["stake"]
        ret = stats["return"]
        profit = ret - stake
        output[mode] = {
            "stake": round(stake, 2),
            "return": round(ret, 2),
            "profit": round(profit, 2),
            "roi_pct": round((profit / stake) * 100.0, 2) if stake else 0.0,
        }
    return output



def build_dashboard_payload(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "summary": summarize_settled_bets(records),
        "clv_buckets": build_clv_buckets(records),
        "accuracy_by_market": build_accuracy_by_market(records),
        "roi_by_mode": build_roi_by_mode(records),
    }


if __name__ == "__main__":
    sample_records = [
        {
            "result": "WIN",
            "stake": 10,
            "return_actual": 18.5,
            "market": "Rebounds",
            "mode": "Pregame",
            "platform": "Underdog",
            "clv_delta": 8,
            "metadata": {"edge": 1.4, "win_prob": 0.63},
        },
        {
            "result": "LOSS",
            "stake": 10,
            "return_actual": 0,
            "market": "Rebounds",
            "mode": "LiveFlow",
            "platform": "Underdog",
            "clv_delta": -4,
            "metadata": {"edge": 0.7, "win_prob": 0.56},
        },
        {
            "result": "PUSH",
            "stake": 10,
            "return_actual": 10,
            "market": "Rebounds",
            "mode": "Pregame",
            "platform": "Underdog",
            "clv_delta": 0,
            "metadata": {"edge": 0.0, "win_prob": 0.5},
        },
    ]
    print(build_dashboard_payload(sample_records))
