"""Offline regression tests: never serialize real odds/score/credential values."""
import importlib.util
from pathlib import Path
import json
import unittest

path = Path(__file__).resolve().parents[1] / "scripts" / "sportsdataio_liveodds_shape_audit.py"
spec = importlib.util.spec_from_file_location("shape_audit", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ShapeAuditTests(unittest.TestCase):
    def test_nested_market_paths_without_leaking_values(self):
        source = [
            {"GameId": 123, "LiveOdds": [
                {"SportsbookId": 42, "MoneyLineHome": -125, "PointSpread": -3.5,
                 "OverUnder": 224.5, "Period": "2H",
                 "TeamTotalHome": 119.5, "OpaqueSecret": "SENSITIVE_MARKER_DO_NOT_LOG"}
            ]},
            {"GameId": 456, "LiveOdds": []},
        ]
        report = mod.structural_audit(source)
        self.assertEqual(report["records_returned"], 2)
        self.assertEqual(report["liveodds_present"], 2)
        self.assertEqual(report["liveodds_nonempty"], 1)
        self.assertTrue(report["bookmaker_identifier_field_paths"])
        self.assertTrue(report["moneyline_field_paths"])
        self.assertTrue(report["spread_field_paths"])
        self.assertTrue(report["game_total_field_paths"])
        self.assertTrue(report["second_half_or_period_field_paths"])
        self.assertTrue(report["team_total_field_paths"])
        self.assertFalse(report["explicit_second_half_market_value_verified"])
        text = json.dumps(report)
        for forbidden in ("SENSITIVE_MARKER_DO_NOT_LOG", "224.5", "-125", "119.5", "123", "456", '"2H"'):
            self.assertNotIn(forbidden, text)

    def test_empty_liveodds_does_not_imply_market_coverage(self):
        report = mod.structural_audit([{"LiveOdds": None}, {"LiveOdds": []}])
        self.assertEqual(report["liveodds_nonempty"], 0)
        self.assertFalse(report["moneyline_field_paths"])
        self.assertFalse(report["team_total_field_paths"])

    def test_missing_liveodds_distinct_from_empty(self):
        report = mod.structural_audit([{"PregameOdds": [{"MoneyLine": -100}]}])
        self.assertEqual(report["liveodds_present"], 0)
        self.assertEqual(report["liveodds_nonempty"], 0)
        self.assertEqual(report["nested_field_paths"], [])

    def test_unsafe_source_field_names_never_render(self):
        report = mod.structural_audit([{"LiveOdds": [{ "apiKey=leak": "secret",
            "SportsbookID": 12, "\\nMALICIOUS": "x"}]}])
        self.assertEqual(report["bookmaker_identifier_field_paths"], ["LiveOdds[].SportsbookID"])
        self.assertNotIn("apiKey=leak", json.dumps(report))

    def test_trial_remains_unverified(self):
        report = mod.structural_audit([{"LiveOdds": [{"Market": "SecondHalf", "Price": 100}]}])
        self.assertFalse(report["numeric_values_accepted_for_training"])
        self.assertFalse(report["explicit_second_half_market_value_verified"])

    def test_malformed_response_is_rejected(self):
        self.assertEqual(mod.structural_audit({})["status"], "unexpected_response_shape")


if __name__ == "__main__":
    unittest.main()
