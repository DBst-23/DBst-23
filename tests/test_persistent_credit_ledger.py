"""Offline contract tests for atomic credit ledger. No database or paid API needed."""
import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[1] / "scripts/odds/persistent_credit_ledger.py"
spec = importlib.util.spec_from_file_location("persistent_credit_ledger", path)
ledger = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ledger)

class Cursor:
    def __init__(self, state):
        self.state = state
        self.result = None
        self.rowcount = 0
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def execute(self, sql, params):
        if sql.startswith("SELECT cap"):
            self.result = (self.state["cap"], self.state["reserved"]) if self.state["exists"] else None
        elif sql.startswith("SELECT 1"):
            self.result = (1,) if params[1] in self.state["requests"] else None
        elif sql.startswith("INSERT"):
            self.state["requests"].add(params[1])
        elif sql.startswith("UPDATE sharpedge_odds_budget"):
            self.state["reserved"] += params[0]
        elif sql.startswith("UPDATE sharpedge_odds_reservations"):
            self.rowcount = int(params[2] in self.state["requests"])
    def fetchone(self): return self.result

class Transaction:
    def __init__(self, state): self.state = state
    def __enter__(self): return self
    def __exit__(self, *args): pass

class Connection:
    def __init__(self, cap=30, exists=True):
        self.state = {"cap": cap, "reserved": 0, "requests": set(), "exists": exists}
    def transaction(self): return Transaction(self.state)
    def cursor(self): return Cursor(self.state)

class LedgerTests(unittest.TestCase):
    def test_duplicate_rejected(self):
        db = Connection()
        ledger.reserve(db, "pilot", "request1", 10, 30)
        with self.assertRaises(ledger.ReservationDenied):
            ledger.reserve(db, "pilot", "request1", 10, 30)
        self.assertEqual(db.state["reserved"], 10)
    def test_budget_exhaustion(self):
        db = Connection()
        ledger.reserve(db, "pilot", "request1", 20, 30)
        with self.assertRaises(ledger.ReservationDenied):
            ledger.reserve(db, "pilot", "request2", 20, 30)
        self.assertEqual(db.state["reserved"], 20)
    def test_missing_budget_fail_closed(self):
        with self.assertRaises(ledger.ReservationDenied):
            ledger.reserve(Connection(exists=False), "pilot", "r", 1, 30)
    def test_cap_mismatch_fail_closed(self):
        with self.assertRaises(ledger.ReservationDenied):
            ledger.reserve(Connection(), "pilot", "r", 1, 31)
    def test_identity_canonical_and_region_sensitive(self):
        a = ledger.request_identity("basketball_nba", "evt", "us", ["totals_h2", "spreads_h2"])
        b = ledger.request_identity("basketball_nba", "evt", "us", ["spreads_h2", "totals_h2"])
        c = ledger.request_identity("basketball_nba", "evt", "us2", ["spreads_h2", "totals_h2"])
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
    def test_invalid_amount(self):
        with self.assertRaises(ValueError):
            ledger.reserve(Connection(), "pilot", "r", -1, 30)
    def test_unknown_reservation_status_rejected(self):
        with self.assertRaises(ledger.ReservationDenied):
            ledger.mark_result(Connection(), "pilot", "absent", "requested")

if __name__ == "__main__":
    unittest.main()
