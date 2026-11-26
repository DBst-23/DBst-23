"""Durable credit reservation using a shared PostgreSQL database.

No network calls or credentials are used by this module itself. Every runner must
connect to the SAME persistent PostgreSQL database. A local SQLite file, GitHub
Actions artifact or checkout file is NOT a supported production backend.
"""
import hashlib
import json

SCHEMA = """
CREATE TABLE IF NOT EXISTS sharpedge_odds_budget (
    budget_id TEXT PRIMARY KEY,
    cap INTEGER NOT NULL CHECK (cap > 0),
    reserved INTEGER NOT NULL DEFAULT 0 CHECK (reserved >= 0)
);
CREATE TABLE IF NOT EXISTS sharpedge_odds_reservations (
    budget_id TEXT NOT NULL REFERENCES sharpedge_odds_budget(budget_id),
    request_id TEXT NOT NULL,
    credits INTEGER NOT NULL CHECK (credits > 0),
    status TEXT NOT NULL DEFAULT 'reserved',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (budget_id, request_id)
);
CREATE TABLE IF NOT EXISTS sharpedge_odds_usage_audit (
    budget_id TEXT NOT NULL,
    request_id TEXT NOT NULL,
    reserved_credits INTEGER NOT NULL CHECK (reserved_credits > 0),
    reported_charge INTEGER NOT NULL CHECK (reported_charge >= 0),
    provider_used INTEGER NOT NULL CHECK (provider_used >= 0),
    provider_remaining INTEGER NOT NULL CHECK (provider_remaining >= 0),
    observed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (budget_id, request_id),
    FOREIGN KEY (budget_id, request_id)
        REFERENCES sharpedge_odds_reservations(budget_id, request_id),
    CHECK (reported_charge <= reserved_credits)
);
"""

class ReservationDenied(Exception):
    pass

def request_identity(sport, event_id, regions, markets, odds_format="american"):
    """Canonical identity for one paid request; repeated attempts are duplicates."""
    if not sport or not event_id or not regions or not markets:
        raise ValueError("Missing request identity component")
    value = json.dumps([sport, event_id, regions, sorted(set(markets)), odds_format],
                       separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(value.encode()).hexdigest()

def reserve(connection, budget_id, request_id, credits, cap):
    """Atomically reserve BEFORE an HTTP call. Never refund ambiguous failures.

    Requires PostgreSQL, psycopg connection, and a pre-initialized budget row.
    Transaction serializes callers via SELECT ... FOR UPDATE; UNIQUE key blocks
    duplicate requests across runners, even after crashes.
    """
    if not budget_id or not request_id or not isinstance(credits, int) or isinstance(credits, bool) or credits <= 0:
        raise ValueError("Invalid reservation")
    if not isinstance(cap, int) or isinstance(cap, bool) or cap <= 0:
        raise ValueError("Invalid cap")
    with connection.transaction():
        with connection.cursor() as cur:
            cur.execute("SELECT cap, reserved FROM sharpedge_odds_budget WHERE budget_id = %s FOR UPDATE", (budget_id,))
            row = cur.fetchone()
            if row is None:
                raise ReservationDenied("Budget must be initialized by administrator")
            stored_cap, reserved = row
            if stored_cap != cap:
                raise ReservationDenied("Budget cap mismatch; refusing to change existing cap")
            cur.execute("SELECT 1 FROM sharpedge_odds_reservations WHERE budget_id = %s AND request_id = %s", (budget_id, request_id))
            if cur.fetchone() is not None:
                raise ReservationDenied("Duplicate paid request")
            if reserved + credits > stored_cap:
                raise ReservationDenied("Credit budget exceeded")
            cur.execute("INSERT INTO sharpedge_odds_reservations (budget_id, request_id, credits) VALUES (%s, %s, %s)",
                        (budget_id, request_id, credits))
            cur.execute("UPDATE sharpedge_odds_budget SET reserved = reserved + %s WHERE budget_id = %s",
                        (credits, budget_id))
    return True

def mark_result(connection, budget_id, request_id, status):
    if status not in ("requested", "failed", "unknown"):
        raise ValueError("Invalid status")
    with connection.transaction():
        with connection.cursor() as cur:
            cur.execute("UPDATE sharpedge_odds_reservations SET status = %s WHERE budget_id = %s AND request_id = %s",
                        (status, budget_id, request_id))
            if cur.rowcount != 1:
                raise ReservationDenied("Unknown reservation")

def reconcile_usage(connection, budget_id, request_id, report):
    """Append one validated provider usage report and finish the reservation.

    IMPORTANT: The full pre-call reservation remains charged against the local
    safety cap even if the provider billed less. Never silently free credits
    on a timeout, malformed header, or ambiguous outcome.

    The usage table is immutable per (budget_id, request_id). Status update
    and usage insert are in the same PostgreSQL transaction.
    """
    if not isinstance(report, dict) or set(report) != {"charge", "used", "remaining"}:
        raise ReservationDenied("Missing or malformed verified usage report")
    if any(type(report[key]) is not int or report[key] < 0 for key in report):
        raise ReservationDenied("Invalid usage values")
    if report["charge"] > report["used"]:
        raise ReservationDenied("Provider usage counters inconsistent")
    with connection.transaction():
        with connection.cursor() as cur:
            cur.execute(
                "SELECT credits, status FROM sharpedge_odds_reservations "
                "WHERE budget_id = %s AND request_id = %s FOR UPDATE",
                (budget_id, request_id),
            )
            row = cur.fetchone()
            if row is None:
                raise ReservationDenied("Unknown reservation")
            hold, status = row
            if status != "reserved":
                raise ReservationDenied("Reservation already finalized")
            if report["charge"] > hold:
                raise ReservationDenied("Provider usage exceeded reserved ceiling")
            cur.execute(
                "INSERT INTO sharpedge_odds_usage_audit "
                "(budget_id, request_id, reserved_credits, reported_charge, "
                "provider_used, provider_remaining) VALUES (%s, %s, %s, %s, %s, %s)",
                (budget_id, request_id, hold, report["charge"],
                 report["used"], report["remaining"]),
            )
            cur.execute(
                "UPDATE sharpedge_odds_reservations SET status = 'requested' "
                "WHERE budget_id = %s AND request_id = %s AND status = 'reserved'",
                (budget_id, request_id),
            )
            if cur.rowcount != 1:
                raise ReservationDenied("Reservation status changed")
    return True
