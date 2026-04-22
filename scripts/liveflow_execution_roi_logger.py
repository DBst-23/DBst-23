import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict

RUNTIME_DIR = Path("runtime")
EXECUTION_LOG_PATH = RUNTIME_DIR / "liveflow_execution_slips_log.jsonl"
LATEST_PAYLOAD_PATH = RUNTIME_DIR / "latest_liveflow_payload.json"
OUTCOMES_LOG_PATH = RUNTIME_DIR / "liveflow_outcomes_log.jsonl"
ROI_TRACKER_PATH = RUNTIME_DIR / "liveflow_roi_tracker_summary.json"


def ensure_runtime_dir() -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)


def load_payload(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Payload file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    ensure_runtime_dir()
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


def load_jsonl(path: Path) -> list[Dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
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


def compute_roi_summary(records: list[Dict[str, Any]]) -> Dict[str, Any]:
    total_bets = len(records)
    wins = [r for r in records if str(r.get("result", "")).upper() == "WIN"]
    losses = [r for r in records if str(r.get("result", "")).upper() == "LOSS"]
    pushes = [r for r in records if str(r.get("result", "")).upper() == "PUSH"]

    total_staked = round(sum(float(r.get("stake", 0.0) or 0.0) for r in records), 2)
    total_payout = round(sum(float(r.get("payout", 0.0) or 0.0) for r in records), 2)
    total_profit = round(sum(float(r.get("profit", 0.0) or 0.0) for r in records), 2)
    roi = round((total_profit / total_staked) * 100.0, 2) if total_staked > 0 else 0.0
    win_rate = round((len(wins) / total_bets) * 100.0, 2) if total_bets > 0 else 0.0

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
    }


def prompt_text(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    raw = input(f"{label}{suffix}: ").strip()
    return raw if raw else default


def prompt_float(label: str, default: float = 0.0) -> float:
    raw = input(f"{label} [{default}]: ").strip()
    return float(raw) if raw else float(default)


def main() -> None:
    print("=== SharpEdge Auto-Log Execution Slips + Outcomes into ROI Tracker ===")
    payload_path = Path(prompt_text("Payload JSON path", str(LATEST_PAYLOAD_PATH)))
    payload = load_payload(payload_path)

    slip = payload.get("execution_slip", {})
    if not slip:
        raise ValueError("No execution_slip found in payload.")

    execution_row = {
        "timestamp_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "game_label": slip.get("game_label", payload.get("odds_snapshot", {}).get("game_label", "UNKNOWN_GAME")),
        "market_type": slip.get("market_type", payload.get("market_type", "unknown")),
        "side": slip.get("side", "UNKNOWN"),
        "line": slip.get("line", 0.0),
        "confidence_tier": slip.get("confidence_tier", "PASS"),
        "confidence_score": slip.get("confidence_score", 0),
        "recommended_total_stake": slip.get("recommended_total_stake", 0.0),
        "recommended_each_leg": slip.get("recommended_each_leg", 0.0),
        "ticket_type": slip.get("ticket_type", "single_leg"),
        "should_fire": bool(slip.get("should_fire", False)),
        "middle_band": slip.get("middle_band"),
        "notes": slip.get("notes", []),
    }
    append_jsonl(EXECUTION_LOG_PATH, execution_row)

    result = prompt_text("Result (WIN/LOSS/PUSH)", "WIN").upper()
    payout = prompt_float("Payout", 0.0)
    notes = prompt_text("Outcome notes", "")
    stake = float(slip.get("recommended_total_stake", 0.0) or 0.0)
    profit = round(payout - stake, 2)

    outcome_row = {
        "timestamp_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "game_label": execution_row["game_label"],
        "market_type": execution_row["market_type"],
        "bet_label": f"{execution_row['side']} {execution_row['line']}",
        "result": result,
        "stake": round(stake, 2),
        "payout": round(payout, 2),
        "profit": profit,
        "confidence_score": execution_row["confidence_score"],
        "confidence_tier": execution_row["confidence_tier"],
        "recommended_units": str(stake),
        "recommendation": payload.get("auto_adjustment", {}).get("recommendation", "NO_FIRE"),
        "should_fire": execution_row["should_fire"],
        "closing_line": float(payload.get("odds_snapshot", {}).get("closing_total", payload.get("odds_snapshot", {}).get("closing_line", 0.0)) or 0.0),
        "live_line": float(execution_row["line"] or 0.0),
        "middle_band": execution_row.get("middle_band"),
        "notes": notes,
    }
    append_jsonl(OUTCOMES_LOG_PATH, outcome_row)

    roi_records = load_jsonl(OUTCOMES_LOG_PATH)
    roi_summary = compute_roi_summary(roi_records)
    ROI_TRACKER_PATH.write_text(json.dumps(roi_summary, indent=2), encoding="utf-8")

    print("\n=== EXECUTION LOGGED ===")
    print(json.dumps(execution_row, indent=2))
    print("\n=== OUTCOME LOGGED ===")
    print(json.dumps(outcome_row, indent=2))
    print("\n=== ROI SUMMARY ===")
    print(json.dumps(roi_summary, indent=2))
    print(f"\nExecution log: {EXECUTION_LOG_PATH}")
    print(f"Outcome log: {OUTCOMES_LOG_PATH}")
    print(f"ROI tracker: {ROI_TRACKER_PATH}")


if __name__ == "__main__":
    main()
