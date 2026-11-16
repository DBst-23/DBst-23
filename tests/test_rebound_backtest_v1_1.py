"""Regression tests for SharpEdge rebound walk-forward v1.1."""
import unittest
from modules.rebound_walk_forward_backtest import backtest

def row(pid, gid, day, rebounds):
    return {"source": "api_basketball_v1", "player_id": pid,
            "player_name": str(pid), "game_id": gid,
            "game_date": day, "minutes": 25.0, "total_rebounds": rebounds}

class WalkForwardV11Tests(unittest.TestCase):
    def test_multi_player_distributions_and_calibration(self):
        rows = []
        for pid in (101, 202):
            for i in range(6):
                rows.append(row(pid, pid * 100 + i, f"2025-01-{i+1:02d}", (pid % 5) + i))
        result = backtest(rows, min_games=3, line=4.5)
        self.assertEqual(result["summary"]["predictions"], 6)
        self.assertEqual(result["summary"]["players"], 2)
        self.assertEqual(len(result["calibration_bins"]), 10)
        for p in result["predictions"]:
            self.assertLess(p["training_last_date"], p["game_date"])
            self.assertIsInstance(p["projected_median"], int)
            self.assertAlmostEqual(sum(p["rebound_distribution"]), 1.0, places=6)
            self.assertAlmostEqual(p["over_probability"] + p["under_probability"] + p["push_probability"], 1.0, places=6)

    def test_same_day_excluded(self):
        rows = [row(1, 1, "2025-01-01", 3),
                row(1, 2, "2025-01-02", 4),
                row(1, 3, "2025-01-03", 5),
                row(1, 4, "2025-01-04", 6),
                row(1, 5, "2025-01-04", 12)]
        result = backtest(rows, min_games=3)
        self.assertEqual(result["summary"]["predictions"], 2)
        for p in result["predictions"]:
            self.assertNotIn(4, p["training_game_ids"])
            self.assertNotIn(5, p["training_game_ids"])

if __name__ == "__main__":
    unittest.main()
