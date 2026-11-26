"""No-network, no-secret tests for the live *event* odds billing model."""
import importlib.util
from pathlib import Path
import unittest

script = Path(__file__).resolve().parents[1] / "scripts/odds/odds_credit_accounting.py"
spec = importlib.util.spec_from_file_location("odds_credit_accounting", script)
accounting = importlib.util.module_from_spec(spec)
spec.loader.exec_module(accounting)


class EventCreditTests(unittest.TestCase):
    markets = ("totals_h2", "spreads_h2", "h2h_h2", "team_totals_h2")

    @staticmethod
    def payload(keys):
        return {"id": "fixture-id", "bookmakers": [
            {"key": "book1", "markets": [{"key": key, "outcomes": []} for key in keys]},
            {"key": "book2", "markets": [{"key": key, "outcomes": []} for key in keys]},
        ]}

    @staticmethod
    def headers(last, used=100, remaining=900):
        return {"X-REQUESTS-LAST": str(last), "X-Requests-Used": str(used),
                "x-requests-remaining": str(remaining)}

    def test_four_markets_one_region_reserve_four(self):
        self.assertEqual(accounting.worst_case_credits(self.markets, "us"), 4)

    def test_four_markets_two_regions_reserve_eight(self):
        self.assertEqual(accounting.worst_case_credits(self.markets, "us,uk"), 8)

    def test_duplicate_regions_rejected(self):
        with self.assertRaises(accounting.CreditAccountingError):
            accounting.worst_case_credits(self.markets, "us,us")

    def test_duplicate_markets_rejected(self):
        with self.assertRaises(accounting.CreditAccountingError):
            accounting.worst_case_credits(("totals_h2", "totals_h2"), "us")

    def test_unsupported_region_fails_closed(self):
        with self.assertRaises(accounting.CreditAccountingError):
            accounting.worst_case_credits(self.markets, "somewhere")

    def test_blank_region_fails_closed(self):
        with self.assertRaises(accounting.CreditAccountingError):
            accounting.worst_case_credits(self.markets, "us,")

    def test_unsupported_market_fails_closed(self):
        with self.assertRaises(accounting.CreditAccountingError):
            accounting.worst_case_credits(("other",), "us")

    def test_provider_reports_two_unique_markets_across_two_books(self):
        result = accounting.reconcile_event_usage(
            self.headers(2), self.payload(("totals_h2", "spreads_h2")),
            self.markets, "us", 4,
        )
        self.assertEqual(result, {"charge": 2, "used": 100, "remaining": 900})

    def test_two_region_cost_uses_unique_markets(self):
        result = accounting.reconcile_event_usage(
            self.headers(4), self.payload(("totals_h2", "spreads_h2")),
            self.markets, "us,uk", 8,
        )
        self.assertEqual(result["charge"], 4)

    def test_all_four_markets_charged_four(self):
        result = accounting.reconcile_event_usage(
            self.headers(4), self.payload(self.markets), self.markets, "us", 4,
        )
        self.assertEqual(result["charge"], 4)

    def test_empty_bookmakers_explicit_zero_charge(self):
        result = accounting.reconcile_event_usage(
            self.headers(0), {"id": "fixture-id", "bookmakers": []},
            self.markets, "us", 4,
        )
        self.assertEqual(result["charge"], 0)

    def test_missing_usage_header_never_frees_held_credit(self):
        with self.assertRaises(accounting.CreditAccountingError):
            accounting.reconcile_event_usage({}, self.payload(self.markets),
                                             self.markets, "us", 3)

    def test_reported_charge_above_reserved_fails_closed(self):
        with self.assertRaises(accounting.CreditAccountingError):
            accounting.reconcile_event_usage(self.headers(5), self.payload(self.markets),
                                             self.markets, "us", 4)

    def test_underreservation_fails_before_reconciliation(self):
        with self.assertRaises(accounting.CreditAccountingError):
            accounting.reconcile_event_usage(self.headers(2), self.payload(("totals_h2",)),
                                             self.markets, "us", 2)

    def test_reported_charge_mismatch_market_payload_fails_closed(self):
        with self.assertRaises(accounting.CreditAccountingError):
            accounting.reconcile_event_usage(self.headers(3),
                                             self.payload(("totals_h2", "spreads_h2")),
                                             self.markets, "us", 4)

    def test_missing_bookmakers_fails_closed(self):
        with self.assertRaises(accounting.CreditAccountingError):
            accounting.reconcile_event_usage(self.headers(0), {"id": "fixture-id"},
                                             self.markets, "us", 4)

    def test_extra_unrequested_market_fails_closed(self):
        with self.assertRaises(accounting.CreditAccountingError):
            accounting.reconcile_event_usage(self.headers(2),
                                             self.payload(("totals_h2", "other")),
                                             self.markets, "us", 4)

    def test_non_numeric_usage_header_fails_closed(self):
        bad = self.headers(3)
        bad["X-Requests-Used"] = "abc"
        with self.assertRaises(accounting.CreditAccountingError):
            accounting.parse_usage_headers(bad)

    def test_negative_usage_header_fails_closed(self):
        with self.assertRaises(accounting.CreditAccountingError):
            accounting.parse_usage_headers(self.headers(-1))

    def test_charge_cannot_exceed_cumulative_used(self):
        with self.assertRaises(accounting.CreditAccountingError):
            accounting.parse_usage_headers(self.headers(3, used=2))

    def test_team_total_h2_market_missing_charge_three_not_four(self):
        # Asking for team_totals_h2 doesn't establish that bookmakers carry it.
        response = self.payload(("totals_h2", "spreads_h2", "h2h_h2"))
        result = accounting.reconcile_event_usage(
            self.headers(3), response, self.markets, "us", 4,
        )
        self.assertEqual(result["charge"], 3)

    def test_team_totals_both_teams_single_market_credit(self):
        response = {"id": "fixture-id", "bookmakers": [
            {"key": "book1", "markets": [
                {"key": "team_totals_h2", "outcomes": [
                    {"name": "Over", "description": "Home", "point": 54.5, "price": -110},
                    {"name": "Under", "description": "Home", "point": 54.5, "price": -110},
                    {"name": "Over", "description": "Away", "point": 49.5, "price": -110},
                    {"name": "Under", "description": "Away", "point": 49.5, "price": -110},
                ]}
            ]},
        ]}
        result = accounting.reconcile_event_usage(
            self.headers(1), response, self.markets, "us", 4,
        )
        self.assertEqual(result["charge"], 1)

    def test_team_total_only_one_team_still_single_market_credit(self):
        response = {"id": "fixture-id", "bookmakers": [
            {"key": "book1", "markets": [
                {"key": "team_totals_h2", "outcomes": [
                    {"name": "Over", "description": "Home", "point": 54.5, "price": -110},
                ]}
            ]},
        ]}
        result = accounting.reconcile_event_usage(
            self.headers(1), response, self.markets, "us", 4,
        )
        self.assertEqual(result["charge"], 1)

    def test_header_case_insensitivity_and_zero(self):
        self.assertEqual(accounting.parse_usage_headers(self.headers(0))["charge"], 0)


if __name__ == "__main__":
    unittest.main()
