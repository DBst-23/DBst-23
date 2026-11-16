import unittest

from modules.rebound_monte_carlo import simulate_player_rebounds, simulate_rebound_combo


PLAYER = {
    "name": "Test Player",
    "line": 8.5,
    "projected_minutes": 36,
    "rebound_chances": 13,
    "rebound_chance_pct": 0.65,
    "adjusted_rebound_chance_pct": 0.65,
    "recent_rebounds": [8, 10, 9],
}


class ReboundSimulationTests(unittest.TestCase):
    def test_half_point_line_and_distribution(self):
        result = simulate_player_rebounds(PLAYER, {}, iterations=2000, seed=7)
        samples = result["results"]
        self.assertEqual(result["line"], 8.5)
        self.assertAlmostEqual(result["over_probability"], sum(x >= 9 for x in samples) / len(samples), places=4)
        self.assertAlmostEqual(result["under_probability"], sum(x <= 8 for x in samples) / len(samples), places=4)
        self.assertEqual(result["push_probability"], 0)
        self.assertAlmostEqual(sum(result["distribution"].values()), 1.0)

    def test_integer_line_push_and_under(self):
        result = simulate_player_rebounds({**PLAYER, "line": 9, "direction": "under"}, {}, iterations=2000, seed=7)
        self.assertAlmostEqual(result["hit_probability"], result["under_probability"])
        self.assertAlmostEqual(
            result["over_probability"] + result["under_probability"] + result["push_probability"], 1.0, places=3
        )

    def test_combo_respects_half_point_and_direction(self):
        legs = [PLAYER, {**PLAYER, "name": "Other", "line": 8.5, "direction": "under"}]
        result = simulate_rebound_combo(legs, {}, iterations=2000, seed=7)
        self.assertEqual(result["leg_summaries"][0]["line"], 8.5)
        self.assertEqual(result["leg_summaries"][1]["direction"], "under")
        self.assertTrue(0 <= result["combo_hit_probability"] <= 1)

    def test_invalid_iterations(self):
        with self.assertRaises(ValueError):
            simulate_player_rebounds(PLAYER, {}, iterations=0)


if __name__ == "__main__":
    unittest.main()
