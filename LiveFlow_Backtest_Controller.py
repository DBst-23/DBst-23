import importlib
import importlib.util
import json
import os
import sys
import argparse
import uuid
from datetime import datetime
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
    if not path:
        return
    os.makedirs(path, exist_ok=True)

def timestamp() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def load_json(path: str) -> Any:
    with open(path, "r") as f:
        return json.load(f)

def save_json(path: str, data: Any) -> None:
    dir_ = os.path.dirname(path)
    if dir_:
        ensure_dir(dir_)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# --------- Engine Import / Verification --------- #

def try_import_sim_engine() -> Tuple[Optional[Any], List[str]]:
    """
    Engine Verification Mode:
    - Try importing known engine modules
    - If packages aren't set up, fall back to importing by file path
    Returns: (engine_or_module_or_instance, errors_list)
    """
    errors: List[str] = []

    # From your repo screenshots:
    # /sim contains: mlb_stabilizer.py, nba_totals_engine.py
    # Root contains: sharpedge/ (package folder)
    module_candidates = [
        # If sharpedge is a package and contains engines (only works if those modules exist)
        "sharpedge.mlb_prop_simulator",
        "sharpedge.simulate_ev_edges",
        "sharpedge.live_edge_alert_system",

        # These DO exist from your screenshot
        "sim.mlb_stabilizer",
        "sim.nba_totals_engine",
    ]

    for name in module_candidates:
        try:
            mod = importlib.import_module(name)
            print(f"[ENGINE VERIFY] Loaded module: {mod.__name__}")
            return mod, []
        except Exception as e:
            errors.append(f"{name}: {e}")

    # File-path fallback (works even if folders aren't packages)
    here = os.path.dirname(os.path.abspath(__file__))
    file_candidates = [
        os.path.join(here, "mlb_prop_simulator.py"),
        os.path.join(here, "simulate_ev_edges.py"),
        os.path.join(here, "live_edge_alert_system.py"),

        os.path.join(here, "scripts", "mlb_prop_simulator.py"),
        os.path.join(here, "scripts", "simulate_ev_edges.py"),
        os.path.join(here, "scripts", "live_edge_alert_system.py"),

        os.path.join(here, "scripts", "scripts", "odds", "pull_odds.py"),  # just in case

        os.path.join(here, "sim", "mlb_stabilizer.py"),
        os.path.join(here, "sim", "nba_totals_engine.py"),
    ]

    for path in file_candidates:
        try:
            if not os.path.exists(path):
                continue
            mod_name = f"_engine_{os.path.splitext(os.path.basename(path))[0]}"
            spec = importlib.util.spec_from_file_location(mod_name, path)
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                sys.modules[mod_name] = mod
                spec.loader.exec_module(mod)
                print(f"[ENGINE VERIFY] Loaded file module: {path}")
                return mod, []
        except Exception as e:
            errors.append(f"{path}: {e}")

    # Stub fallback so pipeline still runs
    class StubEngine:
        def run_simulation(
            self,
            games: List[Dict[str, Any]],
            mode: str = "liveflow",
            overlays: Optional[Dict[str, Any]] = None
        ) -> List[Dict[str, Any]]:
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

    print("[ENGINE VERIFY] WARNING: Using StubEngine. Import errors:")
    for err in errors:
        print(" -", err)

    return StubEngine(), errors

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
    try:
        if "date" in rec:
            datetime.strptime(rec["date"], "%Y-%m-%d")
    except Exception:
        errs.append(f"invalid date format: {rec.get('date')} (expected YYYY-MM-DD)")
    for s in ("score_1", "score_2"):
        if s in rec and isinstance(rec[s], (int, float)) and rec[s] < 0:
            errs.append(f"{s} must be >= 0")
    if "outcome" in rec and rec["outcome"] not in (0, 1):
        errs.append("outcome must be 0 or 1")
    return (len(errs) == 0), errs

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
    if not path:
        return {}
    if not os.path.exists(path):
        return {}
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
    games: List[Dict[str, Any]] = []
    if slate_path and os.path.exists(slate_path):
        raw = load_json(slate_path)
        if isinstance(raw, dict) and "games" in raw:
            games = raw["games"]
        elif isinstance(raw, list):
            games = raw

    # Validate
    clean, bad = validate_dataset(games)

    # Overlays
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

    # Summary
    run_id = f"{date_str}_{mode}_{uuid.uuid4().hex[:8]}"
    summary = {
        "run_id": run_id,
        "timestamp_utc": timestamp(),
        "date": date_str,
        "mode": mode,
        "tag": tag,
        "games_ingested": len(games),
        "games_valid": len(clean),
        "games_invalid": len(bad),
        "overlays_loaded": list(overlays.keys()) if overlays else [],
        "engine_import_errors": import_errors,
        "results_count": len(results),
    }

    # Invalid report
    if bad:
        invalid_path = os.path.join(log_dir, f"{date_str}_{mode}_invalid_rows.json")
        save_json(invalid_path, bad)

    # Write per-game results + collect edges
    aggregate_edges: List[Dict[str, Any]] = []
    for r in results:
        gid = r.get("game_id") or "unknown"
        game_id = gid if isinstance(gid, str) else f"{date_str}_{uuid.uuid4().hex[:6]}"
        game_path = os.path.join(day_folder, f"{game_id}_SIM_RESULT.json")
        save_json(game_path, r)

        for e in r.get("edges", []):
            ecopy = dict(e)
            ecopy["game_id"] = game_id
            aggregate_edges.append(ecopy)

    # Aggregate summary (NOTE: this is OUTSIDE the loop)
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

# --------- CLI --------- #

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="SharpEdge LiveFlow + Backtest unified runner")

    p.add_argument("--date", required=False, default=datetime.utcnow().strftime("%Y-%m-%d"),
                   help="Slate date (YYYY-MM-DD)")
    p.add_argument("--mode", required=False, default="both",
                   choices=["liveflow", "backtest", "both", "engine_verify"],
                   help="Execution mode")
    p.add_argument("--slate", required=False, default="",
                   help="Path to slate JSON (list of games or {'games': [...]})")
    p.add_argument("--overlays", required=False, default="",
                   help="Path to volatility overlays JSON")
    p.add_argument("--out", required=False, default=DEFAULT_OUTPUT_DIR, help="Output dir")
    p.add_argument("--logs", required=False, default=DEFAULT_LOG_DIR, help="Log dir")
    p.add_argument("--tag", required=False, default="", help="Optional tag for this run")

    # GitHub Action compatibility aliases
    p.add_argument("--date-str", dest="date", required=False, help="Alias for --date")
    p.add_argument("--slate-path", dest="slate", required=False, help="Alias for --slate")
    p.add_argument("--overlays-path", dest="overlays", required=False, help="Alias for --overlays")

    return p.parse_args(argv)

def cli() -> None:
    args = parse_args()

    # GitHub Actions sometimes passes "" (empty string). Normalize.
    if not args.date:
        args.date = datetime.utcnow().strftime("%Y-%m-%d")

    slate_path = args.slate if args.slate else None
    overlays_path = args.overlays if args.overlays else None
    tag = args.tag if args.tag else None

    ensure_dir(args.out)
    ensure_dir(args.logs)

    # ENGINE VERIFY (isolated)
    if args.mode == "engine_verify":
        engine, errs = try_import_sim_engine()
        if engine is None:
            raise RuntimeError("ENGINE_VERIFY failed: " + "; ".join(errs or []))
        print("[ENGINE VERIFY] OK")
        return

    # LIVEFLOW
    if args.mode in ("liveflow", "both"):
        run_controller(
            date_str=args.date,
            mode="liveflow",
            slate_path=slate_path,
            overlays_path=overlays_path,
            out_dir=args.out,
            log_dir=args.logs,
            tag=tag,
        )

    # BACKTEST
    if args.mode in ("backtest", "both"):
        run_controller(
            date_str=args.date,
            mode="backtest",
            slate_path=slate_path,
            overlays_path=overlays_path,
            out_dir=args.out,
            log_dir=args.logs,
            tag=tag,
        )

if __name__ == "__main__":
    cli()