import json
from pathlib import Path
from collections import Counter, defaultdict
from statistics import mean

TRACKER_PATH = Path("sharpedge/LIVEFLOW_OUTAGE_TRACKER.json")
SUMMARY_OUTPUT_PATH = Path("sharpedge/LIVEFLOW_OUTAGE_SUMMARY.json")
CLASSIFIER_OUTPUT_PATH = Path("modules/HALFTIME_CLASSIFIER_OUTPUTS.json")


def load_tracker(path: Path = TRACKER_PATH) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Tracker file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_classifier_outputs(path: Path = CLASSIFIER_OUTPUT_PATH) -> dict:
    if not path.exists():
        return {"entries": []}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_summary(summary: dict, path: Path = SUMMARY_OUTPUT_PATH) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        f.write("\n")


def _safe_pct(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round((numerator / denominator) * 100, 2)


def _parse_result(result: str) -> str:
    value = (result or "").strip().lower()
    if value in {"win", "hit", "won"}:
        return "win"
    if value in {"loss", "lose", "lost", "miss"}:
        return "loss"
    if value in {"pass", "passed"}:
        return "pass"
    return "unknown"


def summarize_entries(entries: list[dict], classifier_entries: list[dict]) -> dict:
    result_counter = Counter()
    trigger_counter = Counter()
    confidence_counter = Counter()
    mpz_counter = Counter()
    classifier_counter = Counter()
    classifier_action_counter = Counter()

    trigger_results = defaultdict(lambda: {"wins": 0, "losses": 0, "passes": 0, "unknown": 0})
    confidence_results = defaultdict(lambda: {"wins": 0, "losses": 0, "passes": 0, "unknown": 0})
    player_results = defaultdict(lambda: {"wins": 0, "losses": 0, "passes": 0, "unknown": 0, "entries": 0})
    classifier_results = defaultdict(lambda: {"entries": 0, "avg_confidence": 0.0, "notes": []})

    fair_probs = []
    live_prices = []

    for entry in entries:
        normalized_result = _parse_result(entry.get("result", ""))
        trigger_type = entry.get("trigger_type", "") or "UNSPECIFIED"
        confidence_grade = entry.get("confidence_grade", "") or "UNSPECIFIED"
        mpz_tag = entry.get("mpz_tag", "") or "UNSPECIFIED"
        player = entry.get("player", "") or "UNSPECIFIED"

        result_counter[normalized_result] += 1
        trigger_counter[trigger_type] += 1
        confidence_counter[confidence_grade] += 1
        mpz_counter[mpz_tag] += 1

        if normalized_result == "win":
            trigger_results[trigger_type]["wins"] += 1
            confidence_results[confidence_grade]["wins"] += 1
            player_results[player]["wins"] += 1
        elif normalized_result == "loss":
            trigger_results[trigger_type]["losses"] += 1
            confidence_results[confidence_grade]["losses"] += 1
            player_results[player]["losses"] += 1
        elif normalized_result == "pass":
            trigger_results[trigger_type]["passes"] += 1
            confidence_results[confidence_grade]["passes"] += 1
            player_results[player]["passes"] += 1
        else:
            trigger_results[trigger_type]["unknown"] += 1
            confidence_results[confidence_grade]["unknown"] += 1
            player_results[player]["unknown"] += 1

        player_results[player]["entries"] += 1

        fair_prob = entry.get("updated_fair_probability", 0)
        if isinstance(fair_prob, (int, float)) and fair_prob > 0:
            fair_probs.append(float(fair_prob))

        live_price = entry.get("live_price", "")
        if isinstance(live_price, str) and live_price:
            live_prices.append(live_price)

    for c in classifier_entries:
        env = c.get("environment_type", "UNSPECIFIED")
        action_bias = c.get("action_bias", "UNSPECIFIED")
        confidence = float(c.get("confidence", 0.0) or 0.0)
        classifier_counter[env] += 1
        classifier_action_counter[action_bias] += 1
        classifier_results[env]["entries"] += 1
        classifier_results[env].setdefault("confidence_values", []).append(confidence)
        for note in c.get("notes", []):
            classifier_results[env]["notes"].append(note)

    graded = result_counter["win"] + result_counter["loss"]

    summary = {
        "module": "LIVEFLOW_OUTAGE_SUMMARY_ENGINE",
        "summary_output_path": str(SUMMARY_OUTPUT_PATH),
        "classifier_output_path": str(CLASSIFIER_OUTPUT_PATH),
        "total_entries": len(entries),
        "graded_entries": graded,
        "wins": result_counter["win"],
        "losses": result_counter["loss"],
        "passes": result_counter["pass"],
        "unknown": result_counter["unknown"],
        "overall_hit_rate": _safe_pct(result_counter["win"], graded),
        "average_updated_fair_probability": round(mean(fair_probs), 4) if fair_probs else 0.0,
        "sample_live_prices": live_prices[:10],
        "by_trigger": {},
        "by_confidence": {},
        "by_player": {},
        "by_halftime_environment": {},
        "halftime_action_bias_counts": dict(classifier_action_counter),
        "top_mpz_tags": mpz_counter.most_common(10),
    }

    for trigger, stats in trigger_results.items():
        graded_trigger = stats["wins"] + stats["losses"]
        summary["by_trigger"][trigger] = {
            **stats,
            "hit_rate": _safe_pct(stats["wins"], graded_trigger),
            "graded_entries": graded_trigger,
        }

    for confidence, stats in confidence_results.items():
        graded_conf = stats["wins"] + stats["losses"]
        summary["by_confidence"][confidence] = {
            **stats,
            "hit_rate": _safe_pct(stats["wins"], graded_conf),
            "graded_entries": graded_conf,
        }

    for player, stats in player_results.items():
        graded_player = stats["wins"] + stats["losses"]
        summary["by_player"][player] = {
            **stats,
            "hit_rate": _safe_pct(stats["wins"], graded_player),
            "graded_entries": graded_player,
        }

    for env, stats in classifier_results.items():
        conf_values = stats.pop("confidence_values", [])
        summary["by_halftime_environment"][env] = {
            "entries": stats["entries"],
            "avg_confidence": round(mean(conf_values), 4) if conf_values else 0.0,
            "sample_notes": stats["notes"][:5],
        }

    return summary


def print_summary(summary: dict) -> None:
    print("=== LIVEFLOW OUTAGE SUMMARY ENGINE ===")
    print(f"Total entries: {summary['total_entries']}")
    print(f"Graded entries: {summary['graded_entries']}")
    print(f"Wins: {summary['wins']}")
    print(f"Losses: {summary['losses']}")
    print(f"Passes: {summary['passes']}")
    print(f"Unknown: {summary['unknown']}")
    print(f"Overall hit rate: {summary['overall_hit_rate']}%")
    print(f"Average updated fair probability: {summary['average_updated_fair_probability']}")
    print(f"Exported summary: {summary['summary_output_path']}")
    print(f"Classifier source: {summary['classifier_output_path']}")
    print()

    print("-- By Trigger --")
    for trigger, stats in summary["by_trigger"].items():
        print(f"{trigger}: {stats}")
    print()

    print("-- By Confidence --")
    for confidence, stats in summary["by_confidence"].items():
        print(f"{confidence}: {stats}")
    print()

    print("-- By Player --")
    for player, stats in summary["by_player"].items():
        print(f"{player}: {stats}")
    print()

    print("-- By Halftime Environment --")
    for env, stats in summary["by_halftime_environment"].items():
        print(f"{env}: {stats}")
    print()

    print("-- Halftime Action Bias Counts --")
    for bias, count in summary["halftime_action_bias_counts"].items():
        print(f"{bias}: {count}")
    print()

    print("-- Top MPZ Tags --")
    for tag, count in summary["top_mpz_tags"]:
        print(f"{tag}: {count}")


def main() -> None:
    tracker = load_tracker()
    classifier_payload = load_classifier_outputs()
    entries = tracker.get("entries", [])
    classifier_entries = classifier_payload.get("entries", [])
    summary = summarize_entries(entries, classifier_entries)
    save_summary(summary)
    print_summary(summary)


if __name__ == "__main__":
    main()
