"""Offline private response cache and deterministic historical odds request identity.

Use the SAME durable SQLite database as CreditLedger. No HTTP is performed here.
Never cache credentials, authorization headers or personal identifiers.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path
from urllib.parse import urlsplit

from modules.historical_odds_credit_guard import CreditLedger, ReservationConflict


def request_fingerprint(endpoint: str, params: dict) -> str:
    """Identity includes every query parameter, not just event/date."""
    url = urlsplit(endpoint)
    if url.scheme != "https" or not url.hostname or url.username or url.password or url.query or url.fragment:
        raise ValueError("Use a bare HTTPS endpoint without credentials or query string")
    if not isinstance(params, dict) or not params:
        raise ValueError("Explicit request parameters required")
    if any(not isinstance(k, str) or not k or k.lower() in {"apikey", "api_key", "token", "key"} for k in params):
        raise ValueError("Credentials must not be included in request identity")
    try:
        canonical = json.dumps({"endpoint": endpoint, "params": params},
                               sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("Parameters must be JSON serializable") from exc
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class PrivateOddsCache:
    def __init__(self, ledger: CreditLedger):
        self.ledger = ledger
        self.db = ledger.db
        self.db.execute("""CREATE TABLE IF NOT EXISTS private_response_cache (
            fingerprint TEXT PRIMARY KEY,
            response_json TEXT NOT NULL,
            response_sha256 TEXT NOT NULL,
            request_id TEXT NOT NULL UNIQUE,
            FOREIGN KEY(request_id) REFERENCES reservations(request_id))""")

    def get(self, fingerprint: str):
        row = self.db.execute("SELECT response_json,response_sha256 FROM private_response_cache WHERE fingerprint=?",
                              (fingerprint,)).fetchone()
        if row is None:
            return None
        raw, digest = row
        if hashlib.sha256(raw.encode()).hexdigest() != digest:
            raise ReservationConflict("Cache integrity failure; stop")
        return json.loads(raw)

    def put(self, request_id: str, fingerprint: str, response: dict | list) -> None:
        """Cache only after verified charge settlement, never an unreserved response."""
        raw = json.dumps(response, sort_keys=True, separators=(",", ":"), allow_nan=False)
        digest = hashlib.sha256(raw.encode()).hexdigest()
        self.db.execute("BEGIN IMMEDIATE")
        try:
            row = self.db.execute("SELECT fingerprint,status FROM reservations WHERE request_id=?",
                                  (request_id,)).fetchone()
            if row != (fingerprint, "settled"):
                raise ReservationConflict("Cache write requires matching settled reservation")
            prior = self.db.execute("SELECT response_sha256 FROM private_response_cache WHERE fingerprint=?",
                                    (fingerprint,)).fetchone()
            if prior and prior[0] != digest:
                raise ReservationConflict("Conflicting cached response; stop")
            if not prior:
                self.db.execute("INSERT INTO private_response_cache VALUES(?,?,?,?)",
                                (fingerprint, raw, digest, request_id))
            self.db.execute("COMMIT")
        except BaseException:
            if self.db.in_transaction:
                self.db.execute("ROLLBACK")
            raise

    def lookup_or_reserve(self, request_id: str, endpoint: str, params: dict,
                          worst_case_credits: int):
        """Return (cached_response, should_send_http, fingerprint).

        A duplicate with no cache is a HARD STOP, not permission to retry.
        Caller must use a verified provider charge and settle before cache.put.
        """
        fingerprint = request_fingerprint(endpoint, params)
        cached = self.get(fingerprint)
        if cached is not None:
            return cached, False, fingerprint
        allowed = self.ledger.reserve(request_id, fingerprint, worst_case_credits)
        if not allowed:
            raise ReservationConflict("Already reserved without cached response; manual reconciliation required")
        return None, True, fingerprint
