import json
from pathlib import Path
from typing import Any

TRACKER_PATH = Path("sharpedge/LIVEFLOW_OUTAGE_TRACKER.json")
SUMMARY_PATH = Path("sharpedge/LIVEFLOW_OUTAGE_SUMMARY.json")
ADJUSTER_OUTPUT_PATH = Path("sharpedge/LIVEFLOW_TRIGGER_ADJUSTMENTS.json")

# Thresholds can be tuned later as more samples accumulate.
MIN_GRADED_SAMPLE_TRIGGER = 5
MIN_GRADED_SAMPLE_CONFIDENCE = 5
MIN_ENVIRONMENT_SAMPLE = 5
PROMOTE_HIT_RATE = 58.0
FREEZE_HIT_RATE = 45.0
BOOST_STEP = 0.05
CUT_STEP = -0.05
ENVIRONMENT_PROMOTION_DELTA = 0.04
ENVIRONMENT_CUT_DELTA = -0.04


def load_json(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: Any, path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def classify_adjustment(hit_rate: float, graded_entries: int) -> dict:
    if graded_entries < MIN_GRADED_SAMPLE_TRIGGER:
        return {
            "action": "hold",
            "weight_delta": 0.0,
            "reason": "insufficient_sample"
        }
    if hit_rate >= PROMOTE_HIT_RATE:
        return {
            "action": "promote",
            "weight_delta": BOOST_STEP,
            "reason": "strong_hit_rate"
        }
    if hit_rate <= FREEZE_HIT_RATE:
        return {
            "action": "freeze_or_downgrade",
            "weight_delta": CUT_STEP,
            "reason": "weak_hit_rate"
        }
    return {
        "action": "hold",
        "weight_delta": 0.0,
        "reason": "neutral_band"
    }


def classify_environment_adjustment(environment_name: str, stats: dict) -> dict:
    entries = int(stats.get("entries", 0) or 0)
    avg_confidence = float(stats.get("avg_confidence", 0.0) or 0.0)

    if entries < MIN_ENVIRONMENT_SAMPLE:
        return {
            "action": "hold",
            "weight_delta": 0.0,
            "reason": "insufficient_environment_sample",
            "entries": entries,
            "avg_confidence": avg_confidence,
        }

    if environment_name == "REAL_INFLATION":
        return {
            "action": "promote_continuation_bias",
            "weight_delta": ENVIRONMENT_PROMOTION_DELTA,
            "reason": "real_inflation_environment_confirmed",
            "entries": entries,
            "avg_confidence": avg_confidence,
        }

    if environment_name == "FAKE_INFLATION":
        return {
            "action": "promote_regression_bias",
            "weight_delta": ENVIRONMENT_PROMOTION_DELTA,
            "reason": "fake_inflation_environment_confirmed",
            "entries": entries,
            "avg_confidence": avg_confidence,
        }

    if environment_name == "REAL_SUPPRESSION":
        return {
            "action": "promote_under_bias",
            "weight_delta": ENVIRONMENT_PROMOTION_DELTA,
            "reason": "real_suppression_environment_confirmed",
            "entries": entries,
            "avg_confidence": avg_confidence,
        }

    if environment_name == "FAKE_SUPPRESSION":
        return {
            "action": "promote_over_recovery_bias",
            "weight_delta": ENVIRONMENT_PROMOTION_DELTA,
            "reason": "fake_suppression_environment_confirmed",
            "entries": entries,
            "avg_confidence": avg_confidence,
        }

    if environment_name == "MIXED_NO_FIRE":
        return {
            "action": "downgrade_auto_fire_bias",
            "weight_delta": ENVIRONMENT_CUT_DELTA,
            "reason": "mixed_environment_reduce_aggression",
            "entries": entries,
            "avg_confidence": avg_confidence,
        }

    return {
        "action": "hold",
        "weight_delta": 0.0,
        "reason": "unknown_environment_type",
        "entries": entries,
        "avg_confidence": avg_confidence,
    }


def build_adjustments(summary: dict) -> dict:
    trigger_adjustments = {}
    confidence_adjustments = {}
    halftime_environment_adjustments = {}

    for trigger_name, stats in summary.get("by_trigger", {}).items():
        trigger_adjustments[trigger_name] = {
            **classify_adjustment(
                hit_rate=float(stats.get("hit_rate", 0.0)),
                graded_entries=int(stats.get("graded_entries", 0))
            ),
            "graded_entries": int(stats.get("graded_entries", 0)),
            "hit_rate": float(stats.get("hit_rate", 0.0))
        }

    for confidence_name, stats in summary.get("by_confidence", {}).items():
        graded_entries = int(stats.get("graded_entries", 0))
        hit_rate = float(stats.get("hit_rate", 0.0))

        if graded_entries < MIN_GRADED_SAMPLE_CONFIDENCE:
            confidence_adjustments[confidence_name] = {
                "action": "hold",
                "weight_delta": 0.0,
                "reason": "insufficient_sample",
                "graded_entries": graded_entries,
                "hit_rate": hit_rate
            }
        elif hit_rate >= PROMOTE_HIT_RATE:
            confidence_adjustments[confidence_name] = {
                "action": "promote",
                "weight_delta": BOOST_STEP,
                "reason": "strong_hit_rate",
                "graded_entries": graded_entries,
                "hit_rate": hit_rate
            }
        elif hit_rate <= FREEZE_HIT_RATE:
            confidence_adjustments[confidence_name] = {
                "action": "freeze_or_downgrade",
                "weight_delta": CUT_STEP,
                "reason": "weak_hit_rate",
                "graded_entries": graded_entries,
                "hit_rate": hit_rate
            }
        else:
            confidence_adjustments[confidence_name] = {
                "action": "hold",
                "weight_delta": 0.0,
                "reason": "neutral_band",
                "graded_entries": graded_entries,
                "hit_rate": hit_rate
            }

    for environment_name, stats in summary.get("by_halftime_environment", {}).items():
        halftime_environment_adjustments[environment_name] = classify_environment_adjustment(environment_name, stats)

    return {
        "module": "LIVEFLOW_TRIGGER_AUTO_ADJUSTER",
        "source_summary": str(SUMMARY_PATH),
        "thresholds": {
            "min_graded_sample_trigger": MIN_GRADED_SAMPLE_TRIGGER,
            "min_graded_sample_confidence": MIN_GRADED_SAMPLE_CONFIDENCE,
            "min_environment_sample": MIN_ENVIRONMENT_SAMPLE,
            "promote_hit_rate": PROMOTE_HIT_RATE,
            "freeze_hit_rate": FREEZE_HIT_RATE,
            "boost_step": BOOST_STEP,
            "cut_step": CUT_STEP,
            "environment_promotion_delta": ENVIRONMENT_PROMOTION_DELTA,
            "environment_cut_delta": ENVIRONMENT_CUT_DELTA,
        },
        "trigger_adjustments": trigger_adjustments,
        "confidence_adjustments": confidence_adjustments,
        "halftime_environment_adjustments": halftime_environment_adjustments,
    }


def main() -> None:
    _ = load_json(TRACKER_PATH)  # ensures tracker exists as part of workflow integrity
    summary = load_json(SUMMARY_PATH)
    adjustments = build_adjustments(summary)
    save_json(adjustments, ADJUSTER_OUTPUT_PATH)

    print("=== LIVEFLOW TRIGGER AUTO ADJUSTER ===")
    print(f"Loaded summary from: {SUMMARY_PATH}")
    print(f"Saved adjustments to: {ADJUSTER_OUTPUT_PATH}")
    print("\n-- Trigger Adjustments --")
    for name, stats in adjustments["trigger_adjustments"].items():
        print(f"{name}: {stats}")
    print("\n-- Confidence Adjustments --")
    for name, stats in adjustments["confidence_adjustments"].items():
        print(f"{name}: {stats}")
    print("\n-- Halftime Environment Adjustments --")
    for name, stats in adjustments["halftime_environment_adjustments"].items():
        print(f"{name}: {stats}")


if __name__ == "__main__":
    main()
