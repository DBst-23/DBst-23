from dataclasses import dataclass, asdict
import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional


RUNTIME_DIR = Path("runtime")
LINKED_BETS_PATH = RUNTIME_DIR / "liveflow_bet_records_linked.jsonl"
LINKED_SUMMARY_PATH = RUNTIME_DIR / "liveflow_bet_records_linked_summary.json"
OUTCOMES_LOG_PATH = RUNTIME_DIR / "liveflow_outcomes_log.jsonl"
CLV_LOG_PATH = RUNTIME_DIR / "liveflow_clv_log.jsonl"


@dataclass
class LinkedBetRecord:
    timestamp_utc: str
    game_label: str
    bet_label: str
    market_type: str
    confidence_score: int
    confidence_tier: str
    recommendation: str
    result: str
    stake: float
    payout: float
    profit: float
    entry_line: float
    closing_line: float
    clv_delta: float
    beat_closing_line: bool
    notes: str = ""


def ensure_runtime_dir() -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    return rows


def append_linked_record(record: LinkedBetRecord) -> None:
    ensure_runtime_dir()
    with LINKED_BETS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(record)) + "\n")


def compute_linked_summary(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(records)
    if total == 0:
        return {
            "generated_at_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "total_linked_bets": 0,
            "wins": 0,
            "losses": 0,
            "positive_clv_wins": 0,
            "positive_clv_losses": 0,
            "negative_clv_wins": 0,
            "negative_clv_losses": 0,
        }

    wins = [r for r in records if str(r.get("result", "")).upper() == "WIN"]
    losses = [r for r in records if str(r.get("result", "")).upper() == "LOSS"]

    pos_clv_wins = [r for r in wins if float(r.get("clv_delta", 0.0) or 0.0) > 0]
    pos_clv_losses = [r for r in losses if float(r.get("clv_delta", 0.0) or 0.0) > 0]
    neg_clv_wins = [r for r in wins if float(r.get("clv_delta", 0.0) or 0.0) <= 0]
    neg_clv_losses = [r for r in losses if float(r.get("clv_delta", 0.0) or 0.0) <= 0]

    return {
        "generated_at_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "total_linked_bets": total,
        "wins": len(wins),
        "losses": len(losses),
        "positive_clv_wins": len(pos_clv_wins),
        "positive_clv_losses": len(pos_clv_losses),
        "negative_clv_wins": len(neg_clv_wins),
        "negative_clv_losses": len(neg_clv_losses),
        "avg_profit": round(sum(float(r.get("profit", 0.0) or 0.0) for r in records) / total, 3),
        "avg_clv_delta": round(sum(float(r.get("clv_delta", 0.0) or 0.0) for r in records) / total, 3),
    }


def write_linked_summary(summary: Dict[str, Any]) -> None:
    ensure_runtime_dir()
    LINKED_SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def find_latest_match(rows: List[Dict[str, Any]], game_label: str, bet_label: str) -> Optional[Dict[str, Any]]:
    matches = [r for r in rows if str(r.get("game_label", "")) == game_label and str(r.get("bet_label", "")) == bet_label]
    if not matches:
        return None
    return matches[-1]


def prompt_text(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    raw = input(f"{label}{suffix}: ").strip()
    return raw if raw else default


def main() -> None:
    print("=== SharpEdge Auto-Link CLV + ROI to Each Bet Record ===")
    game_label = prompt_text("Game label")
    bet_label = prompt_text("Bet label")
    notes = prompt_text("Notes", "")

    outcomes = load_jsonl(OUTCOMES_LOG_PATH)
    clv_rows = load_jsonl(CLV_LOG_PATH)

    outcome = find_latest_match(outcomes, game_label, bet_label)
    clv = find_latest_match(clv_rows, game_label, bet_label)

    if outcome is None:
        raise ValueError(f"No outcome record found for {game_label} / {bet_label}")
    if clv is None:
        raise ValueError(f"No CLV record found for {game_label} / {bet_label}")

    linked = LinkedBetRecord(
        timestamp_utc=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        game_label=game_label,
        bet_label=bet_label,
        market_type=str(outcome.get("market_type", "unknown")),
        confidence_score=int(outcome.get("confidence_score", 0) or 0),
        confidence_tier=str(outcome.get("confidence_tier", "PASS")),
        recommendation=str(outcome.get("recommendation", "NO_FIRE")),
        result=str(outcome.get("result", "PENDING")),
        stake=float(outcome.get("stake", 0.0) or 0.0),
        payout=float(outcome.get("payout", 0.0) or 0.0),
        profit=float(outcome.get("profit", 0.0) or 0.0),
        entry_line=float(clv.get("entry_line", 0.0) or 0.0),
        closing_line=float(clv.get("closing_line", 0.0) or 0.0),
        clv_delta=float(clv.get("clv_delta", 0.0) or 0.0),
        beat_closing_line=bool(clv.get("beat_closing_line", False)),
        notes=notes,
    )

    append_linked_record(linked)

    records = load_jsonl(LINKED_BETS_PATH)
    summary = compute_linked_summary(records)
    write_linked_summary(summary)

    print("\n=== LINKED BET RECORD ===")
    print(json.dumps(asdict(linked), indent=2))
    print("\n=== LINKED SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print("\nLinked log:", LINKED_BETS_PATH)
    print("Linked summary:", LINKED_SUMMARY_PATH)


if __name__ == "__main__":
    main()
