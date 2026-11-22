import tempfile
import unittest
from pathlib import Path
from modules.historical_odds_credit_guard import CreditLedger, BudgetExceeded, ReservationConflict


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "budget.sqlite"

    def tearDown(self):
        self.tmp.cleanup()

    def test_persistent_across_process_style_reopens(self):
        a = CreditLedger(self.path, cap=100, baseline_spent=20)
        self.assertTrue(a.reserve("a", "event1@time1", 60))
        a.close()
        b = CreditLedger(self.path, cap=100, baseline_spent=20)
        self.assertFalse(b.reserve("a", "event1@time1", 60))
        self.assertEqual(b.remaining(), 20)
        with self.assertRaises(BudgetExceeded):
            b.reserve("b", "event2", 21)
        b.settle("a", actual_credits=35)
        self.assertEqual(b.remaining(), 45)
        b.close()

    def test_unknown_charge_never_refunds(self):
        a = CreditLedger(self.path, cap=60)
        a.reserve("a", "one", 60)
        a.settle("a", actual_credits=None)
        self.assertEqual(a.remaining(), 0)
        with self.assertRaises(BudgetExceeded):
            a.reserve("b", "two", 1)
        a.close()

    def test_conflict_and_overage_fail_closed(self):
        a = CreditLedger(self.path, cap=100)
        a.reserve("a", "one", 30)
        with self.assertRaises(ReservationConflict):
            a.reserve("a", "changed", 30)
        with self.assertRaises(ReservationConflict):
            a.settle("a", actual_credits=31)
        self.assertEqual(a.remaining(), 70)
        a.settle("a", actual_credits=20)
        with self.assertRaises(ReservationConflict):
            a.settle("a", actual_credits=19)
        a.close()

    def test_configuration_cannot_reset_on_rerun(self):
        a = CreditLedger(self.path, cap=100, baseline_spent=40)
        a.close()
        with self.assertRaises(ReservationConflict):
            CreditLedger(self.path, cap=100, baseline_spent=0)

    def test_no_ephemeral_memory_ledger(self):
        with self.assertRaises(ValueError):
            CreditLedger(":memory:", cap=100)


if __name__ == "__main__":
    unittest.main()
