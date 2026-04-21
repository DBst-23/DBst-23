from dataclasses import dataclass, asdict
import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List


RUNTIME_DIR = Path("runtime")
SIGNALS_LOG_PATH = RUNTIME_DIR / "liveflow_signals_log.jsonl"
EDGE_TRACKER_PATH = RUNTIME_DIR / "liveflow_edge_tracker_summary.json"


@dataclass
class LiveFlowSignalRecord:
    timestamp_utc: str
    game_label: str
    market_type: str
    sportsbook: str
    closing_line: float
    live_line: float
    confidence_score: int
    confidence_tier: str
    recommended_units: str
    recommendation: str
    should_fire: bool
    heat_index: int
    heat_action: str
    classifier_action: str
    classifier_confidence: float
    notes: str = ""


def ensure_runtime_dir() -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)


def append_signal_record(record: LiveFlowSignalRecord) -> None:
    ensure_runtime_dir()
    with SIGNALS_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(record)) + "\n")


def load_signal_records() -> List[Dict[str, Any]]:
    if not SIGNALS_LOG_PATH.exists():
        return []
    rows: List[Dict[str, Any]] = []
    with SIGNALS_LOG_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    return rows


def compute_edge_tracker_summary(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(records)
    fired = [r for r in records if r.get("should_fire") is True]
    lock = [r for r in records if r.get("confidence_tier") == "LOCK"]
    strong = [r for r in records if r.get("confidence_tier") == "STRONG"]
    team_total = [r for r in records if r.get("market_type") == "team_total"]
    total_market = [r for r in records if r.get("market_type") == "total"]
    spread = [r for r in records if r.get("market_type") == "spread"]

    avg_conf = round(sum(int(r.get("confidence_score", 0) or 0) for r in records) / total, 2) if total else 0.0
    avg_heat = round(sum(int(r.get("heat_index", 0) or 0) for r in records) / total, 2) if total else 0.0

    recommendation_counts: Dict[str, int] = {}
    for r in records:
        rec = str(r.get("recommendation", "UNKNOWN"))
        recommendation_counts[rec] = recommendation_counts.get(rec, 0) + 1

    summary = {
        "generated_at_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "total_signals": total,
        "signals_fired": len(fired),
        "lock_count": len(lock),
        "strong_count": len(strong),
        "market_type_counts": {
            "team_total": len(team_total),
            "total": len(total_market),
            "spread": len(spread),
        },
        "average_confidence_score": avg_conf,
        "average_heat_index": avg_heat,
        "recommendation_counts": recommendation_counts,
    }
    return summary


def write_edge_tracker_summary(summary: Dict[str, Any]) -> None:
    ensure_runtime_dir()
    EDGE_TRACKER_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def build_record_from_payload(payload: Dict[str, Any]) -> LiveFlowSignalRecord:
    odds = payload.get("odds_snapshot", {})
    heat = payload.get("heat_result", {})
    classifier = payload.get("classifier_result", {})
    auto = payload.get("auto_adjustment", {})
    confidence = payload.get("confidence_result", {})
    trigger = payload.get("trigger_result", {})

    return LiveFlowSignalRecord(
        timestamp_utc=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        game_label=str(odds.get("game_label", "UNKNOWN_GAME")),
        market_type=str(payload.get("market_type", "total")),
        sportsbook=str(odds.get("sportsbook", "unknown_source")),
        closing_line=float(odds.get("closing_total", odds.get("closing_line", 0.0)) or 0.0),
        live_line=float(odds.get("live_total", odds.get("live_line", 0.0)) or 0.0),
        confidence_score=int(confidence.get("confidence_score", 0) or 0),
        confidence_tier=str(confidence.get("confidence_tier", "PASS")),
        recommended_units=str(confidence.get("recommended_units", "0.00u")),
        recommendation=str(auto.get("recommendation", "NO_FIRE")),
        should_fire=bool(trigger.get("should_fire", payload.get("should_fire", False))),
        heat_index=int(heat.get("heat_index", 0) or 0),
        heat_action=str(heat.get("action_tag", "NO_EDGE")),
        classifier_action=str(classifier.get("action_bias", "NO_FIRE")),
        classifier_confidence=float(classifier.get("confidence", 0.0) or 0.0),
        notes=str(odds.get("notes", "")),
    )


def prompt_payload_path() -> Path:
    raw = input("Payload JSON path [runtime/latest_liveflow_payload.json]: ").strip()
    return Path(raw) if raw else Path("runtime/latest_liveflow_payload.json")


def main() -> None:
    print("=== SharpEdge Persistent Logging + Edge Tracker ===")
    payload_path = prompt_payload_path()
    if not payload_path.exists():
        raise FileNotFoundError(f"Payload file not found: {payload_path}")

    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    record = build_record_from_payload(payload)
    append_signal_record(record)

    records = load_signal_records()
    summary = compute_edge_tracker_summary(records)
    write_edge_tracker_summary(summary)

    print("\n=== LOGGED RECORD ===")
    print(json.dumps(asdict(record), indent=2))
    print("\n=== EDGE TRACKER SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print("\nSignals log:", SIGNALS_LOG_PATH)
    print("Edge tracker:", EDGE_TRACKER_PATH)


if __name__ == "__main__":
    main()
