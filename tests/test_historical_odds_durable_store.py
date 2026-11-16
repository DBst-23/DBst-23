"""Offline persistence contract tests. No network or API credits."""
import tempfile
import unittest
from pathlib import Path

from modules.historical_odds_credit_guard import ReservationConflict
from modules.historical_odds_durable_store import StorageNotProvisioned, open_durable_store


class DurableStoreTests(unittest.TestCase):
    def test_requires_provisioned_path(self):
        with self.assertRaises(StorageNotProvisioned):
            open_durable_store(cap=10, baseline_spent=0, environ={})

    def test_rejects_ephemeral_actions_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.sqlite"
            path.touch()
            with self.assertRaises(StorageNotProvisioned):
                open_durable_store(cap=10, baseline_spent=0, environ={
                    "SHARPEDGE_ODDS_LEDGER_PATH": str(path),
                    "GITHUB_ACTIONS": "true", "GITHUB_WORKSPACE": directory})

    def test_reopen_preserves_reservation_and_cached_response(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.sqlite"
            path.touch()
            env = {"SHARPEDGE_ODDS_LEDGER_PATH": str(path)}
            ledger, cache = open_durable_store(cap=10, baseline_spent=0, environ=env)
            endpoint = "https://api.the-odds-api.com/v4/historical/sports/basketball_nba/events"
            params = {"date": "2024-11-01T12:00:00Z", "markets": "player_rebounds"}
            cached, send, fingerprint = cache.lookup_or_reserve("req-1", endpoint, params, 3)
            self.assertIsNone(cached)
            self.assertTrue(send)
            ledger.settle("req-1", actual_credits=2)
            cache.put("req-1", fingerprint, {"response": []})
            self.assertEqual(ledger.remaining(), 8)
            ledger.close()
            ledger2, cache2 = open_durable_store(cap=10, baseline_spent=0, environ=env)
            try:
                value, send, _ = cache2.lookup_or_reserve("req-2", endpoint, params, 3)
                self.assertEqual(value, {"response": []})
                self.assertFalse(send)
                self.assertEqual(ledger2.remaining(), 8)
                with self.assertRaises(ReservationConflict):
                    open_durable_store(cap=11, baseline_spent=0, environ=env)
            finally:
                ledger2.close()

    def test_uncertain_reservation_survives_restart_and_blocks_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.sqlite"
            path.touch()
            env = {"SHARPEDGE_ODDS_LEDGER_PATH": str(path)}
            endpoint = "https://api.the-odds-api.com/v4/historical/sports/basketball_nba/events"
            params = {"date": "2024-11-02T12:00:00Z"}
            ledger, cache = open_durable_store(cap=5, baseline_spent=0, environ=env)
            cache.lookup_or_reserve("req-1", endpoint, params, 4)
            ledger.close()
            ledger2, cache2 = open_durable_store(cap=5, baseline_spent=0, environ=env)
            try:
                self.assertEqual(ledger2.remaining(), 1)
                with self.assertRaises(ReservationConflict):
                    cache2.lookup_or_reserve("req-2", endpoint, params, 4)
            finally:
                ledger2.close()


if __name__ == "__main__":
    unittest.main()
