import unittest

from modules.rebound_walk_forward_backtest import backtest


def row(game_id, day, rebounds, player=570):
    return {
        "source": "api_basketball_v1", "player_id": player,
        "player_name": "TEST FIXTURE", "game_id": game_id,
        "game_date": day, "minutes": 20.0, "total_rebounds": rebounds,
    }


class WalkForwardTests(unittest.TestCase):
    def test_strictly_prior_dates_and_no_same_day_leakage(self):
        rows = [
            row(90, "2025-01-01", 2),
            row(10, "2025-01-02", 4),
            row(70, "2025-01-03", 6),
            row(11, "2025-01-04", 100),
            row(12, "2025-01-04", 0),
            row(13, "2025-01-05", 8),
        ]
        result = backtest(rows, min_games=3, window=3)
        same_day = [p for p in result["predictions"] if p["game_date"] == "2025-01-04"]
        self.assertEqual(len(same_day), 2)
        for p in same_day:
            self.assertEqual(p["training_game_ids"], [90, 10, 70])
            self.assertEqual(p["projected_mean"], 4)
            self.assertLess(p["training_last_date"], p["game_date"])
        self.assertEqual(result["summary"]["skipped_insufficient_history"], 3)

    def test_deterministic_order_independent(self):
        rows = [row(i, f"2025-01-{i:02d}", i % 7) for i in range(1, 9)]
        self.assertEqual(backtest(rows), backtest(list(reversed(rows))))

    def test_reject_missing_dates_and_duplicates(self):
        rows = [row(i, f"2025-01-{i:02d}", i) for i in range(1, 5)]
        bad = [dict(rows[0])]
        bad[0].pop("game_date")
        with self.assertRaises(ValueError):
            backtest(bad)
        with self.assertRaises(ValueError):
            backtest(rows + [rows[0]])

    def test_half_point_probabilities_and_metrics(self):
        rows = [row(i, f"2025-01-{i:02d}", i) for i in range(1, 6)]
        result = backtest(rows, line=3.5)
        self.assertEqual(result["summary"]["predictions"], 2)
        for p in result["predictions"]:
            self.assertAlmostEqual(p["over_probability"] + p["under_probability"] + p["push_probability"], 1.0, places=6)
            self.assertEqual(p["push_probability"], 0)
        self.assertIsNotNone(result["summary"]["mean_absolute_error"])


if __name__ == "__main__":
    unittest.main()
