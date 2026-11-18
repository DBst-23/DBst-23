"""Offline, zero-credit tests for SharpEdge halftime event collector."""
import datetime as dt
import importlib.util
import pathlib
import unittest
from unittest import mock

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "odds" / "halftime_event_collector.py"
spec = importlib.util.spec_from_file_location("halftime_event_collector", SCRIPT)
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)

def t(value):
    return collector.timestamp(value)

class HalftimeCollectorTests(unittest.TestCase):
    def setUp(self):
        self.q2 = t("2026-11-16T20:11:00Z")
        self.q3 = t("2026-11-16T20:26:00Z")
        self.captured = t("2026-11-16T20:17:00Z")
        self.payload = {
            "id": "test-event", "sport_key": "basketball_nba",
            "home_team": "Washington Wizards", "away_team": "Memphis Grizzlies",
            "bookmakers": [{"key": "testbook", "title": "Fixture Book",
                "markets": [
                    {"key": "totals_h2", "last_update": "2026-11-16T20:15:00Z",
                     "outcomes": [{"name": "Over", "point": 116.5, "price": -110},
                                  {"name": "Under", "point": 116.5, "price": -110}]},
                    {"key": "unrelated_market", "last_update": "2026-11-16T20:15:00Z",
                     "outcomes": [{"name": "Over", "price": -110}]}
                ]}]
        }

    def test_valid_halftime_fixture_is_paper_only(self):
        rows = collector.normalize(self.payload, self.captured, self.q2, self.q3, 30)
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(row["timing_eligible"] for row in rows))
        self.assertTrue(all(not row["training_eligible"] and row["paper_only"] for row in rows))
        self.assertTrue(all(row["registry_join_status"] == "UNMATCHED" for row in rows))

    def test_stale_market_is_not_eligible(self):
        self.payload["bookmakers"][0]["markets"][0]["last_update"] = "2026-11-16T20:10:59Z"
        rows = collector.normalize(self.payload, self.captured, self.q2, self.q3, 30)
        self.assertTrue(all(not row["timing_eligible"] for row in rows))

    def test_after_cutoff_capture_is_not_eligible(self):
        rows = collector.normalize(self.payload, t("2026-11-16T20:25:45Z"), self.q2, self.q3, 30)
        self.assertTrue(all(not row["timing_eligible"] for row in rows))

    def test_no_verified_halftime_clocks(self):
        rows = collector.normalize(self.payload, self.captured, None, None, 30)
        self.assertTrue(all(not row["timing_eligible"] for row in rows))

    def test_missing_markets(self):
        self.payload["bookmakers"] = []
        self.assertEqual(collector.normalize(self.payload, self.captured, self.q2, self.q3, 30), [])

    def test_invalid_event(self):
        with self.assertRaises(ValueError):
            collector.normalize({"bookmakers": []}, self.captured, self.q2, self.q3, 30)

    def test_future_market_update_is_ineligible(self):
        self.payload["bookmakers"][0]["markets"][0]["last_update"] = "2026-11-16T20:18:00Z"
        rows = collector.normalize(self.payload, self.captured, self.q2, self.q3, 30)
        self.assertTrue(all(not row["timing_eligible"] for row in rows))

    def test_pre_halftime_capture_is_ineligible(self):
        rows = collector.normalize(self.payload, t("2026-11-16T20:10:00Z"), self.q2, self.q3, 30)
        self.assertTrue(all(not row["timing_eligible"] for row in rows))

    def test_reversed_clocks_rejected(self):
        with self.assertRaises(ValueError):
            collector.normalize(self.payload, self.captured, self.q3, self.q2, 30)

    def test_paid_mode_is_locked_even_with_opt_in(self):
        import sys
        with mock.patch.object(sys, "argv", ["collector", "--live", "--event-id", "test-event"]):
            with mock.patch.dict("os.environ", {"SHARPEDGE_ALLOW_PAID_ODDS": "YES"}):
                with self.assertRaises(SystemExit) as err:
                    collector.main()
                self.assertEqual(err.exception.code, 2)

if __name__ == "__main__":
    unittest.main()
