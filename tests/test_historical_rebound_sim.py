import unittest
from run_historical_rebound_sim import simulate


class HistoricalReboundSimulationTests(unittest.TestCase):
    def setUp(self):
        # Test-only fixture, never presented as actual historical NBA observations.
        self.rows = [
            {"source": "api_basketball_v1", "game_id": i, "player_id": 17,
             "player_name": "TEST PLAYER", "minutes": 30.0, "total_rebounds": r}
            for i, r in [(101, 6), (102, 8), (103, 10), (104, 7)]
        ]

    def test_reproducible(self):
        a = simulate(self.rows, 17, 7.5)
        b = simulate(self.rows, 17, 7.5)
        self.assertEqual(a, b)
        self.assertAlmostEqual(a["over_probability"] + a["under_probability"] +
                               a["push_probability"], 1.0, places=5)
        self.assertEqual(a["historical_games"], 4)
        self.assertIsNone(a["ev"])

    def test_integer_push(self):
        a = simulate(self.rows, 17, 8)
        self.assertGreater(a["push_probability"], 0)

    def test_insufficient_history_rejected(self):
        with self.assertRaises(ValueError):
            simulate(self.rows[:2], 17, 7.5)

    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            simulate(self.rows + [self.rows[0]], 17, 7.5)


if __name__ == "__main__":
    unittest.main()
