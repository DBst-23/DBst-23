import tempfile
import unittest
from pathlib import Path

from modules.historical_odds_credit_guard import CreditLedger, ReservationConflict
from modules.historical_odds_private_cache import PrivateOddsCache, request_fingerprint

ENDPOINT = "https://api.the-odds-api.com/v4/historical/sports/basketball_nba/odds"
PARAMS = {"date": "2024-10-25T00:00:00Z", "markets": "player_rebounds", "regions": "us"}


class PrivateCacheTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "private.sqlite"
        self.ledger = CreditLedger(self.path, cap=100)
        self.cache = PrivateOddsCache(self.ledger)

    def tearDown(self):
        self.ledger.close()
        self.tmp.cleanup()

    def test_canonical_request_identity(self):
        self.assertEqual(request_fingerprint(ENDPOINT, PARAMS),
                         request_fingerprint(ENDPOINT, dict(reversed(list(PARAMS.items())))))
        self.assertNotEqual(request_fingerprint(ENDPOINT, PARAMS),
                            request_fingerprint(ENDPOINT, {**PARAMS, "date": "2024-10-26T00:00:00Z"}))
        with self.assertRaises(ValueError):
            request_fingerprint(ENDPOINT, {**PARAMS, "apiKey": "secret"})

    def test_cache_persists_and_avoids_second_charge(self):
        _, send, fp = self.cache.lookup_or_reserve("one", ENDPOINT, PARAMS, 30)
        self.assertTrue(send)
        self.ledger.settle("one", actual_credits=20)
        self.cache.put("one", fp, {"data": [1, 2]})
        self.ledger.close()
        self.ledger = CreditLedger(self.path, cap=100)
        self.cache = PrivateOddsCache(self.ledger)
        response, send, other_fp = self.cache.lookup_or_reserve("two", ENDPOINT, PARAMS, 30)
        self.assertEqual(response, {"data": [1, 2]})
        self.assertFalse(send)
        self.assertEqual(fp, other_fp)
        self.assertEqual(self.ledger.remaining(), 80)

    def test_duplicate_without_cache_fails_closed_across_ids(self):
        self.cache.lookup_or_reserve("one", ENDPOINT, PARAMS, 30)
        with self.assertRaises(ReservationConflict):
            self.cache.lookup_or_reserve("two", ENDPOINT, PARAMS, 30)
        self.assertEqual(self.ledger.remaining(), 70)

    def test_unsettled_cannot_cache_and_conflicts_rejected(self):
        _, _, fp = self.cache.lookup_or_reserve("one", ENDPOINT, PARAMS, 30)
        with self.assertRaises(ReservationConflict):
            self.cache.put("one", fp, {"x": 1})
        self.ledger.settle("one", actual_credits=30)
        self.cache.put("one", fp, {"x": 1})
        with self.assertRaises(ReservationConflict):
            self.cache.put("one", fp, {"x": 2})

    def test_different_fingerprints_reserve_independently(self):
        self.cache.lookup_or_reserve("one", ENDPOINT, PARAMS, 30)
        self.cache.lookup_or_reserve("two", ENDPOINT, {**PARAMS, "date": "2024-10-26T00:00:00Z"}, 30)
        self.assertEqual(self.ledger.remaining(), 40)


if __name__ == "__main__":
    unittest.main()
