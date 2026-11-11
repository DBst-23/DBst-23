"""Offline regression tests for isolated SportsDataIO diagnostic."""
import importlib.util
import unittest
from pathlib import Path

FILE = Path(__file__).resolve().parent / "diagnose_sportsdataio_game.py"
spec = importlib.util.spec_from_file_location("diagnostic", FILE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def fixture():
    return {
        "Game": {"GameID": 14620, "AwayTeamScore": 100, "HomeTeamScore": 110},
        "Quarters": [
            {"Number": 1, "AwayScore": 25, "HomeScore": 30},
            {"Number": 2, "AwayScore": 25, "HomeScore": 25},
            {"Number": 3, "AwayScore": 25, "HomeScore": 25},
            {"Number": 4, "AwayScore": 25, "HomeScore": 30},
        ],
        "Plays": [{"PotentialPoints": 2, "PlayID": 1}],
    }

class ValidationTests(unittest.TestCase):
    def test_valid_structure_not_authenticated(self):
        errors, warnings, stats = module.validate(fixture(), 14620)
        self.assertEqual(errors, [])
        self.assertTrue(warnings)
        self.assertEqual(stats["regulation_away_points"], 100)

    def test_mismatched_final_rejected(self):
        game = fixture()
        game["Game"]["HomeTeamScore"] = 111
        errors, _, _ = module.validate(game, 14620)
        self.assertIn("quarter sums disagree with Game final score", errors)

    def test_impossible_shot_rejected(self):
        game = fixture()
        game["Plays"][0]["PotentialPoints"] = 4
        errors, _, _ = module.validate(game, 14620)
        self.assertTrue(any("PotentialPoints" in error for error in errors))

    def test_missing_quarter_rejected(self):
        game = fixture()
        game["Quarters"].pop()
        errors, _, _ = module.validate(game, 14620)
        self.assertTrue(any("missing regulation" in error for error in errors))

if __name__ == "__main__":
    unittest.main()
