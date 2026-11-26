"""Offline/no-secret tests for one-time team-total coverage probe."""
import datetime as dt
import importlib.util
import os
from pathlib import Path
import sys
import unittest
from unittest import mock

script = Path(__file__).resolve().parents[1] / "scripts/odds/one_credit_teamtotals_probe.py"
spec = importlib.util.spec_from_file_location("one_credit_teamtotals_probe", script)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class ProbeUnitTests(unittest.TestCase):
    def event(self):
        return {
            "id": "1234567890abcdef1234567890abcdef",
            "sport_key": "basketball_nba",
            "home_team": probe.HOME,
            "away_team": probe.AWAY,
            "commence_time": "2026-11-28T00:00:00Z",
        }

    def make_payload(self, home=True, away=True):
        outcomes = []
        if home:
            outcomes += [
                {"description": probe.HOME, "name": "Over", "price": -110, "point": 52.5},
                {"description": probe.HOME, "name": "Under", "price": -110, "point": 52.5},
            ]
        if away:
            outcomes += [
                {"description": probe.AWAY, "name": "Over", "price": -110, "point": 51.5},
                {"description": probe.AWAY, "name": "Under", "price": -110, "point": 51.5},
            ]
        return {"id": self.event()["id"], "bookmakers": [
            {"key": probe.BOOK, "markets": [
                {"key": probe.MARKET, "outcomes": outcomes},
            ]},
        ]}

    def test_target_date_converts_correctly_from_utc(self):
        self.assertEqual(probe.select_target([self.event()])["id"], self.event()["id"])

    def test_wrong_game_not_accepted(self):
        bad = dict(self.event(), home_team="Boston Celtics")
        with self.assertRaises(probe.ProbeStop):
            probe.select_target([bad])

    def test_wrong_date_not_accepted(self):
        bad = dict(self.event(), commence_time="2026-11-29T00:00:00Z")
        with self.assertRaises(probe.ProbeStop):
            probe.select_target([bad])

    def test_duplicate_match_not_accepted(self):
        with self.assertRaises(probe.ProbeStop):
            probe.select_target([self.event(), self.event()])

    def test_both_teams_over_under_covered(self):
        result = probe.quote_coverage(self.make_payload(), self.event())
        self.assertEqual(result["status"], "both_teams")
        self.assertEqual(result["home_over_under"], ["Over", "Under"])
        self.assertEqual(result["away_over_under"], ["Over", "Under"])

    def test_one_missing_team_is_partial_not_fabricated(self):
        result = probe.quote_coverage(self.make_payload(away=False), self.event())
        self.assertEqual(result["status"], "partial")
        self.assertEqual(result["away_over_under"], [])

    def test_empty_bookmakers_is_unavailable_not_fabricated(self):
        result = probe.quote_coverage(
            {"id": self.event()["id"], "bookmakers": []}, self.event(),
        )
        self.assertEqual(result["status"], "not_returned")

    def test_wrong_bookmaker_rejected(self):
        payload = self.make_payload()
        payload["bookmakers"][0]["key"] = "otherbook"
        with self.assertRaises(probe.ProbeStop):
            probe.quote_coverage(payload, self.event())

    def test_wrong_event_id_rejected(self):
        payload = self.make_payload()
        payload["id"] = "bad-event"
        with self.assertRaises(probe.ProbeStop):
            probe.quote_coverage(payload, self.event())

    def test_preflight_makes_only_one_free_api_call(self):
        response = ([self.event()], {"x-requests-last": "0", "x-requests-remaining": "100"}, dt.datetime.now(dt.timezone.utc))
        with mock.patch.dict(os.environ, {"ODDS_API_KEY": "FAKE_NO_NETWORK_KEY"}):
            with mock.patch.object(probe, "fetch_json", return_value=response) as fetch:
                with mock.patch.object(sys, "argv", ["probe", "--phase", "preflight"]):
                    probe.run()
        self.assertEqual(fetch.call_count, 1)
        self.assertTrue(fetch.call_args.args[0].endswith("/sports/basketball_nba/events"))

    def test_paid_probe_without_explicit_phrase_stops_before_database(self):
        response = ([self.event()], {"x-requests-last": "0", "x-requests-remaining": "100"}, dt.datetime.now(dt.timezone.utc))
        with mock.patch.dict(os.environ, {"ODDS_API_KEY": "FAKE_NO_NETWORK_KEY"}):
            with mock.patch.object(probe, "fetch_json", return_value=response) as fetch:
                with mock.patch.object(sys, "argv", ["probe", "--phase", "probe"]):
                    with self.assertRaises(probe.ProbeStop):
                        probe.run()
        self.assertEqual(fetch.call_count, 1)  # FREE endpoint only.

    def test_missing_api_key_stops_without_network(self):
        with mock.patch.dict(os.environ, {"ODDS_API_KEY": ""}):
            with mock.patch.object(probe, "fetch_json") as fetch:
                with mock.patch.object(sys, "argv", ["probe", "--phase", "preflight"]):
                    with self.assertRaises(probe.ProbeStop):
                        probe.run()
        fetch.assert_not_called()


if __name__ == "__main__":
    unittest.main()
