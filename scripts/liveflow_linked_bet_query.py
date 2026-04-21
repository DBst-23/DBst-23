from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


LINKED_BETS_PATH = Path("runtime/liveflow_bet_records_linked.jsonl")


@dataclass
class QueryFilters:
    result: Optional[str] = None
    confidence_tier: Optional[str] = None
    market_type: Optional[str] = None
    recommendation: Optional[str] = None
    beat_closing_line: Optional[bool] = None
    min_clv_delta: Optional[float] = None
    max_clv_delta: Optional[float] = None
    min_profit: Optional[float] = None
    max_profit: Optional[float] = None


def load_linked_records() -> List[Dict[str, Any]]:
    if not LINKED_BETS_PATH.exists():
        return []
    rows: List[Dict[str, Any]] = []
    with LINKED_BETS_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    return rows


def apply_filters(records: List[Dict[str, Any]], filters: QueryFilters) -> List[Dict[str, Any]]:
    out = records
    if filters.result:
        out = [r for r in out if str(r.get("result", "")).upper() == filters.result.upper()]
    if filters.confidence_tier:
        out = [r for r in out if str(r.get("confidence_tier", "")).upper() == filters.confidence_tier.upper()]
    if filters.market_type:
        out = [r for r in out if str(r.get("market_type", "")).lower() == filters.market_type.lower()]
    if filters.recommendation:
        out = [r for r in out if str(r.get("recommendation", "")).upper() == filters.recommendation.upper()]
    if filters.beat_closing_line is not None:
        out = [r for r in out if bool(r.get("beat_closing_line", False)) == filters.beat_closing_line]
    if filters.min_clv_delta is not None:
        out = [r for r in out if float(r.get("clv_delta", 0.0) or 0.0) >= filters.min_clv_delta]
    if filters.max_clv_delta is not None:
        out = [r for r in out if float(r.get("clv_delta", 0.0) or 0.0) <= filters.max_clv_delta]
    if filters.min_profit is not None:
        out = [r for r in out if float(r.get("profit", 0.0) or 0.0) >= filters.min_profit]
    if filters.max_profit is not None:
        out = [r for r in out if float(r.get("profit", 0.0) or 0.0) <= filters.max_profit]
    return out


def summarize(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(records)
    total_profit = round(sum(float(r.get("profit", 0.0) or 0.0) for r in records), 2)
    avg_clv = round(sum(float(r.get("clv_delta", 0.0) or 0.0) for r in records) / total, 3) if total else 0.0
    wins = sum(1 for r in records if str(r.get("result", "")).upper() == "WIN")
    losses = sum(1 for r in records if str(r.get("result", "")).upper() == "LOSS")
    return {
        "count": total,
        "wins": wins,
        "losses": losses,
        "total_profit": total_profit,
        "avg_clv_delta": avg_clv,
    }


def prompt_text(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    raw = input(f"{label}{suffix}: ").strip()
    return raw if raw else default


def prompt_float_optional(label: str) -> Optional[float]:
    raw = input(f"{label} [blank skip]: ").strip()
    return float(raw) if raw else None


def prompt_bool_optional(label: str) -> Optional[bool]:
    raw = input(f"{label} [true/false/blank]: ").strip().lower()
    if raw == "true":
        return True
    if raw == "false":
        return False
    return None


def main() -> None:
    print("=== SharpEdge Filter + Query Engine for Linked Bets ===")
    print("Examples:")
    print("- result=LOSS + min_clv_delta=0.5 → good-process losses")
    print("- result=WIN + max_clv_delta=0 → lucky wins")
    print("- confidence_tier=LOCK + result=LOSS → lock-tier failures")

    filters = QueryFilters(
        result=prompt_text("Result filter", ""),
        confidence_tier=prompt_text("Confidence tier filter", ""),
        market_type=prompt_text("Market type filter", ""),
        recommendation=prompt_text("Recommendation filter", ""),
        beat_closing_line=prompt_bool_optional("Beat closing line filter"),
        min_clv_delta=prompt_float_optional("Minimum CLV delta"),
        max_clv_delta=prompt_float_optional("Maximum CLV delta"),
        min_profit=prompt_float_optional("Minimum profit"),
        max_profit=prompt_float_optional("Maximum profit"),
    )

    records = load_linked_records()
    filtered = apply_filters(records, filters)
    summary = summarize(filtered)

    print("\n=== FILTERS ===")
    print(json.dumps(asdict(filters), indent=2))
    print("\n=== SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print("\n=== MATCHING RECORDS ===")
    print(json.dumps(filtered, indent=2))


if __name__ == "__main__":
    main()
