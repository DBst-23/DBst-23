"""Real PostgreSQL credit reservation tests, including independent OS processes.

Run only against a disposable PostgreSQL database. Never calls an odds provider.
Requires SHARPEDGE_TEST_POSTGRES_DSN; CI provisions a local postgres service.
"""
import multiprocessing as mp
import os
import sys
from pathlib import Path
import unittest
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts/odds"))
import persistent_credit_ledger as ledger
import psycopg

DSN = os.environ.get("SHARPEDGE_TEST_POSTGRES_DSN")


def worker(dsn, budget, request, start, result):
    start.wait(timeout=15)
    try:
        with psycopg.connect(dsn, connect_timeout=5) as conn:
            ledger.reserve(conn, budget, request, 20, 30)
        result.put("reserved")
    except ledger.ReservationDenied as exc:
        result.put("denied:" + str(exc))
    except Exception as exc:
        result.put("error:" + repr(exc))


@unittest.skipUnless(DSN, "Requires disposable SHARPEDGE_TEST_POSTGRES_DSN")
class RealPostgresTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = psycopg.connect(DSN, connect_timeout=5)
        cls.conn.execute(ledger.SCHEMA)
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def setUp(self):
        self.budget = "test-" + uuid.uuid4().hex
        with self.conn.transaction():
            self.conn.execute("INSERT INTO sharpedge_odds_budget (budget_id, cap) VALUES (%s, 30)", (self.budget,))

    def tearDown(self):
        with self.conn.transaction():
            self.conn.execute("DELETE FROM sharpedge_odds_reservations WHERE budget_id = %s", (self.budget,))
            self.conn.execute("DELETE FROM sharpedge_odds_budget WHERE budget_id = %s", (self.budget,))

    def snapshot(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT reserved FROM sharpedge_odds_budget WHERE budget_id = %s", (self.budget,))
            reserved = cur.fetchone()[0]
            cur.execute("SELECT request_id FROM sharpedge_odds_reservations WHERE budget_id = %s", (self.budget,))
            rows = [r[0] for r in cur.fetchall()]
        return reserved, rows

    def race(self, request_a, request_b):
        ctx = mp.get_context("spawn")
        start = ctx.Event()
        result = ctx.Queue()
        processes = [ctx.Process(target=worker, args=(DSN, self.budget, request, start, result))
                     for request in (request_a, request_b)]
        for p in processes: p.start()
        start.set()
        outcomes = [result.get(timeout=25) for _ in processes]
        for p in processes:
            p.join(timeout=10)
            self.assertEqual(p.exitcode, 0)
        return outcomes

    def test_duplicate_race_one_reservation_only(self):
        outcomes = self.race("same-request", "same-request")
        self.assertEqual(sum(x == "reserved" for x in outcomes), 1, outcomes)
        self.assertEqual(sum(x.startswith("denied:Duplicate") for x in outcomes), 1, outcomes)
        self.assertEqual(self.snapshot(), (20, ["same-request"]))

    def test_budget_race_different_requests_one_only(self):
        outcomes = self.race("request-a", "request-b")
        self.assertEqual(sum(x == "reserved" for x in outcomes), 1, outcomes)
        self.assertEqual(sum(x.startswith("denied:Credit budget exceeded") for x in outcomes), 1, outcomes)
        reserved, rows = self.snapshot()
        self.assertEqual(reserved, 20)
        self.assertEqual(len(rows), 1)

    def test_duplicate_persists_across_connections(self):
        with psycopg.connect(DSN) as conn:
            ledger.reserve(conn, self.budget, "persist", 20, 30)
        with psycopg.connect(DSN) as conn:
            with self.assertRaisesRegex(ledger.ReservationDenied, "Duplicate"):
                ledger.reserve(conn, self.budget, "persist", 20, 30)
        self.assertEqual(self.snapshot(), (20, ["persist"]))


if __name__ == "__main__": unittest.main()
