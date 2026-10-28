"""Only write to strict accuracy cohort through this fail-closed gateway."""
import argparse
import json
import os
import tempfile
from pathlib import Path
from liveflow.nba.sync_gate import evaluate

STRICT_PATH = Path("analytics/liveflow_master/nba_halftime_strict_accuracy_v1.json")

def append_checkpoint(freeze_path, market_path, registry_path=STRICT_PATH):
    freeze_path, market_path, registry_path = map(Path, (freeze_path, market_path, registry_path))
    # Source JSON must already have been durably captured before this process.
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    market = json.loads(market_path.read_text(encoding="utf-8"))
    verdict = evaluate(freeze, market)
    if verdict["status"] != "PASS":
        raise ValueError("Strict accuracy admission denied: " + "; ".join(verdict["reasons"]))
    if registry_path.exists():
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    else:
        registry = {"schema_version": "strict_v1", "cohort": "premarket_regulation_only", "games": []}
    if registry.get("schema_version") != "strict_v1" or not isinstance(registry.get("games"), list):
        raise ValueError("Registry schema incompatible: refusing to modify")
    game_id = freeze["game_id"]
    if any(row.get("game_id") == game_id for row in registry["games"]):
        raise ValueError("Duplicate game_id: strict cohort allows only one halftime checkpoint per game")
    record = {"game_id": game_id, "checkpoint": "HALFTIME", "freeze": freeze,
              "market": market, "gate": verdict}
    registry["games"].append(record)
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".strict-", dir=str(registry_path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, registry_path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    return verdict

def main():
    parser = argparse.ArgumentParser(description="Strict NBA LIVE-FLOW registry admission")
    parser.add_argument("--freeze", required=True)
    parser.add_argument("--market", required=True)
    parser.add_argument("--registry", default=str(STRICT_PATH))
    args = parser.parse_args()
    verdict = append_checkpoint(args.freeze, args.market, args.registry)
    print(json.dumps(verdict, indent=2))

if __name__ == "__main__":
    main()
