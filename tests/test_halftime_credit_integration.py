"""Offline collector integration tests: no database, network, or paid credits."""
import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import patch

root = Path(__file__).resolve().parents[1] / "scripts/odds"
import sys
sys.path.insert(0, str(root))
spec = importlib.util.spec_from_file_location("halftime_event_collector", root / "halftime_event_collector.py")
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)

class Cursor:
    def __init__(self, db): self.db, self.result = db, None
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def execute(self, sql, params):
        if sql.startswith("SELECT cap"):
            self.result = (self.db.cap, self.db.reserved)
        elif sql.startswith("SELECT 1"):
            self.result = (1,) if params[1] in self.db.requests else None
        elif sql.startswith("INSERT"):
            self.db.requests.add(params[1])
        elif sql.startswith("UPDATE sharpedge_odds_budget"):
            self.db.reserved += params[0]
    def fetchone(self): return self.result

class DB:
    def __init__(self): self.cap, self.reserved, self.requests = 30, 0, set()
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def transaction(self): return self
    def cursor(self): return Cursor(self)

class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.db = DB()
        self.connect = lambda *args, **kwargs: self.db
        self.env = patch.dict(os.environ, {"SHARPEDGE_ODDS_POSTGRES_DSN": "postgresql://test.invalid/db", "SHARPEDGE_ODDS_BUDGET_ID": "pilot"}, clear=False)
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_reservation_precedes_network_and_duplicate_is_denied(self):
        collector.reserve_live_budget("evt1", "basketball_nba", "us", 20, 30, self.connect)
        self.assertEqual(self.db.reserved, 20)
        with self.assertRaises(collector.credit_ledger.ReservationDenied):
            collector.reserve_live_budget("evt1", "basketball_nba", "us", 20, 30, self.connect)
        self.assertEqual(self.db.reserved, 20)

    def test_exhaustion_denies_second_event(self):
        collector.reserve_live_budget("evt1", "basketball_nba", "us", 20, 30, self.connect)
        with self.assertRaises(collector.credit_ledger.ReservationDenied):
            collector.reserve_live_budget("evt2", "basketball_nba", "us", 20, 30, self.connect)
        self.assertEqual(self.db.reserved, 20)

    def test_insufficient_pre_call_reservation_fails_without_connecting(self):
        def prohibited_connect(*args, **kwargs):
            self.fail("Should not connect to a database if charge is under-reserved")
        with self.assertRaises(collector.credit_ledger.ReservationDenied):
            collector.reserve_live_budget(
                "evt", "basketball_nba", "us", 2, 30, prohibited_connect,
            )
        self.assertEqual(self.db.reserved, 0)

    def test_multiple_regions_multiply_required_credit_hold(self):
        def prohibited_connect(*args, **kwargs):
            self.fail("Should not connect to a database if region hold is insufficient")
        with self.assertRaises(collector.credit_ledger.ReservationDenied):
            collector.reserve_live_budget(
                "evt", "basketball_nba", "us,uk", 3, 30, prohibited_connect,
            )

    def test_missing_shared_database_fails_closed(self):
        del os.environ["SHARPEDGE_ODDS_POSTGRES_DSN"]
        with self.assertRaises(collector.credit_ledger.ReservationDenied):
            collector.reserve_live_budget("evt", "basketball_nba", "us", 30, 30, self.connect)
        self.assertEqual(self.db.reserved, 0)

if __name__ == "__main__":
    unittest.main()
