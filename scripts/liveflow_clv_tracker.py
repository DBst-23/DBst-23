from dataclasses import dataclass, asdict
import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List


RUNTIME_DIR = Path("runtime")
CLV_LOG_PATH = RUNTIME_DIR / "liveflow_clv_log.jsonl"
CLV_SUMMARY_PATH = RUNTIME_DIR / "liveflow_clv_summary.json"


@dataclass
class LiveFlowCLVRecord:
    timestamp_utc: str
    game_label: str
    market_type: str
    bet_label: str
    side: str
    entry_line: float
    closing_line: float
    clv_delta: float
    beat_closing_line: bool
    confidence_score: int
    confidence_tier: str
    recommendation: str
    result: str = "PENDING"
    notes: str = ""


def ensure_runtime_dir() -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)


def append_clv_record(record: LiveFlowCLVRecord) -> None:
    ensure_runtime_dir()
    with CLV_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(record)) + "\n")


def load_clv_records() -> List[Dict[str, Any]]:
    if not CLV_LOG_PATH.exists():
        return []
    rows: List[Dict[str, Any]] = []
    with CLV_LOG_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    return rows


def compute_clv_summary(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(records)
    if total == 0:
        return {
            "generated_at_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "total_tracked": 0,
            "avg_clv_delta": 0.0,
            "beat_closing_count": 0,
            "beat_closing_rate_pct": 0.0,
            "by_market_type": {},
        }

    avg_clv = round(sum(float(r.get("clv_delta", 0.0) or 0.0) for r in records) / total, 3)
    beat_count = sum(1 for r in records if bool(r.get("beat_closing_line", False)))
    beat_rate = round((beat_count / total) * 100.0, 2)

    by_market: Dict[str, Dict[str, Any]] = {}
    market_types = sorted({str(r.get("market_type", "unknown")) for r in records})
    for market in market_types:
        rows = [r for r in records if str(r.get("market_type", "")) == market]
        m_total = len(rows)
        m_avg = round(sum(float(r.get("clv_delta", 0.0) or 0.0) for r in rows) / m_total, 3) if m_total else 0.0
        m_beat = sum(1 for r in rows if bool(r.get("beat_closing_line", False)))
        by_market[market] = {
            "count": m_total,
            "avg_clv_delta": m_avg,
            "beat_closing_rate_pct": round((m_beat / m_total) * 100.0, 2) if m_total else 0.0,
        }

    return {
        "generated_at_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "total_tracked": total,
        "avg_clv_delta": avg_clv,
        "beat_closing_count": beat_count,
        "beat_closing_rate_pct": beat_rate,
        "by_market_type": by_market,
    }


def write_clv_summary(summary: Dict[str, Any]) -> None:
    ensure_runtime_dir()
    CLV_SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def build_clv_record(payload: Dict[str, Any], bet_label: str, side: str, entry_line: float, closing_line: float, notes: str) -> LiveFlowCLVRecord:
    odds = payload.get("odds_snapshot", {})
    confidence = payload.get("confidence_result", {})
    auto = payload.get("auto_adjustment", {})

    side_norm = side.upper()
    if side_norm in {"UNDER", "NO"}:
        clv_delta = round(closing_line - entry_line, 3)
        beat = closing_line > entry_line
    elif side_norm in {"OVER", "YES"}:
        clv_delta = round(entry_line - closing_line, 3)
        beat = closing_line < entry_line
    else:
        clv_delta = round(entry_line - closing_line, 3)
        beat = clv_delta > 0

    return LiveFlowCLVRecord(
        timestamp_utc=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        game_label=str(odds.get("game_label", "UNKNOWN_GAME")),
        market_type=str(payload.get("market_type", "total")),
        bet_label=bet_label,
        side=side_norm,
        entry_line=entry_line,
        closing_line=closing_line,
        clv_delta=clv_delta,
        beat_closing_line=beat,
        confidence_score=int(confidence.get("confidence_score", 0) or 0),
        confidence_tier=str(confidence.get("confidence_tier", "PASS")),
        recommendation=str(auto.get("recommendation", "NO_FIRE")),
        notes=notes,
    )


def prompt_text(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    raw = input(f"{label}{suffix}: ").strip()
    return raw if raw else default


def prompt_float(label: str, default: float = 0.0) -> float:
    raw = input(f"{label} [{default}]: ").strip()
    return float(raw) if raw else float(default)


def load_payload(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Payload file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    print("=== SharpEdge CLV Tracker + Closing Line Comparison ===")
    payload_path = Path(prompt_text("Payload JSON path", "runtime/latest_liveflow_payload.json"))
    payload = load_payload(payload_path)

    bet_label = prompt_text("Bet label", "LiveFlow bet")
    side = prompt_text("Side (UNDER/OVER or NO/YES)", "UNDER")
    entry_line = prompt_float("Entry line", 0.0)
    closing_line = prompt_float("Closing line", 0.0)
    notes = prompt_text("Notes", "")

    record = build_clv_record(payload, bet_label, side, entry_line, closing_line, notes)
    append_clv_record(record)

    records = load_clv_records()
    summary = compute_clv_summary(records)
    write_clv_summary(summary)

    print("\n=== CLV RECORD ===")
    print(json.dumps(asdict(record), indent=2))
    print("\n=== CLV SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print("\nCLV log:", CLV_LOG_PATH)
    print("CLV summary:", CLV_SUMMARY_PATH)


if __name__ == "__main__":
    main()
