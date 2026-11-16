import unittest

from modules.historical_player_rebounds_odds import normalize_rebound_snapshot


def fixture():
    return {
        "timestamp": "2025-01-02T23:55:00Z",
        "data": {"id": "event1", "home_team": "Home", "away_team": "Away",
                 "commence_time": "2025-01-03T00:00:00Z",
                 "bookmakers": [{"key": "example_book", "title": "Example",
                   "markets": [{"key": "player_rebounds", "last_update": "2025-01-02T23:54:00Z",
                     "outcomes": [
                       {"name": "Over", "description": "Example Player", "point": 10.5, "price": 1.91},
                       {"name": "Under", "description": "Example Player", "point": 10.5, "price": 1.91}]}]}]}
    }


class HistoricalReboundOddsTests(unittest.TestCase):
    def test_extracts_both_sides_and_provenance(self):
        rows = normalize_rebound_snapshot(fixture(), event_id="event1",
                   requested_at="2025-01-02T23:55:00Z", decision_cutoff="2025-01-02T23:59:00Z")
        self.assertEqual([r["side"] for r in rows], ["Over", "Under"])
        self.assertEqual(rows[0]["line"], 10.5)
        self.assertEqual(rows[0]["status"], "RESEARCH_ONLY_UNVERIFIED_EXECUTABILITY")

    def test_rejects_future_snapshot(self):
        with self.assertRaises(ValueError):
            normalize_rebound_snapshot(fixture(), event_id="event1",
                 requested_at="2025-01-02T23:55:00Z", decision_cutoff="2025-01-02T23:50:00Z")

    def test_rejects_wrong_event(self):
        with self.assertRaises(ValueError):
            normalize_rebound_snapshot(fixture(), event_id="other",
                 requested_at="2025-01-02T23:55:00Z", decision_cutoff="2025-01-02T23:59:00Z")

    def test_rejects_late_market_update(self):
        f = fixture()
        f["data"]["bookmakers"][0]["markets"][0]["last_update"] = "2025-01-03T00:01:00Z"
        rows = normalize_rebound_snapshot(f, event_id="event1",
                   requested_at="2025-01-02T23:55:00Z", decision_cutoff="2025-01-02T23:59:00Z")
        self.assertEqual(rows, [])


if __name__ == "__main__":
    unittest.main()
