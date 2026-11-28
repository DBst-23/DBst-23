"""No-network safety checks for the one-shot 4-market NBA halftime collector."""
import datetime as dt
import importlib.util
import json
from pathlib import Path
from unittest import TestCase, main, mock

code = Path(__file__).resolve().parents[1] / "scripts/odds/nba_h2_four_market_probe.py"
spec = importlib.util.spec_from_file_location("nba_h2_four_market_probe", code)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

GAME = {
    "id": "aaaabbbbccccdddd0000111122223333",
    "home_team": "New York Knicks",
    "away_team": "Miami Heat",
    "commence_time": "2026-11-28T00:13:00Z",
}


def event_result(markets=probe.MARKETS):
    return {"id": GAME["id"], "home_team": GAME["home_team"],
            "away_team": GAME["away_team"], "bookmakers": [{
                "key": probe.BOOK,
                "markets": [{"key": market, "outcomes": [
                    {"name": "Over", "description": GAME["home_team"],
                     "point": 55.5, "price": -110},
                    {"name": "Under", "description": GAME["away_team"],
                     "point": 49.5, "price": -110},
                ]} for market in markets],
            }]}


class ProbeSafety(TestCase):
    def test_market_set_contains_all_four(self):
        self.assertEqual(probe.MARKETS, (
            "h2h_h2", "spreads_h2", "totals_h2", "team_totals_h2"
        ))
        self.assertEqual(probe.MAX_CREDITS, 4)

    def test_provider_response_four_markets(self):
        result, found = probe.summarize_odds(event_result(), GAME)
        self.assertEqual(found, set(probe.MARKETS))
        self.assertTrue(all(result[key]["market_returned"] for key in probe.MARKETS))
        self.assertEqual(result["team_totals_h2"]["usable_selections"], 2)

    def test_team_total_not_returned_is_not_fabricated(self):
        result, found = probe.summarize_odds(
            event_result(("h2h_h2", "spreads_h2", "totals_h2")), GAME
        )
        self.assertEqual(len(found), 3)
        self.assertFalse(result["team_totals_h2"]["market_returned"])
        self.assertEqual(result["team_totals_h2"]["usable_selections"], 0)

    def test_all_markets_missing(self):
        result, keys = probe.summarize_odds(
            {"id": GAME["id"], "home_team": GAME["home_team"],
             "away_team": GAME["away_team"], "bookmakers": []}, GAME
        )
        self.assertEqual(keys, set())
        self.assertTrue(all(not val["market_returned"] for val in result.values()))

    def test_outside_bookmaker_denied(self):
        payload = event_result()
        payload["bookmakers"][0]["key"] = "wrong_book"
        with self.assertRaises(probe.SafeStop):
            probe.summarize_odds(payload, GAME)

    def test_wrong_event_denied(self):
        payload = event_result()
        payload["id"] = "wrong-id"
        with self.assertRaises(probe.SafeStop):
            probe.summarize_odds(payload, GAME)

    def test_wrong_team_denied(self):
        payload = event_result()
        payload["home_team"] = "different"
        with self.assertRaises(probe.SafeStop):
            probe.summarize_odds(payload, GAME)

    def test_duplicate_market_denied(self):
        payload = event_result()
        payload["bookmakers"][0]["markets"].append(
            payload["bookmakers"][0]["markets"][0]
        )
        with self.assertRaises(probe.SafeStop):
            probe.summarize_odds(payload, GAME)

    def test_missing_team_description_never_becomes_valid_team_total(self):
        payload = event_result(("team_totals_h2",))
        for item in payload["bookmakers"][0]["markets"][0]["outcomes"]:
            item.pop("description")
        summary, keys = probe.summarize_odds(payload, GAME)
        self.assertEqual(keys, {"team_totals_h2"})
        self.assertEqual(summary["team_totals_h2"]["usable_selections"], 0)

    def test_quota_invalid_or_missing_denied(self):
        for data in ({}, {"x-requests-last": "-1"}, {"x-requests-last": "abc"}):
            with self.subTest(data=data):
                with self.assertRaises(probe.SafeStop):
                    probe.quota_int(data, "x-requests-last")

    def test_invalid_event_id_denied(self):
        with self.assertRaises(probe.SafeStop):
            probe.select_event([GAME], "NOT_A_REAL_EVENT!")
        with self.assertRaises(probe.SafeStop):
            probe.select_event([], GAME["id"])

    def test_free_listing_does_not_include_distant_future(self):
        now = probe.parse_utc(GAME["commence_time"])
        eligible = probe.free_event_list([GAME], now)
        self.assertEqual(len(eligible), 1)

    def test_probe_missing_confirmation_stops_before_any_network(self):
        with mock.patch.dict("os.environ", {"ODDS_API_KEY": "DUMMY_KEY"}):
            with mock.patch.object(probe, "request_json") as fetch:
                with self.assertRaises(probe.SafeStop):
                    probe.run(["--phase", "probe", "--event-id", GAME["id"]])
                fetch.assert_not_called()

    def test_preflight_uses_free_endpoint_only_no_database(self):
        with mock.patch.dict("os.environ", {"ODDS_API_KEY": "DUMMY_KEY"}):
            with mock.patch.object(probe, "request_json", return_value=(
                [GAME], {"x-requests-last": "0", "x-requests-remaining": "10"},
                dt.datetime.now(dt.timezone.utc),
            )) as fetch:
                with mock.patch.object(probe, "reserve_single_pilot") as db:
                    probe.run(["--phase", "preflight"])
                    self.assertEqual(fetch.call_count, 1)
                    self.assertTrue(fetch.call_args.args[0].endswith("/events"))
                    db.assert_not_called()

    def test_refuses_paid_outside_halftime_window(self):
        # Event was many hours ago; no DB and only the free listing touched.
        with mock.patch.dict("os.environ", {"ODDS_API_KEY": "DUMMY_KEY"}):
            with mock.patch.object(probe, "request_json", return_value=(
                [GAME], {"x-requests-last": "0", "x-requests-remaining": "10"},
                dt.datetime(2026, 11, 28, 7, 0, tzinfo=dt.timezone.utc)
            )) as fetch:
                with mock.patch.object(probe, "reserve_single_pilot") as reserve:
                    with self.assertRaises(probe.SafeStop):
                        probe.run(["--phase", "probe", "--event-id", GAME["id"],
                                   "--confirmation", probe.CONFIRMATION])
                    self.assertEqual(fetch.call_count, 1)
                    reserve.assert_not_called()

    def test_refuses_if_provider_remaining_quota_below_four(self):
        with mock.patch.dict("os.environ", {"ODDS_API_KEY": "DUMMY_KEY"}):
            with mock.patch.object(probe, "request_json", return_value=(
                [GAME], {"x-requests-last": "0", "x-requests-remaining": "3"},
                dt.datetime(2026, 11, 28, 1, 5, tzinfo=dt.timezone.utc),
            )) as fetch:
                with mock.patch.object(probe.dt, "datetime", wraps=dt.datetime) as mocked:
                    mocked.now.return_value = dt.datetime(
                        2026, 11, 28, 1, 5, tzinfo=dt.timezone.utc
                    )
                    with mock.patch.object(probe, "reserve_single_pilot") as reserve:
                        with self.assertRaises(probe.SafeStop):
                            probe.run(["--phase", "probe", "--event-id", GAME["id"],
                                       "--confirmation", probe.CONFIRMATION])
                        self.assertEqual(fetch.call_count, 1)
                        reserve.assert_not_called()


if __name__ == "__main__":
    main()
