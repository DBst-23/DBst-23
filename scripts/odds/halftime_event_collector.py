"""Step 2L.2: event-level halftime odds capture; PAPER ONLY.

Default mode is fixture/offline. Live calls require explicit opt-in, a persistent
budget ledger and a fixed event ID. No Airtable writes, wagers or signals.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request

try:
    from . import persistent_credit_ledger as credit_ledger
except ImportError:
    import persistent_credit_ledger as credit_ledger

BASE = "https://api.the-odds-api.com/v4"
MARKETS = ("totals_h2", "spreads_h2", "h2h_h2")
UTC = dt.timezone.utc


def timestamp(value):
    if not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            return None
        return parsed.astimezone(UTC)
    except (TypeError, ValueError):
        return None


def iso(value):
    return value.isoformat().replace("+00:00", "Z") if value else None


def load_json(path, default):
    return json.loads(path.read_text()) if path.exists() else default


def atomic_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


def normalize(payload, captured_at, q2_end, q3_start, latency_seconds):
    """No guessed halftime clocks. Reject quotes lacking per-market freshness."""
    if not isinstance(payload, dict) or not payload.get("id"):
        raise ValueError("Expected a single event object with id")
    if latency_seconds < 0:
        raise ValueError("Latency must be nonnegative")
    if q2_end and q3_start and q2_end >= q3_start:
        raise ValueError("Q2 end must precede Q3 start")
    if captured_at.tzinfo is None:
        raise ValueError("Capture timestamp must be timezone-aware")
    cutoff = q3_start - dt.timedelta(seconds=latency_seconds) if q3_start else None
    rows = []
    for book in payload.get("bookmakers", []):
        for market in book.get("markets", []):
            key = market.get("key")
            if key not in MARKETS:
                continue
            updated = timestamp(market.get("last_update"))
            eligible = bool(
                q2_end and cutoff and updated
                and q2_end <= captured_at < cutoff
                and q2_end <= updated <= captured_at
                and updated < cutoff
            )
            for outcome in market.get("outcomes", []):
                if outcome.get("price") is None:
                    continue
                rows.append({
                    "provider": "the_odds_api",
                    "event_id": payload["id"],
                    "sport_key": payload.get("sport_key"),
                    "home_team": payload.get("home_team"),
                    "away_team": payload.get("away_team"),
                    "commence_time": payload.get("commence_time"),
                    "book_key": book.get("key"),
                    "book_title": book.get("title"),
                    "market": key,
                    "outcome_name": outcome.get("name"),
                    "line": outcome.get("point"),
                    "odds": outcome["price"],
                    "market_last_update_utc": iso(updated),
                    "captured_at_utc": iso(captured_at),
                    "q2_end_utc": iso(q2_end),
                    "q3_start_utc": iso(q3_start),
                    "decision_cutoff_utc": iso(cutoff),
                    "timing_eligible": eligible,
                    "training_eligible": False,
                    "paper_only": True,
                    "registry_join_status": "UNMATCHED",
                })
    return rows


def live_fetch(event_id, sport, regions, markets, key):
    url = BASE + "/sports/" + urllib.parse.quote(sport, safe="") + "/events/" + urllib.parse.quote(event_id, safe="") + "/odds"
    query = urllib.parse.urlencode({
        "apiKey": key, "regions": regions, "markets": ",".join(markets),
        "oddsFormat": "american", "dateFormat": "iso",
    })
    request = urllib.request.Request(url + "?" + query, headers={"User-Agent": "SharpEdge-Paper-Research/2L2"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read()
            headers = dict(response.headers.items())
            return json.loads(body), headers
    except urllib.error.HTTPError as error:
        raise RuntimeError("Odds API HTTP " + str(error.code)) from None


def reserve_live_budget(event_id, sport, regions, credits, cap, connect):
    """Reserve once in shared PostgreSQL before any provider request.

    The connection factory is injected so offline tests never use a database.
    A missing/invalid DSN or uninitialized budget fails closed.
    """
    dsn = os.getenv("SHARPEDGE_ODDS_POSTGRES_DSN", "").strip()
    budget_id = os.getenv("SHARPEDGE_ODDS_BUDGET_ID", "").strip()
    if not dsn or not budget_id:
        raise credit_ledger.ReservationDenied("Shared PostgreSQL DSN and budget ID required")
    request_id = credit_ledger.request_identity(sport, event_id, regions, MARKETS)
    with connect(dsn, connect_timeout=5) as connection:
        credit_ledger.reserve(connection, budget_id, request_id, credits, cap)
    return budget_id, request_id


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--fixture", type=Path, help="Offline provider event JSON (default mode)")
    p.add_argument("--live", action="store_true", help="Opt in to one paid event call")
    p.add_argument("--event-id", help="Provider event ID; do not guess from team names")
    p.add_argument("--sport", default="basketball_nba")
    p.add_argument("--regions", default="us")
    p.add_argument("--q2-end", help="Licensed UTC ISO timestamp")
    p.add_argument("--q3-start", help="Licensed UTC ISO timestamp")
    p.add_argument("--latency-seconds", type=int, default=30)
    p.add_argument("--max-credits", type=int, default=30)
    p.add_argument("--budget-cap", type=int, default=30)
    p.add_argument("--out", type=Path, default=Path("private/halftime_registry_odds.json"))
    args = p.parse_args()
    if args.live == bool(args.fixture):
        p.error("Specify exactly one of --fixture or --live")
    if args.latency_seconds < 0 or args.max_credits < 1 or args.budget_cap < 1:
        p.error("Invalid latency or credit budget")
    q2, q3 = timestamp(args.q2_end), timestamp(args.q3_start)
    if bool(q2) != bool(q3) or (q2 and q2 >= q3):
        p.error("Supply both valid licensed Q2-end and Q3-start timestamps, or neither")
    now = dt.datetime.now(UTC)
    if args.live:
        if os.getenv("SHARPEDGE_ALLOW_PAID_ODDS") != "YES":
            p.error("Paid request disabled: set SHARPEDGE_ALLOW_PAID_ODDS=YES explicitly")
        # SAFETY LOCK: integration is review-only until a real PostgreSQL
        # concurrency test, provider cost verification and explicit paid approval.
        p.error("Paid mode locked: PostgreSQL integration is staged, not released")
        if not args.event_id:
            p.error("--event-id required for live requests")
        key = os.getenv("ODDS_API_KEY", "").strip()
        if not key:
            p.error("ODDS_API_KEY required; never commit it")
        try:
            import psycopg
        except ImportError:
            p.error("psycopg required for shared PostgreSQL budget reservation")
        try:
            budget_id, call_id = reserve_live_budget(
                args.event_id, args.sport, args.regions,
                args.max_credits, args.budget_cap, psycopg.connect,
            )
        except (credit_ledger.ReservationDenied, ValueError) as exc:
            p.error("Paid request denied: " + str(exc))
        # No automatic retry. A failed/ambiguous HTTP request consumes its
        # reservation; never refund credits based on uncertain provider billing.
        try:
            payload, headers = live_fetch(args.event_id, args.sport, args.regions, MARKETS, key)
        except Exception:
            with psycopg.connect(os.environ["SHARPEDGE_ODDS_POSTGRES_DSN"], connect_timeout=5) as connection:
                credit_ledger.mark_result(connection, budget_id, call_id, "unknown")
            raise
        with psycopg.connect(os.environ["SHARPEDGE_ODDS_POSTGRES_DSN"], connect_timeout=5) as connection:
            credit_ledger.mark_result(connection, budget_id, call_id, "requested")
    else:
        payload = load_json(args.fixture, None)
    if args.event_id and payload.get("id") != args.event_id:
        raise ValueError("Event ID mismatch")
    rows = normalize(payload, now, q2, q3, args.latency_seconds)
    registry = load_json(args.out, {"schema_version": 1, "records": []})
    existing = {hashlib.sha256(json.dumps(r, sort_keys=True).encode()).hexdigest() for r in registry["records"]}
    for row in rows:
        identity = hashlib.sha256(json.dumps(row, sort_keys=True).encode()).hexdigest()
        if identity not in existing:
            registry["records"].append(row)
            existing.add(identity)
    atomic_json(args.out, registry)
    print(json.dumps({"event_id": payload["id"], "quotes": len(rows),
                      "timing_eligible": sum(r["timing_eligible"] for r in rows),
                      "registry_records": len(registry["records"]),
                      "mode": "paper_only", "training_enabled": False}, indent=2))


if __name__ == "__main__":
    main()
