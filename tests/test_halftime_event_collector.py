"""Offline, zero-credit tests for SharpEdge halftime event collector."""
import datetime as dt
import importlib.util
import json
import pathlib
import tempfile
import urllib.parse
import sys
import unittest
from unittest import mock

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "odds" / "halftime_event_collector.py"
sys.path.insert(0, str(SCRIPT.parent))  # Resolve sibling persistent_credit_ledger in direct-file import.
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

    def simulate_http_receipt(self, when):
        """Offline HTTP stub: clock must be read AFTER response.read() completes."""
        observed = []
        fixture = self.payload

        class FakeResponse:
            headers = {"x-requests-last": "0"}

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                observed.append("response_body_read")
                return json.dumps(fixture).encode("utf-8")

        def receipt_clock():
            observed.append("receipt_clock")
            return t(when)

        with mock.patch.object(collector.urllib.request, "urlopen", return_value=FakeResponse()) as urlopen:
            payload, headers, captured_at = collector.live_fetch(
                "test-event", "basketball_nba", "us", collector.MARKETS,
                "OFFLINE_FAKE_KEY", clock=receipt_clock,
            )
        urlopen.assert_called_once()
        self.assertEqual(observed, ["response_body_read", "receipt_clock"])
        self.assertEqual(headers["x-requests-last"], "0")
        rows = collector.normalize(payload, captured_at, self.q2, self.q3, 30)
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(not row["training_eligible"] for row in rows))
        self.assertTrue(all(row["captured_at_utc"] == when for row in rows))
        return rows

    def test_http_response_after_q3_starts_is_ineligible(self):
        # Request could have begun during halftime. Only receipt time matters.
        rows = self.simulate_http_receipt("2026-11-16T20:26:05Z")
        self.assertTrue(all(not row["timing_eligible"] for row in rows))

    def test_http_response_at_exact_latency_cutoff_is_ineligible(self):
        # Cutoff is 30s before 20:26:00Z; equality is deliberately rejected.
        rows = self.simulate_http_receipt("2026-11-16T20:25:30Z")
        self.assertTrue(all(not row["timing_eligible"] for row in rows))

    def test_http_response_before_latency_cutoff_can_be_eligible(self):
        rows = self.simulate_http_receipt("2026-11-16T20:25:29Z")
        self.assertTrue(all(row["timing_eligible"] for row in rows))

    def test_team_total_h2_quotes_identify_both_teams(self):
        market = {
            "key": "team_totals_h2",
            "last_update": "2026-11-16T20:15:00Z",
            "outcomes": [
                {"name": "Over", "description": "Washington Wizards", "point": 55.5, "price": -110},
                {"name": "Under", "description": "Washington Wizards", "point": 55.5, "price": -110},
                {"name": "Over", "description": "Memphis Grizzlies", "point": 50.5, "price": -105},
                {"name": "Under", "description": "Memphis Grizzlies", "point": 50.5, "price": -115},
            ],
        }
        self.payload["bookmakers"][0]["markets"].append(market)
        rows = collector.normalize(self.payload, self.captured, self.q2, self.q3, 30)
        team_rows = [r for r in rows if r["market"] == "team_totals_h2"]
        self.assertEqual(len(team_rows), 4)
        self.assertEqual(
            {(r["team_total_team"], r["outcome_name"], r["line"]) for r in team_rows},
            {
                ("Washington Wizards", "Over", 55.5),
                ("Washington Wizards", "Under", 55.5),
                ("Memphis Grizzlies", "Over", 50.5),
                ("Memphis Grizzlies", "Under", 50.5),
            },
        )
        self.assertTrue(all(r["timing_eligible"] and not r["training_eligible"] for r in team_rows))
        coverage = collector.team_totals_h2_coverage(self.payload, rows)
        self.assertTrue(coverage["requested"])
        self.assertTrue(coverage["market_returned"])
        self.assertEqual(coverage["teams"]["home"]["quotes"], 2)
        self.assertEqual(coverage["teams"]["away"]["quotes"], 2)

    def test_partial_team_total_h2_never_fabricates_away_lines(self):
        self.payload["bookmakers"][0]["markets"].append({
            "key": "team_totals_h2",
            "last_update": "2026-11-16T20:15:00Z",
            "outcomes": [
                {"name": "Over", "description": "Washington Wizards", "point": 55.5, "price": -110},
                {"name": "Under", "description": "Washington Wizards", "point": 55.5, "price": -110},
            ],
        })
        rows = collector.normalize(self.payload, self.captured, self.q2, self.q3, 30)
        coverage = collector.team_totals_h2_coverage(self.payload, rows)
        self.assertEqual(coverage["teams"]["home"]["status"], "available")
        self.assertEqual(coverage["teams"]["away"], {
            "name": "Memphis Grizzlies", "status": "no_usable_quote", "quotes": 0
        })
        self.assertFalse(any(r["team_total_team"] == "Memphis Grizzlies" for r in rows))

    def test_missing_team_total_market_explicitly_marked_not_returned(self):
        rows = collector.normalize(self.payload, self.captured, self.q2, self.q3, 30)
        coverage = collector.team_totals_h2_coverage(self.payload, rows)
        self.assertTrue(coverage["requested"])
        self.assertFalse(coverage["market_returned"])
        self.assertEqual(coverage["teams"]["home"]["status"], "not_returned")
        self.assertEqual(coverage["teams"]["away"]["status"], "not_returned")
        self.assertFalse(any(r["market"] == "team_totals_h2" for r in rows))

    def test_unattributed_team_total_quote_not_eligible(self):
        self.payload["bookmakers"][0]["markets"].append({
            "key": "team_totals_h2",
            "last_update": "2026-11-16T20:15:00Z",
            "outcomes": [{"name": "Over", "point": 53.5, "price": -110}],
        })
        rows = collector.normalize(self.payload, self.captured, self.q2, self.q3, 30)
        team_rows = [r for r in rows if r["market"] == "team_totals_h2"]
        self.assertEqual(len(team_rows), 1)
        self.assertIsNone(team_rows[0]["team_total_team"])
        self.assertFalse(team_rows[0]["timing_eligible"])
        self.assertEqual(
            collector.team_totals_h2_coverage(self.payload, rows)["teams"]["home"]["status"],
            "no_usable_quote",
        )

    def test_fixture_persists_market_attempt_even_when_missing(self):
        with tempfile.TemporaryDirectory() as temp:
            fixture = pathlib.Path(temp) / "fixture.json"
            output = pathlib.Path(temp) / "registry.json"
            fixture.write_text(json.dumps(self.payload))
            with mock.patch.object(sys, "argv", [
                "collector", "--fixture", str(fixture), "--out", str(output),
            ]):
                collector.main()
            registry = json.loads(output.read_text())
        self.assertEqual(len(registry["market_attempts"]), 1)
        attempt = registry["market_attempts"][0]
        self.assertIn("team_totals_h2", attempt["requested_markets"])
        self.assertTrue(attempt["team_totals_h2"]["requested"])
        self.assertEqual(attempt["team_totals_h2"]["teams"]["away"]["status"], "not_returned")
        self.assertTrue(all(not r["training_eligible"] for r in registry["records"]))

    def test_api_request_includes_second_half_team_totals(self):
        class OfflineResponse:
            headers = {}
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self): return json.dumps(self_payload).encode()
        self_payload = self.payload
        with mock.patch.object(collector.urllib.request, "urlopen", return_value=OfflineResponse()) as mock_open:
            collector.live_fetch(
                "test-event", "basketball_nba", "us", collector.MARKETS,
                "OFFLINE_FAKE_KEY", clock=lambda: self.captured,
            )
        request = mock_open.call_args.args[0]
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(request.full_url).query)
        self.assertEqual(query["markets"][0].split(","), list(collector.MARKETS))
        self.assertIn("team_totals_h2", query["markets"][0])
        self.assertNotIn("apiKey", query)

    def test_paid_mode_is_locked_even_with_opt_in(self):
        import sys
        with mock.patch.object(sys, "argv", ["collector", "--live", "--event-id", "test-event"]):
            with mock.patch.dict("os.environ", {"SHARPEDGE_ALLOW_PAID_ODDS": "YES"}):
                with self.assertRaises(SystemExit) as err:
                    collector.main()
                self.assertEqual(err.exception.code, 2)

if __name__ == "__main__":
    unittest.main()
