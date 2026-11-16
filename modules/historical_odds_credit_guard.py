"""Fail-closed, persistent credit reservations for paid historical Odds API calls.

The SQLite DB MUST live on durable shared storage across runs, with a single
writer/transaction domain for every consumer of the same API key. An ephemeral
GitHub Actions workspace is NOT an acceptable ledger. This is an offline
component; it never sends HTTP requests.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path


class BudgetExceeded(RuntimeError):
    pass


class ReservationConflict(RuntimeError):
    pass


class CreditLedger:
    def __init__(self, path: str | Path, *, cap: int, baseline_spent: int = 0):
        if cap < 0 or not 0 <= baseline_spent <= cap:
            raise ValueError("Invalid cap or opening spent credits")
        self.path = str(path)
        if self.path == ":memory:":
            raise ValueError("An in-memory ledger is not persistent")
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        self.db.execute("PRAGMA busy_timeout=30000")
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("CREATE TABLE IF NOT EXISTS budget (id INTEGER PRIMARY KEY CHECK(id=1), cap INTEGER NOT NULL, baseline INTEGER NOT NULL)")
        self.db.execute("""CREATE TABLE IF NOT EXISTS reservations (
            request_id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL,
            reserved INTEGER NOT NULL CHECK(reserved > 0),
            actual INTEGER, status TEXT NOT NULL CHECK(status IN ('reserved','settled','uncertain')),
            CHECK(actual IS NULL OR (actual >= 0 AND actual <= reserved)))""")
        self.db.execute("BEGIN IMMEDIATE")
        try:
            row = self.db.execute("SELECT cap,baseline FROM budget WHERE id=1").fetchone()
            if row is None:
                self.db.execute("INSERT INTO budget VALUES(1,?,?)", (cap, baseline_spent))
            elif row != (cap, baseline_spent):
                raise ReservationConflict("Budget configuration changed; manual reconciliation required")
            self.db.execute("COMMIT")
        except BaseException:
            self.db.execute("ROLLBACK")
            raise

    def _used(self) -> int:
        return self.db.execute(
            "SELECT baseline + COALESCE((SELECT SUM(CASE WHEN status='settled' THEN actual ELSE reserved END) FROM reservations),0) FROM budget WHERE id=1"
        ).fetchone()[0]

    def remaining(self) -> int:
        return self.db.execute("SELECT cap FROM budget WHERE id=1").fetchone()[0] - self._used()

    def reserve(self, request_id: str, fingerprint: str, worst_case_credits: int) -> bool:
        """Reserve before HTTP. Returns False on exact duplicate; never re-send it."""
        if not request_id or not fingerprint or worst_case_credits <= 0:
            raise ValueError("Request ID, fingerprint and positive worst-case cost required")
        self.db.execute("BEGIN IMMEDIATE")
        try:
            prior = self.db.execute(
                "SELECT fingerprint,reserved FROM reservations WHERE request_id=?", (request_id,)
            ).fetchone()
            if prior:
                if prior != (fingerprint, worst_case_credits):
                    raise ReservationConflict("Request ID reused for different request or cost")
                self.db.execute("COMMIT")
                return False
            if self.remaining() < worst_case_credits:
                raise BudgetExceeded("Cross-run credit budget exhausted")
            self.db.execute("INSERT INTO reservations VALUES(?,?,?,NULL,'reserved')",
                            (request_id, fingerprint, worst_case_credits))
            self.db.execute("COMMIT")
            return True
        except BaseException:
            if self.db.in_transaction:
                self.db.execute("ROLLBACK")
            raise

    def settle(self, request_id: str, *, actual_credits: int | None) -> None:
        """Only settle using a verified provider charge; unknown stays fully reserved."""
        self.db.execute("BEGIN IMMEDIATE")
        try:
            row = self.db.execute("SELECT reserved,actual,status FROM reservations WHERE request_id=?",
                                  (request_id,)).fetchone()
            if row is None:
                raise ReservationConflict("Unknown request")
            reserved, prior_actual, status = row
            if status == "settled":
                if actual_credits != prior_actual:
                    raise ReservationConflict("Conflicting charge for settled request")
            elif actual_credits is None:
                self.db.execute("UPDATE reservations SET status='uncertain' WHERE request_id=?", (request_id,))
            elif isinstance(actual_credits, bool) or not isinstance(actual_credits, int) or not 0 <= actual_credits <= reserved:
                raise ReservationConflict("Charge invalid or exceeds reserved maximum; stop and reconcile")
            else:
                self.db.execute("UPDATE reservations SET actual=?,status='settled' WHERE request_id=?",
                                (actual_credits, request_id))
            self.db.execute("COMMIT")
        except BaseException:
            if self.db.in_transaction:
                self.db.execute("ROLLBACK")
            raise

    def close(self) -> None:
        self.db.close()
