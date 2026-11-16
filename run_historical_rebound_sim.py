"""Reproducible historical NBA rebound simulation from observed API-Basketball rows.

Input must contain real normalized player-game records. No fabricated rebound chances,
sportsbook odds, player identities, or game chronology.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from collections import Counter
from pathlib import Path
from statistics import mean, median

from modules.api_basketball_rebounds import fetch_player_game_stats, normalize_player_rebounds


def collect(game_ids: list[int]) -> list[dict]:
    rows = []
    for game_id in game_ids:
        fetched = normalize_player_rebounds(fetch_player_game_stats(game_id=game_id))
        if not fetched:
            raise ValueError(f"Game {game_id} returned no normalized player rebounds")
        rows.extend(fetched)
    return rows


def simulate(rows: list[dict], player_id: int, line: float, seed: int = 42,
             iterations: int = 10000, min_games: int = 3) -> dict:
    if iterations < 1 or min_games < 1 or not math.isfinite(line) or line < 0:
        raise ValueError("Invalid iterations, min_games, or rebound line")
    selected = [r for r in rows if r.get("player_id") == player_id]
    if any(r.get("source") != "api_basketball_v1" for r in selected):
        raise ValueError("Expected authenticated API-Basketball normalized records")
    by_game = {}
    for r in selected:
        game_id = r.get("game_id")
        rebounds = r.get("total_rebounds")
        minutes = r.get("minutes")
        if (not isinstance(game_id, int) or isinstance(game_id, bool)
                or not isinstance(rebounds, int) or isinstance(rebounds, bool)
                or rebounds < 0 or not isinstance(minutes, (int, float))
                or not math.isfinite(minutes) or minutes <= 0):
            raise ValueError("Invalid player-game record")
        if game_id in by_game:
            raise ValueError(f"Duplicate player-game record: {game_id}")
        by_game[game_id] = r
    if len(by_game) < min_games:
        raise ValueError(f"Only {len(by_game)} distinct games; need {min_games}")
    # Historical rows must be supplied from games strictly BEFORE the target game.
    # No inferred chronological order from opaque game IDs.
    records = [by_game[k] for k in sorted(by_game)]
    observed = [r["total_rebounds"] for r in records]
    minutes = [float(r["minutes"]) for r in records]
    # Exposure-weighted rebounds/minute, scaled to observed mean minutes.
    # This is a simple Poisson baseline, NOT rebound-chance tracking.
    projected_minutes = mean(minutes)
    rate = sum(observed) / sum(minutes)
    lam = rate * projected_minutes
    rng = random.Random(seed)
    samples = []
    for _ in range(iterations):
        # Exact Poisson via inverse CDF; avoids overflow for typical NBA rebound rates.
        u = rng.random()
        p = math.exp(-lam)
        cumulative = p
        n = 0
        while u > cumulative:
            n += 1
            p *= lam / n
            cumulative += p
        samples.append(n)
    counts = Counter(samples)
    over = sum(v for k, v in counts.items() if k > line) / iterations
    under = sum(v for k, v in counts.items() if k < line) / iterations
    push = sum(v for k, v in counts.items() if k == line) / iterations
    result = {
        "model": "historical_poisson_baseline_v1",
        "source": "api_basketball_v1",
        "player_id": player_id,
        "player_name": records[0].get("player_name"),
        "historical_game_ids": sorted(by_game),
        "historical_games": len(records),
        "historical_mean_rebounds": mean(observed),
        "projected_minutes": round(projected_minutes, 4),
        "lambda": round(lam, 6),
        "line": line,
        "iterations": iterations,
        "seed": seed,
        "mean": round(mean(samples), 4),
        "median": median(samples),
        "over_probability": round(over, 6),
        "under_probability": round(under, 6),
        "push_probability": round(push, 6),
        "distribution": {str(k): round(v / iterations, 6) for k, v in sorted(counts.items())},
        "fair_over_decimal_no_push": round(1 / over, 4) if over > 0 and push == 0 else None,
        "fair_under_decimal_no_push": round(1 / under, 4) if under > 0 and push == 0 else None,
        "edge": None,
        "ev": None,
        "notes": "Historical baseline only. No sportsbook odds or rebound-chance data. Historical game IDs must precede prediction target.",
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--game-ids", nargs="*", type=int, default=[])
    parser.add_argument("--input", type=Path)
    parser.add_argument("--snapshot", type=Path, default=Path("historical_rebounds_snapshot.json"))
    parser.add_argument("--output", type=Path, default=Path("historical_rebound_simulation.json"))
    parser.add_argument("--player-id", type=int, required=True)
    parser.add_argument("--line", type=float, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--iterations", type=int, default=10000)
    args = parser.parse_args()
    if bool(args.game_ids) == bool(args.input):
        parser.error("Supply exactly one of --game-ids (live API) or --input (saved snapshot)")
    if args.game_ids:
        rows = collect(args.game_ids)
        args.snapshot.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n")
    else:
        rows = json.loads(args.input.read_text())
        if not isinstance(rows, list):
            raise ValueError("Snapshot must be a JSON array")
    output = simulate(rows, args.player_id, args.line, args.seed, args.iterations)
    snapshot_bytes = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    output["input_sha256"] = hashlib.sha256(snapshot_bytes).hexdigest()
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: output[k] for k in ("player_name", "historical_games", "mean",
                    "median", "over_probability", "under_probability", "push_probability",
                    "input_sha256")}, indent=2))


if __name__ == "__main__":
    main()
