from DataValidator import validate_dataset
from datetime import datetime
import json
import os
import argparse
import uuid
from typing import Any, Dict, List, Optional, Tuple

BANNER = """
====================================================
 SharpEdge LiveFlow + Backtest Controller (v1.0)
====================================================
"""

DEFAULT_LOG_DIR = "logs"
DEFAULT_OUTPUT_DIR = "output"

# --------- Utilities --------- #

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def timestamp() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def load_json(path: str) -> Any:
    with open(path, "r") as f:
        return json.load(f)

def save_json(path: str, data: Any) -> None:
    ensure_dir(os.path.dirname(path))
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def try_import_sim_engine():
    """
    Attempts to import user's simulation engine(s).
    We try several known filenames from the project and provide a minimal stub if none are found.
    """
    engine = None
    errors = []
    candidates = [
        "mlb_prop_simulator",          # user's main simulator
        "simulate_ev_edges",           # EV edge simulator
        "live_edge_alert_system",      # live alert system
        "Download mlb_model_v1_1_5_alpha"  # legacy filename with spaces
    ]
    for name in candidates:
        try:
            engine = __import__(name)
            return engine, None
        except Exception as e:
            errors.append(f"{name}: {e}")

    # Fallback stub so the pipeline still runs
    class StubEngine:
        def run_simulation(self, games: List[Dict[str, Any]], mode: str = "liveflow", overlays: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
            results = []
            for g in games:
                gid = g.get("game_id") or f"{g.get('team_1','?')}_vs_{g.get('team_2','?')}"
                results.append({
                    "game_id": gid,
                    "mode": mode,
                    "median": {"runs": 8.2, "f5_runs": 4.1},
                    "props": {"team_total_over_prob": 0.52, "team_total_under_prob": 0.48},
                    "edges": [{"market": "F5 Total Under 4.5", "edge": 0.06}],
                    "overlays_applied": list((overlays or {}).keys())
                })
            return results

    return StubEngine(), "\n".join(errors)

# --------- Validation Layer (lightweight) --------- #

REQUIRED_FIELDS = [
    "date", "team_1", "team_2",
    "score_1", "score_2",
    "odds_open_team_1", "odds_open_team_2",
    "odds_close_team_1", "odds_close_team_2",
    "line_movement", "outcome"
]

def validate_record(rec: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errs = []
    for k in REQUIRED_FIELDS:
        if k not in rec:
            errs.append(f"missing field: {k}")
    # basic checks
    try:
        if "date" in rec:
            datetime.strptime(rec["date"], "%Y-%m-%d")
    except Exception:
        errs.append(f"invalid date format: {rec.get('date')} (expected YYYY-MM-DD)")
    for s in ("score_1","score_2"):
        if s in rec and isinstance(rec[s], (int, float)) and rec[s] < 0:
            errs.append(f"{s} must be >= 0")
    if "outcome" in rec and rec["outcome"] not in (0,1):
        errs.append("outcome must be 0 or 1")
    ok = len(errs)==0
    return ok, errs

def validate_dataset(data: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    clean, bad = [], []
    for i, rec in enumerate(data, start=1):
        ok, errs = validate_record(rec)
        if ok:
            clean.append(rec)
        else:
            bad.append({"row": i, "errors": errs, "record": rec})
    return clean, bad

# --------- Overlay Loader --------- #

def load_overlays(path: Optional[str]) -> Dict[str, Any]:
    if not path: return {}
    if not os.path.exists(path): return {}
    try:
        return load_json(path)
    except Exception:
        return {}

# --------- Controller --------- #

def run_controller(
    date_str: str,
    mode: str,
    slate_path: Optional[str],
    overlays_path: Optional[str],
    out_dir: str = DEFAULT_OUTPUT_DIR,
    log_dir: str = DEFAULT_LOG_DIR,
    tag: Optional[str] = None
) -> Dict[str, Any]:

    print(BANNER)
    day_folder = os.path.join(out_dir, date_str)
    ensure_dir(day_folder)
    ensure_dir(log_dir)

    # Load slate
    if slate_path and os.path.exists(slate_path):
        raw = load_json(slate_path)
        if isinstance(raw, dict) and "games" in raw:
            games = raw["games"]
        else:
            games = raw if isinstance(raw, list) else []
    else:
        games = []

    # Validate (lightweight)
    clean, bad = validate_dataset(games)

    # Prepare overlays
    overlays = load_overlays(overlays_path)

    # Import sim engine
    engine, import_errors = try_import_sim_engine()

    # Run simulation
    if hasattr(engine, "run_simulation"):
        results = engine.run_simulation(clean, mode=mode, overlays=overlays)
    elif hasattr(engine, "main"):
        results = engine.main(clean, mode=mode, overlays=overlays)
    else:
        raise RuntimeError("No compatible simulation function found. Expected run_simulation(games, mode, overlays).")

    # Build log summary
    run_id = f"{date_str}_{mode}_{uuid.uuid4().hex[:8]}"
    summary = {
        "run_id": run_id,
        "timestamp_utc": timestamp(),
        "date": date_str,
        "mode": mode,
        "games_ingested": len(games),
        "games_valid": len(clean),
        "games_invalid": len(bad),
        "overlays_loaded": list(overlays.keys()) if overlays else [],
        "engine_import_errors": import_errors,
        "results_count": len(results)
    }

    # Write invalid report
    if bad:
        invalid_path = os.path.join(log_dir, f"{date_str}_{mode}_invalid_rows.json")
        save_json(invalid_path, bad)

    # Write per-game results + aggregate
    aggregate_edges = []
    for r in results:
        gid = r.get("game_id") or "unknown"
        game_id = gid if isinstance(gid, str) else f"{date_str}_{uuid.uuid4().hex[:6]}"
        game_path = os.path.join(day_folder, f"{game_id}_SIM_RESULT.json")
        save_json(game_path, r)
        # collect edges if present
        for e in r.get("edges", []):
            ecopy = dict(e)
            ecopy["game_id"] = game_id
            aggregate_edges.append(ecopy)

    # Aggregate summary
    agg_path = os.path.join(day_folder, f"{date_str}_{mode}_AGGREGATE.json")
    save_json(agg_path, {
        "summary": summary,
        "aggregate_edges": aggregate_edges
    })

    print(f"[OK] Results written to: {day_folder}")
    if bad:
        print(f"[WARN] Invalid rows logged: {os.path.join(log_dir, f'{date_str}_{mode}_invalid_rows.json')}")

    return {
        "output_dir": day_folder,
        "aggregate_file": agg_path,
        "invalid_file": os.path.join(log_dir, f"{date_str}_{mode}_invalid_rows.json") if bad else None,
        "summary": summary
    }

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="SharpEdge LiveFlow + Backtest unified runner")
    p.add_argument("--date", required=False, default=datetime.utcnow().strftime("%Y-%m-%d"), help="Slate date (YYYY-MM-DD)")
    p.add_argument("--mode", required=False, default="both", choices=["liveflow","backtest","both"], help="Execution mode")
    p.add_argument("--slate", required=False, help="Path to slate JSON (list of games or {'games': [...]})")
    p.add_argument("--overlays", required=False, help="Path to volatility overlays JSON")
    p.add_argument("--out", required=False, default=DEFAULT_OUTPUT_DIR, help="Output dir")
    p.add_argument("--logs", required=False, default=DEFAULT_LOG_DIR, help="Log dir")
    p.add_argument("--tag", required=False, help="Optional tag for this run")
    return p.parse_args(argv)

def cli():
    args = parse_args()
    date_str = args.date
    ensure_dir(args.out)
    ensure_dir(args.logs)

    if args.mode in ("liveflow", "both"):
        run_controller(date_str=date_str, mode="liveflow", slate_path=args.slate, overlays_path=args.overlays, out_dir=args.out, log_dir=args.logs, tag=args.tag)

    if args.mode in ("backtest", "both"):
        run_controller(date_str=date_str, mode="backtest", slate_path=args.slate, overlays_path=args.overlays, out_dir=args.out, log_dir=args.logs, tag=args.tag)

if __name__ == "__main__":
    cli()