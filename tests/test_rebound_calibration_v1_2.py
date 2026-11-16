"""Leakage, date batching, and scoring tests for V1.2."""
import unittest
from modules.rebound_probability_calibration import calibrate


def pred(day, gid, prob, outcome, player=1):
    return {"player_id": player, "game_id": gid, "game_date": day,
            "training_last_date": "2024-12-31", "over_probability": prob,
            "outcome": outcome, "line": 4.5}


class CalibrationV12Tests(unittest.TestCase):
    def test_same_day_labels_never_train_each_other(self):
        rows = [pred("2025-01-01", 1, .8, "over"),
                pred("2025-01-02", 2, .8, "under"),
                pred("2025-01-02", 3, .8, "over")]
        result = calibrate(rows, min_history=1, prior_strength=1)
        a, b = result["predictions"][1:]
        self.assertEqual(a["calibration_history_settled"], 1)
        self.assertEqual(b["calibration_history_settled"], 1)
        self.assertEqual(a["calibrated_over_probability"], b["calibrated_over_probability"])
        self.assertEqual(a["calibration_training_last_date"], "2025-01-01")

    def test_future_outcomes_do_not_change_earlier_predictions(self):
        rows = [pred("2025-01-01", 1, .8, "over"),
                pred("2025-01-02", 2, .8, "under"),
                pred("2025-01-03", 3, .8, "over")]
        baseline = calibrate(rows, min_history=1)["predictions"]
        rows[-1]["outcome"] = "under"
        changed = calibrate(rows, min_history=1)["predictions"]
        self.assertEqual(baseline[:2], changed[:2])

    def test_warmup_and_push(self):
        rows = [pred("2025-01-01", 1, .4, "push"),
                pred("2025-01-02", 2, .4, "over"),
                pred("2025-01-03", 3, .4, "under")]
        r = calibrate(rows, min_history=1)
        self.assertFalse(r["predictions"][1]["calibration_active"])
        self.assertTrue(r["predictions"][2]["calibration_active"])
        self.assertEqual(r["summary"]["pushes_excluded"], 1)
        self.assertEqual(r["summary"]["calibration_active_only"]["n"], 1)

    def test_rejects_leaky_base_prediction(self):
        with self.assertRaises(ValueError):
            calibrate([dict(pred("2025-01-01", 1, .4, "over"),
                            training_last_date="2025-01-01")])

    def test_empty_data(self):
        self.assertEqual(calibrate([])["summary"]["all_settled"]["n"], 0)


if __name__ == "__main__":
    unittest.main()
