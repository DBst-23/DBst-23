"""Regression tests for V1.3 out-of-sample stability reporting."""
import unittest

from modules.rebound_calibration_stability_v1_3 import evaluate


def row(day, game, raw, cal, outcome="over", cutoff="2024-10-01"):
    return {
        "game_date": day, "game_id": game, "player_id": 7,
        "calibration_active": True, "calibration_training_last_date": cutoff,
        "raw_over_probability": raw, "calibrated_over_probability": cal,
        "outcome": outcome,
    }


def payload(rows):
    return {"model": "sharpedge_rebound_prequential_calibration_v1_2", "predictions": rows}


class StabilityTests(unittest.TestCase):
    def test_months_are_separate_and_brier_delta_correct(self):
        rows = [
            row("2024-10-20", 1, 0.4, 0.8),
            row("2024-11-20", 2, 0.8, 0.9, "under"),
        ]
        result = evaluate(payload(rows), min_cohort=1)
        self.assertEqual(result["summary"]["eligible_months"], 2)
        self.assertEqual(result["summary"]["months_improved"], 1)
        self.assertEqual(result["summary"]["months_worsened"], 1)
        self.assertAlmostEqual(result["cohorts"][0]["delta_calibrated_minus_raw"], -0.32)
        self.assertAlmostEqual(result["cohorts"][1]["delta_calibrated_minus_raw"], 0.17)

    def test_reject_same_day_or_future_calibration(self):
        for cutoff in ("2024-10-20", "2024-10-21"):
            with self.subTest(cutoff=cutoff), self.assertRaises(ValueError):
                evaluate(payload([row("2024-10-20", 1, 0.4, 0.8, cutoff=cutoff)]))

    def test_excludes_inactive_and_push(self):
        inactive = row("2024-10-20", 1, 0.4, 0.8)
        inactive["calibration_active"] = False
        push = row("2024-10-21", 2, 0.4, 0.8, "push")
        self.assertEqual(evaluate(payload([inactive, push]))["cohorts"], [])

    def test_duplicate_prediction_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(payload([row("2024-10-20", 1, 0.4, 0.8)] * 2))


if __name__ == "__main__":
    unittest.main()
