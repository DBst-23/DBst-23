import json
from pathlib import Path
from typing import Any, Dict, List

LINKED_BETS_PATH = Path("runtime/liveflow_bet_records_linked.jsonl")
OUTPUT_PATH = Path("runtime/liveflow_middle_band_hit_rate.json")


def load_linked_bets() -> List[Dict[str, Any]]:
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


def classify_middle_records(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    middle_rows = [
        r for r in records
        if r.get("middle_band") or "middle" in str(r.get("notes", "")).lower()
    ]

    total_middle = len(middle_rows)
    if total_middle == 0:
        return {
            "total_middle_bets": 0,
            "middle_hit_rate": 0.0,
            "positive_clv_middle_rate": 0.0,
            "average_band_width": 0.0,
            "records": []
        }

    middle_hits = 0
    positive_clv_middle = 0
    band_widths: List[float] = []
    normalized_records: List[Dict[str, Any]] = []

    for row in middle_rows:
        result = str(row.get("result", "")).upper()
        clv_delta = float(row.get("clv_delta", 0.0) or 0.0)
        middle_band = row.get("middle_band") or {}
        band_width = float(middle_band.get("band_width", 0.0) or 0.0)

        if result == "WIN":
            middle_hits += 1
        if clv_delta > 0:
            positive_clv_middle += 1
        if band_width > 0:
            band_widths.append(band_width)

        normalized_records.append({
            "game_label": row.get("game_label"),
            "bet_label": row.get("bet_label"),
            "result": result,
            "profit": row.get("profit"),
            "clv_delta": clv_delta,
            "band_width": band_width,
            "confidence_tier": row.get("confidence_tier"),
        })

    return {
        "total_middle_bets": total_middle,
        "middle_hit_rate": round(middle_hits / total_middle, 4),
        "positive_clv_middle_rate": round(positive_clv_middle / total_middle, 4),
        "average_band_width": round(sum(band_widths) / len(band_widths), 4) if band_widths else 0.0,
        "records": normalized_records,
    }


def main() -> None:
    records = load_linked_bets()
    summary = classify_middle_records(records)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("=== Middle Band Auto-Learned Hit Rate ===")
    print(json.dumps(summary, indent=2))
    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
