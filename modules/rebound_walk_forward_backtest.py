"""Leakage-free, walk-forward rebound baseline backtesting.

Input: authenticated API-Basketball normalized player-game rows enriched with
an independently verified game_date (YYYY-MM-DD) from the games schedule.
Never infer chronology from opaque game IDs. All games on the prediction date
are excluded from training. No odds, edge, or EV are fabricated.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from collections import defaultdict
from datetime import date
from pathlib import Path
from statistics import mean


def _validate(row: dict) -> dict:
    if not isinstance(row, dict) or row.get("source") != "api_basketball_v1":
        raise ValueError("Expected API-Basketball normalized player-game row")
    for key in ("game_id", "player_id", "total_rebounds"):
        val = row.get(key)
        if type(val) is not int or val < 0:
            raise ValueError(f"Invalid {key}")
    minutes = row.get("minutes")
    if type(minutes) not in (int, float) or not math.isfinite(minutes) or minutes <= 0:
        raise ValueError("Invalid minutes")
    try:
        day = date.fromisoformat(row["game_date"])
        if day.isoformat() != row["game_date"]:
            raise ValueError()
    except (KeyError, TypeError, ValueError):
        raise ValueError("Verified ISO game_date is required; game IDs are not dates")
    return row


def _poisson_probabilities(lam: float, line: float) -> tuple[float, float, float]:
    if not math.isfinite(lam) or lam < 0 or not math.isfinite(line) or line < 0:
        raise ValueError("Invalid lambda or line")
    # P(X < line), P(X = line), P(X > line), computed without random noise.
    term = math.exp(-lam)
    cumulative_under = 0.0
    push = 0.0
    k = 0
    # Typical NBA rebound rates; protect against accidental huge input.
    if lam > 200:
        raise ValueError("Unreasonable Poisson rebound rate")
    while k <= max(400, int(lam * 5 + 50)):
        if k < line:
            cumulative_under += term
        elif k == line:
            push = term
        else:
            break
        k += 1
        term *= lam / k
    under = min(1.0, max(0.0, cumulative_under))
    push = min(1.0 - under, max(0.0, push))
    return max(0.0, 1.0 - under - push), under, push


def backtest(rows: list[dict], *, line: float = 4.5, min_games: int = 3,
             window: int = 10, seed: int = 42) -> dict:
    """Walk-forward predictions; training dates strictly precede target date.

    Uses each player's last `window` completed games, with equal-game
    historical rebound mean as the Poisson rate. The seed is retained in
    metadata for reproducibility; analytic probabilities need no RNG.
    """
    if type(min_games) is not int or min_games < 1 or type(window) is not int or window < min_games:
        raise ValueError("Invalid min_games/window")
    if not math.isfinite(line) or line < 0 or line % 1 not in (0, 0.5):
        raise ValueError("Line must be nonnegative integer or half-point")
    validated = [_validate(r) for r in rows]
    seen = set()
    grouped = defaultdict(list)
    for row in validated:
        key = (row["player_id"], row["game_id"])
        if key in seen:
            raise ValueError(f"Duplicate player/game {key}")
        seen.add(key)
        grouped[row["player_id"]].append(row)

    predictions = []
    skipped = 0
    for player_id, player_rows in sorted(grouped.items()):
        player_rows.sort(key=lambda r: (r["game_date"], r["game_id"]))
        for target in player_rows:
            prior = [r for r in player_rows if r["game_date"] < target["game_date"]]
            prior = prior[-window:]
            if len(prior) < min_games:
                skipped += 1
                continue
            lam = mean(r["total_rebounds"] for r in prior)
            over, under, push = _poisson_probabilities(lam, line)
            actual = target["total_rebounds"]
            outcome = "over" if actual > line else "under" if actual < line else "push"
            # Binary Brier score for over, including pushes as non-over;
            # pushes separately reported to avoid conflating settled bets.
            brier = (over - int(actual > line)) ** 2
            predictions.append({
                "player_id": player_id,
                "player_name": target.get("player_name"),
                "game_id": target["game_id"],
                "game_date": target["game_date"],
                "training_game_ids": [r["game_id"] for r in prior],
                "training_last_date": max(r["game_date"] for r in prior),
                "training_games": len(prior),
                "projected_mean": round(lam, 6),
                "actual_rebounds": actual,
                "line": line,
                "over_probability": round(over, 8),
                "under_probability": round(under, 8),
                "push_probability": round(push, 8),
                "outcome": outcome,
                "over_brier": round(brier, 8),
            })
    settled = [p for p in predictions if p["outcome"] != "push"]
    return {
        "model": "walk_forward_historical_poisson_v1",
        "source": "api_basketball_v1",
        "line": line,
        "min_games": min_games,
        "window": window,
        "seed": seed,
        "predictions": predictions,
        "summary": {
            "predictions": len(predictions),
            "skipped_insufficient_history": skipped,
            "settled_predictions": len(settled),
            "pushes": len(predictions) - len(settled),
            "mean_absolute_error": round(mean(abs(p["projected_mean"] - p["actual_rebounds"]) for p in predictions), 6) if predictions else None,
            "over_brier_all_games": round(mean(p["over_brier"] for p in predictions), 6) if predictions else None,
            "over_brier_settled_only": round(mean(p["over_brier"] for p in settled), 6) if settled else None,
        },
        "limitations": "No market odds, EV, or claimed edge. Historical box-score-only Poisson baseline. Date provenance must be independently verified.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="JSON array of dated normalized API-Basketball records")
    parser.add_argument("--output", type=Path, default=Path("rebound_backtest_results.json"))
    parser.add_argument("--line", type=float, default=4.5)
    parser.add_argument("--min-games", type=int, default=3)
    parser.add_argument("--window", type=int, default=10)
    args = parser.parse_args()
    rows = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError("Expected JSON array")
    result = backtest(rows, line=args.line, min_games=args.min_games, window=args.window)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
