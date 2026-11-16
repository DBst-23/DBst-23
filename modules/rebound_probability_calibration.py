"""SharpEdge V1.2: prequential, prior-date-only probability calibration.

A smoothed histogram calibrator is deliberately simple and auditable.
All observations from a date are scored before any outcomes from that date
are added to calibration history. No random split or future-date fitting.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from datetime import date
from pathlib import Path


def calibrate(predictions: list[dict], *, bins: int = 10,
              min_history: int = 100, prior_strength: float = 30.0) -> dict:
    if not isinstance(predictions, list):
        raise ValueError("Expected predictions list")
    if type(bins) is not int or bins < 2 or bins > 100:
        raise ValueError("Invalid bins")
    if type(min_history) is not int or min_history < 1:
        raise ValueError("Invalid min_history")
    if not math.isfinite(prior_strength) or prior_strength <= 0:
        raise ValueError("Invalid prior_strength")

    seen = set()
    ordered = []
    for p in predictions:
        if not isinstance(p, dict):
            raise ValueError("Invalid prediction")
        d = p.get("game_date")
        try:
            if date.fromisoformat(d).isoformat() != d:
                raise ValueError()
        except (TypeError, ValueError):
            raise ValueError("Invalid game_date")
        cutoff = p.get("training_last_date")
        if cutoff is None or not isinstance(cutoff, str) or cutoff >= d:
            raise ValueError("Base prediction violates training-date cutoff")
        prob = p.get("over_probability")
        if type(prob) not in (int, float) or not math.isfinite(prob) or not 0 <= prob <= 1:
            raise ValueError("Invalid over_probability")
        outcome = p.get("outcome")
        if outcome not in ("over", "under", "push"):
            raise ValueError("Invalid outcome")
        key = (p.get("player_id"), p.get("game_id"))
        if key in seen:
            raise ValueError("Duplicate prediction")
        seen.add(key)
        ordered.append(p)
    ordered.sort(key=lambda p: (p["game_date"], str(p.get("player_id")), str(p.get("game_id"))))

    # Historical bucket outcomes are exclusively from completed earlier dates.
    counts = [0] * bins
    successes = [0] * bins
    settled_history = 0
    last_history_date = None
    scored = []
    by_date = defaultdict(list)
    for p in ordered:
        by_date[p["game_date"]].append(p)

    for day in sorted(by_date):
        batch = by_date[day]
        # Score the entire day using a frozen prior-date snapshot.
        for p in batch:
            raw = float(p["over_probability"])
            idx = min(bins - 1, int(raw * bins))
            # Bayesian shrinkage to raw probability, avoiding unstable tiny bins.
            calibrated = ((successes[idx] + prior_strength * raw) /
                          (counts[idx] + prior_strength))
            active = settled_history >= min_history
            selected = calibrated if active else raw
            rec = {
                "player_id": p.get("player_id"),
                "game_id": p.get("game_id"),
                "game_date": day,
                "line": p.get("line"),
                "outcome": p["outcome"],
                "raw_over_probability": raw,
                "calibrated_over_probability": round(selected, 8),
                "calibration_active": active,
                "calibration_history_settled": settled_history,
                "calibration_bin_count": counts[idx],
                "calibration_training_last_date": last_history_date,
                "bin": idx,
            }
            if p["outcome"] != "push":
                y = int(p["outcome"] == "over")
                rec["raw_brier"] = (raw - y) ** 2
                rec["calibrated_brier"] = (selected - y) ** 2
            scored.append(rec)
        # Only now may the day's labels enter subsequent calibration fits.
        for p in batch:
            if p["outcome"] == "push":
                continue
            idx = min(bins - 1, int(float(p["over_probability"]) * bins))
            counts[idx] += 1
            successes[idx] += int(p["outcome"] == "over")
            settled_history += 1
        if any(p["outcome"] != "push" for p in batch):
            last_history_date = day

    settled = [p for p in scored if "raw_brier" in p]
    evaluated = [p for p in settled if p["calibration_active"]]
    def metrics(group):
        if not group:
            return {"n": 0, "raw_brier": None, "calibrated_brier": None, "brier_delta": None}
        raw = sum(p["raw_brier"] for p in group) / len(group)
        cal = sum(p["calibrated_brier"] for p in group) / len(group)
        return {"n": len(group), "raw_brier": round(raw, 8),
                "calibrated_brier": round(cal, 8),
                "brier_delta": round(cal - raw, 8)}
    return {
        "model": "sharpedge_rebound_prequential_calibration_v1_2",
        "method": "prior-date-only histogram with raw-probability shrinkage",
        "parameters": {"bins": bins, "min_history": min_history, "prior_strength": prior_strength},
        "summary": {"all_settled": metrics(settled), "calibration_active_only": metrics(evaluated),
                    "total_predictions": len(scored), "pushes_excluded": len(scored) - len(settled)},
        "predictions": scored,
        "limitations": "Illustrative line; no historical sportsbook odds, EV, ROI, or demonstrated betting edge. Parameters are predeclared, not tuned on evaluation outcomes.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("rebound_calibration_v1_2.json"))
    parser.add_argument("--min-history", type=int, default=100)
    parser.add_argument("--prior-strength", type=float, default=30.0)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = calibrate(payload["predictions"], min_history=args.min_history,
                       prior_strength=args.prior_strength)
    result["input_provenance"] = payload.get("provenance")
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
