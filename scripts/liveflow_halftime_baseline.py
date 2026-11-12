"""Chronological halftime baseline for second-half outcomes and final winner.

Train the regression on 2022, calibrate its residual distribution on 2023,
and evaluate once on untouched 2024 games. No market odds are used.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
from statistics import mean, median

FEATURES = ("halftime_margin_home", "halftime_total", "home_q2",
            "away_q2", "home_q1", "away_q1")
TARGETS = ("second_half_margin_home", "second_half_total")


def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    n = len(vector)
    a = [matrix[i][:] + [vector[i]] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda i: abs(a[i][col]))
        if abs(a[pivot][col]) < 1e-10:
            raise ValueError("Singular training matrix")
        a[col], a[pivot] = a[pivot], a[col]
        factor = a[col][col]
        a[col] = [v / factor for v in a[col]]
        for row in range(n):
            if row == col:
                continue
            factor = a[row][col]
            a[row] = [a[row][j] - factor * a[col][j] for j in range(n + 1)]
    return [a[i][-1] for i in range(n)]


def fit(rows: list[dict], target: str) -> tuple[list[float], list[float], list[float]]:
    # Scale based on training rows only; keep the intercept unpenalized.
    columns = [[float(row[f]) for row in rows] for f in FEATURES]
    centers = [mean(col) for col in columns]
    scales = [math.sqrt(mean([(v - c) ** 2 for v in col])) or 1.0
              for col, c in zip(columns, centers)]
    n = len(FEATURES) + 1
    gram = [[0.0] * n for _ in range(n)]
    rhs = [0.0] * n
    for row in rows:
        x = [1.0] + [(float(row[f]) - centers[j]) / scales[j]
                     for j, f in enumerate(FEATURES)]
        y = float(row[target])
        for i in range(n):
            rhs[i] += x[i] * y
            for j in range(n):
                gram[i][j] += x[i] * x[j]
    for i in range(1, n):
        gram[i][i] += 1.0  # weak ridge penalty, fixed before holdout
    return solve(gram, rhs), centers, scales


def predict(model: tuple[list[float], list[float], list[float]], row: dict) -> float:
    coef, centers, scales = model
    return coef[0] + sum(coef[j + 1] * (float(row[f]) - centers[j]) / scales[j]
                         for j, f in enumerate(FEATURES))


def error_metrics(actual: list[float], predicted: list[float]) -> dict:
    residuals = [a - p for a, p in zip(actual, predicted)]
    return {"mae": round(mean(abs(x) for x in residuals), 4),
            "rmse": round(math.sqrt(mean(x * x for x in residuals)), 4),
            "bias_actual_minus_predicted": round(mean(residuals), 4)}


def probability_home_win(predicted_final_margin: float, residuals: list[float]) -> float:
    # Empirical distribution from validation year only. +1 smoothing.
    # Half a point continuity correction approximates the integer margin threshold.
    count = sum(predicted_final_margin + error > 0.5 for error in residuals)
    return (count + 0.5) / (len(residuals) + 1)


def evaluate(rows: list[dict]) -> dict:
    by_season = defaultdict(list)
    seen = set()
    for row in rows:
        required = set(FEATURES) | set(TARGETS) | {"game_id", "season",
                                                  "final_home", "final_away"}
        if not required.issubset(row):
            raise ValueError("Missing required halftime or outcome fields")
        if row["game_id"] in seen:
            raise ValueError("Duplicate game ID")
        seen.add(row["game_id"])
        by_season[int(row["season"])].append(row)
    if any(len(by_season[year]) < 100 for year in (2022, 2023, 2024)):
        raise ValueError("Insufficient data for chronological seasons")

    train, validation, test = (by_season[year] for year in (2022, 2023, 2024))
    models = {target: fit(train, target) for target in TARGETS}
    val_residuals = {target: [float(r[target]) - predict(models[target], r)
                               for r in validation] for target in TARGETS}
    metrics = {}
    for target in TARGETS:
        actual = [float(r[target]) for r in test]
        predicted = [predict(models[target], r) for r in test]
        naive = (0.0 if target == "second_half_margin_home"
                 else mean(float(r[target]) for r in train))
        metrics[target] = {
            "model": error_metrics(actual, predicted),
            "naive_baseline": error_metrics(actual, [naive] * len(test)),
            "validation_residual_mean": round(mean(val_residuals[target]), 4),
            "validation_residual_median": round(median(val_residuals[target]), 4),
        }

    bins = [{"count": 0, "probability_sum": 0.0, "outcomes": 0}
            for _ in range(5)]
    brier_sum, log_loss_sum = 0.0, 0.0
    naive_brier_sum, naive_log_loss_sum = 0.0, 0.0
    naive_residuals = [float(r["second_half_margin_home"]) for r in validation]
    for row in test:
        margin = float(row["halftime_margin_home"]) + predict(
            models["second_half_margin_home"], row)
        p = probability_home_win(margin, val_residuals["second_half_margin_home"])
        naive_p = probability_home_win(
            float(row["halftime_margin_home"]), naive_residuals)
        result = int(float(row["final_home"]) > float(row["final_away"]))
        brier_sum += (p - result) ** 2
        log_loss_sum -= result * math.log(p) + (1 - result) * math.log1p(-p)
        naive_brier_sum += (naive_p - result) ** 2
        naive_log_loss_sum -= result * math.log(naive_p) + (
            1 - result) * math.log1p(-naive_p)
        index = min(int(p * 5), 4)
        bins[index]["count"] += 1
        bins[index]["probability_sum"] += p
        bins[index]["outcomes"] += result
    calibration = [
        {"range": f"{i/5:.1f}–{(i+1)/5:.1f}",
         "count": b["count"],
         "mean_probability": round(b["probability_sum"] / b["count"], 4),
         "observed_home_win_rate": round(b["outcomes"] / b["count"], 4)}
        for i, b in enumerate(bins) if b["count"]]
    return {
        "split": {"train_2022": len(train), "calibrate_2023": len(validation),
                  "test_2024": len(test)},
        "features": list(FEATURES),
        "targets": list(TARGETS),
        "test_metrics": metrics,
        "home_win_probability": {
            "brier_score": round(brier_sum / len(test), 5),
            "log_loss": round(log_loss_sum / len(test), 5),
            "naive_brier_score": round(naive_brier_sum / len(test), 5),
            "naive_log_loss": round(naive_log_loss_sum / len(test), 5),
            "calibration_by_probability": calibration,
        },
        "candidate_promotable": (
            metrics["second_half_margin_home"]["model"]["rmse"]
            < metrics["second_half_margin_home"]["naive_baseline"]["rmse"]
            and brier_sum < naive_brier_sum
        ),
        "market_odds_available": False,
        "betting_edge_measured": False,
        "limitations": ["Only score-state features at halftime; no live odds, "
                        "lineups, foul counts, play-by-play, or halftime box scores.",
                        "Regulation regular-season games only; overtime and playoffs excluded.",
                        "A single 2024 holdout does not establish future profitability."],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.dataset.read_text().splitlines()
            if line.strip()]
    report = evaluate(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"split": report["split"],
                      "test_metrics": report["test_metrics"],
                      "home_win_probability": report["home_win_probability"],
                      "candidate_promotable": report["candidate_promotable"],
                      "betting_edge_measured": False}))


if __name__ == "__main__":
    main()
