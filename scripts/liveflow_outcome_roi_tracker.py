from dataclasses import dataclass, asdict
import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List


RUNTIME_DIR = Path("runtime")
OUTCOMES_LOG_PATH = RUNTIME_DIR / "liveflow_outcomes_log.jsonl"
ROI_TRACKER_PATH = RUNTIME_DIR / "liveflow_roi_tracker_summary.json"


@dataclass
class LiveFlowOutcomeRecord:
    timestamp_utc: str
    game_label: str
    market_type: str
    bet_label: str
    result: str
    stake: float
    payout: float
    profit: float
    confidence_score: int
    confidence_tier: str
    recommended_units: str
    recommendation: str
    should_fire: bool
    closing_line: float
    live_line: float
    notes: str = ""


def ensure_runtime_dir() -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)


def append_outcome_record(record: LiveFlowOutcomeRecord) -> None:
    ensure_runtime_dir()
    with OUTCOMES_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(record)) + "\n")


def load_outcome_records() -> List[Dict[str, Any]]:
    if not OUTCOMES_LOG_PATH.exists():
        return []
    rows: List[Dict[str, Any]] = []
    with OUTCOMES_LOG_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    return rows


def compute_roi_tracker_summary(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_bets = len(records)
    wins = [r for r in records if str(r.get("result", "")).upper() == "WIN"]
    losses = [r for r in records if str(r.get("result", "")).upper() == "LOSS"]
    pushes = [r for r in records if str(r.get("result", "")).upper() == "PUSH"]

    total_staked = round(sum(float(r.get("stake", 0.0) or 0.0) for r in records), 2)
    total_payout = round(sum(float(r.get("payout", 0.0) or 0.0) for r in records), 2)
    total_profit = round(sum(float(r.get("profit", 0.0) or 0.0) for r in records), 2)

    roi = round((total_profit / total_staked) * 100.0, 2) if total_staked > 0 else 0.0
    win_rate = round((len(wins) / total_bets) * 100.0, 2) if total_bets > 0 else 0.0

    by_tier: Dict[str, Dict[str, Any]] = {}
    for tier in ["LOCK", "STRONG", "LEAN", "PASS"]:
        tier_rows = [r for r in records if str(r.get("confidence_tier", "")) == tier]
        tier_staked = sum(float(r.get("stake", 0.0) or 0.0) for r in tier_rows)
        tier_profit = sum(float(r.get("profit", 0.0) or 0.0) for r in tier_rows)
        tier_roi = round((tier_profit / tier_staked) * 100.0, 2) if tier_staked > 0 else 0.0
        by_tier[tier] = {
            "count": len(tier_rows),
            "staked": round(tier_staked, 2),
            "profit": round(tier_profit, 2),
            "roi_pct": tier_roi,
        }

    by_market: Dict[str, Dict[str, Any]] = {}
    for market in sorted({str(r.get("market_type", "unknown")) for r in records}):
        market_rows = [r for r in records if str(r.get("market_type", "")) == market]
        market_staked = sum(float(r.get("stake", 0.0) or 0.0) for r in market_rows)
        market_profit = sum(float(r.get("profit", 0.0) or 0.0) for r in market_rows)
        market_roi = round((market_profit / market_staked) * 100.0, 2) if market_staked > 0 else 0.0
        by_market[market] = {
            "count": len(market_rows),
            "staked": round(market_staked, 2),
            "profit": round(market_profit, 2),
            "roi_pct": market_roi,
        }

    return {
        "generated_at_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "total_bets": total_bets,
        "wins": len(wins),
        "losses": len(losses),
        "pushes": len(pushes),
        "win_rate_pct": win_rate,
        "total_staked": total_staked,
        "total_payout": total_payout,
        "total_profit": total_profit,
        "roi_pct": roi,
        "by_confidence_tier": by_tier,
        "by_market_type": by_market,
    }


def write_roi_tracker_summary(summary: Dict[str, Any]) -> None:
    ensure_runtime_dir()
    ROI_TRACKER_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def load_payload(payload_path: Path) -> Dict[str, Any]:
    if not payload_path.exists():
        raise FileNotFoundError(f"Payload file not found: {payload_path}")
    return json.loads(payload_path.read_text(encoding="utf-8"))


def build_outcome_record_from_payload(payload: Dict[str, Any], result: str, stake: float, payout: float, bet_label: str, notes: str) -> LiveFlowOutcomeRecord:
    odds = payload.get("odds_snapshot", {})
    auto = payload.get("auto_adjustment", {})
    confidence = payload.get("confidence_result", {})
    trigger = payload.get("trigger_result", {})

    profit = round(payout - stake, 2)

    return LiveFlowOutcomeRecord(
        timestamp_utc=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        game_label=str(odds.get("game_label", "UNKNOWN_GAME")),
        market_type=str(payload.get("market_type", "total")),
        bet_label=bet_label,
        result=result.upper(),
        stake=round(stake, 2),
        payout=round(payout, 2),
        profit=profit,
        confidence_score=int(confidence.get("confidence_score", 0) or 0),
        confidence_tier=str(confidence.get("confidence_tier", "PASS")),
        recommended_units=str(confidence.get("recommended_units", "0.00u")),
        recommendation=str(auto.get("recommendation", "NO_FIRE")),
        should_fire=bool(trigger.get("should_fire", payload.get("should_fire", False))),
        closing_line=float(odds.get("closing_total", odds.get("closing_line", 0.0)) or 0.0),
        live_line=float(odds.get("live_total", odds.get("live_line", 0.0)) or 0.0),
        notes=notes,
    )


def prompt_text(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    raw = input(f"{label}{suffix}: ").strip()
    return raw if raw else default


def prompt_float(label: str, default: float = 0.0) -> float:
    raw = input(f"{label} [{default}]: ").strip()
    return float(raw) if raw else float(default)


def main() -> None:
    print("=== SharpEdge Outcome Grading + ROI Tracker ===")
    payload_path_raw = prompt_text("Payload JSON path", "runtime/latest_liveflow_payload.json")
    payload = load_payload(Path(payload_path_raw))

    bet_label = prompt_text("Bet label", "LiveFlow bet")
    result = prompt_text("Result (WIN/LOSS/PUSH)", "WIN").upper()
    stake = prompt_float("Stake", 0.0)
    payout = prompt_float("Payout", 0.0)
    notes = prompt_text("Notes", "")

    record = build_outcome_record_from_payload(payload, result, stake, payout, bet_label, notes)
    append_outcome_record(record)

    records = load_outcome_records()
    summary = compute_roi_tracker_summary(records)
    write_roi_tracker_summary(summary)

    print("\n=== OUTCOME RECORDED ===")
    print(json.dumps(asdict(record), indent=2))
    print("\n=== ROI TRACKER SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print("\nOutcome log:", OUTCOMES_LOG_PATH)
    print("ROI tracker:", ROI_TRACKER_PATH)


if __name__ == "__main__":
    main()
