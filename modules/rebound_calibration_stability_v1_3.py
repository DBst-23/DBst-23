"""SharpEdge V1.3: chronological out-of-sample calibration stability audit.

Consumes V1.2 prequential predictions; never refits calibration on evaluation labels.
Calendar-month cohorts are descriptive holdout slices, not independent seasons.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from datetime import date
from pathlib import Path


def evaluate(payload: dict, *, min_cohort: int = 30) -> dict:
    if type(min_cohort) is not int or min_cohort < 1:
        raise ValueError("min_cohort must be a positive integer")
    if payload.get("model") != "sharpedge_rebound_prequential_calibration_v1_2":
        raise ValueError("Expected V1.2 calibrated prediction artifact")
    rows = payload.get("predictions")
    if not isinstance(rows, list):
        raise ValueError("Missing predictions")
    groups = defaultdict(list)
    seen = set()
    for row in rows:
        day = row.get("game_date")
        try:
            if date.fromisoformat(day).isoformat() != day:
                raise ValueError()
        except (TypeError, ValueError):
            raise ValueError("Invalid game_date")
        key = (row.get("player_id"), row.get("game_id"))
        if key in seen:
            raise ValueError("Duplicate player-game prediction")
        seen.add(key)
        cutoff = row.get("calibration_training_last_date")
        if cutoff is not None and (not isinstance(cutoff, str) or cutoff >= day):
            raise ValueError("Calibration uses same-day or future data")
        if row.get("calibration_active") is not True or row.get("outcome") == "push":
            continue
        if cutoff is None:
            raise ValueError("Active calibration has no prior-date history")
        y = row.get("outcome")
        if y not in ("over", "under"):
            raise ValueError("Invalid settled outcome")
        raw = row.get("raw_over_probability")
        calibrated = row.get("calibrated_over_probability")
        for p in (raw, calibrated):
            if type(p) not in (int, float) or not math.isfinite(p) or not 0 <= p <= 1:
                raise ValueError("Invalid probability")
        groups[day[:7]].append((float(raw), float(calibrated), int(y == "over")))

    cohorts = []
    for month, items in sorted(groups.items()):
        n = len(items)
        raw_brier = sum((r - y) ** 2 for r, _, y in items) / n
        cal_brier = sum((c - y) ** 2 for _, c, y in items) / n
        cohorts.append({
            "month": month, "n": n, "eligible": n >= min_cohort,
            "raw_brier": round(raw_brier, 8),
            "calibrated_brier": round(cal_brier, 8),
            "delta_calibrated_minus_raw": round(cal_brier - raw_brier, 8),
            "observed_over_rate": round(sum(y for _, _, y in items) / n, 8),
            "mean_raw_probability": round(sum(r for r, _, _ in items) / n, 8),
            "mean_calibrated_probability": round(sum(c for _, c, _ in items) / n, 8),
        })
    eligible = [c for c in cohorts if c["eligible"]]
    return {
        "model": "sharpedge_rebound_calibration_stability_v1_3",
        "input_model": payload["model"],
        "min_cohort": min_cohort,
        "cohorts": cohorts,
        "summary": {
            "eligible_months": len(eligible),
            "months_improved": sum(c["delta_calibrated_minus_raw"] < 0 for c in eligible),
            "months_worsened": sum(c["delta_calibrated_minus_raw"] > 0 for c in eligible),
            "inconclusive": len(eligible) < 2,
        },
        "limitations": (
            "Descriptive chronological month slices of prequential predictions; "
            "not independent seasons, not a separately frozen model holdout, "
            "and no sportsbook odds, EV, ROI, or betting-edge claim. "
            "Do not tune V1.2 parameters using these evaluation cohorts."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("rebound_stability_v1_3.json"))
    parser.add_argument("--min-cohort", type=int, default=30)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = evaluate(payload, min_cohort=args.min_cohort)
    result["input_provenance"] = payload.get("input_provenance")
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
