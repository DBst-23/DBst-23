"""One-time NBA team_totals_h2 provider coverage probe (Nov 27, 2026).

The independent SharpEdge collector on PR #53 remains explicitly paid-locked.
This single-event probe has two manually selected modes: free preflight and
ONE authorized, <=1-credit event-odds HTTP request. No retries or raw odds logs.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

SPORT = "basketball_nba"
BOOK = "williamhill_us"  # The Odds API catalogue labels this as Caesars (US)
MARKET = "team_totals_h2"
HOME = "New York Knicks"
AWAY = "Miami Heat"
EVENT_DATE_ET = "2026-11-27"
CONFIRM = "AUTHORIZE_ONE_CREDIT"
SCHEMA = "sharpedge_ci_crossrun"
UTC = dt.timezone.utc


class ProbeStop(Exception):
    pass


def as_utc(text):
    return dt.datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(UTC)


def fetch_json(url, api_key):
    """ONE network attempt; never print URLs, tokens, or response bodies."""
    request = urllib.request.Request(
        url,
        headers={"x-api-key": api_key, "User-Agent": "SharpEdge-Coverage-Probe/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            body = response.read()
            receipt_time = dt.datetime.now(UTC)
            headers = {k.lower(): v for k, v in response.headers.items()}
            return json.loads(body), headers, receipt_time
    except urllib.error.HTTPError as error:
        raise ProbeStop(f"Provider returned HTTP {error.code}; no retry.") from None
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as error:
        raise ProbeStop(f"Provider request failed ({type(error).__name__}); no retry.") from None


def select_target(events):
    if not isinstance(events, list):
        raise ProbeStop("Invalid free-event listing; no paid request")
    matches = [
        event for event in events
        if isinstance(event, dict)
        and event.get("home_team") == HOME
        and event.get("away_team") == AWAY
        and isinstance(event.get("commence_time"), str)
        and as_utc(event["commence_time"]).astimezone(
            ZoneInfo("America/New_York")
        ).strftime("%Y-%m-%d") == EVENT_DATE_ET
    ]
    if len(matches) != 1:
        raise ProbeStop(f"Expected exactly one {AWAY} @ {HOME} game on {EVENT_DATE_ET}; found {len(matches)}")
    event = matches[0]
    if not isinstance(event.get("id"), str) or not re.fullmatch(
        r"[a-zA-Z0-9_-]{8,80}", event["id"]
    ):
        raise ProbeStop("Invalid provider event ID")
    return event


def quote_coverage(payload, expected_event):
    """Do not print or store licensed odds. Only report team coverage booleans."""
    if not isinstance(payload, dict) or payload.get("id") != expected_event["id"]:
        raise ProbeStop("Paid response event-ID mismatch")
    books = payload.get("bookmakers")
    if not isinstance(books, list):
        raise ProbeStop("Invalid provider bookmakers response")
    if any(not isinstance(book, dict) or book.get("key") != BOOK for book in books):
        raise ProbeStop("Unexpected bookmaker in single-book probe")
    sides = {HOME: set(), AWAY: set()}
    found_market = False
    for book in books:
        for market in book.get("markets", []):
            if not isinstance(market, dict):
                raise ProbeStop("Invalid returned market")
            if market.get("key") != MARKET:
                raise ProbeStop("Unexpected market in single-market probe")
            found_market = True
            for outcome in market.get("outcomes", []):
                if not isinstance(outcome, dict):
                    raise ProbeStop("Invalid market outcome")
                side = outcome.get("description")
                name = outcome.get("name")
                if (
                    side in sides and name in ("Over", "Under")
                    and outcome.get("point") is not None
                    and outcome.get("price") is not None
                ):
                    sides[side].add(name)
    both = all(sides[name] == {"Over", "Under"} for name in (HOME, AWAY))
    partial = any(sides[name] for name in (HOME, AWAY))
    status = "both_teams" if both else "partial" if partial else "not_returned"
    return {"status": status, "market_found": found_market,
            "home_over_under": sorted(sides[HOME]),
            "away_over_under": sorted(sides[AWAY])}


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("preflight", "probe"), required=True)
    parser.add_argument("--confirmation", default="")
    args = parser.parse_args()

    key = os.environ.get("ODDS_API_KEY", "").strip()
    if not key:
        raise ProbeStop("ODDS_API_KEY secret unavailable; no paid request")
    # The official /events endpoint is free; use it to identify, not guess.
    events, free_headers, _ = fetch_json(
        "https://api.the-odds-api.com/v4/sports/basketball_nba/events", key,
    )
    if free_headers.get("x-requests-last") != "0":
        raise ProbeStop("Free event-listing quota metadata unexpected; refusing paid request")
    target = select_target(events)
    tip = as_utc(target["commence_time"])
    now = dt.datetime.now(UTC)
    minutes_since_tip = (now - tip).total_seconds() / 60
    print(f"TARGET: {AWAY} @ {HOME}; provider ID={target['id']}; tip UTC={tip.isoformat()}")
    print("FREE EVENTS PREFLIGHT: provider reports 0 credits spent.")

    if args.phase == "preflight":
        print("PREFLIGHT PASS: no paid odds calls, no database writes.")
        return

    # Single, explicitly acknowledged paid probe; never enable the locked collector.
    if args.confirmation != CONFIRM:
        raise ProbeStop("Probe authorization phrase missing; no paid request")
    if not (35 <= minutes_since_tip <= 90):
        raise ProbeStop("Outside bounded post-tip window (35-90 minutes); no paid request")
    remaining = free_headers.get("x-requests-remaining")
    if remaining is None or not remaining.isascii() or not remaining.isdecimal() or int(remaining) < 1:
        raise ProbeStop("Provider quota unknown/exhausted; no paid request")
    dsn = os.environ.get("SHARPEDGE_ODDS_POSTGRES_DSN", "").strip()
    if not dsn:
        raise ProbeStop("Neon DSN unavailable; no paid request")
    try:
        import psycopg
        # One persistent reservation, committed before HTTP. A rerun cannot call
        # the paid endpoint again for the same event/bookmaker/market.
        with psycopg.connect(dsn, connect_timeout=8, sslmode="require", autocommit=True) as conn:
            with conn.transaction():
                conn.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
                conn.execute(f"""CREATE TABLE IF NOT EXISTS {SCHEMA}.nba_teamtotal_onecall (
                    probe_id TEXT PRIMARY KEY,
                    event_id TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'reserved',
                    held_credits INTEGER NOT NULL DEFAULT 1 CHECK (held_credits = 1),
                    provider_charge INTEGER,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    finished_at TIMESTAMPTZ
                )""")
                probe_id = f"{SPORT}:{target['id']}:{BOOK}:{MARKET}"
                inserted = conn.execute(
                    f"INSERT INTO {SCHEMA}.nba_teamtotal_onecall (probe_id,event_id) "
                    "VALUES (%s,%s) ON CONFLICT DO NOTHING RETURNING probe_id",
                    (probe_id, target["id"]),
                ).fetchone()
                if inserted != (probe_id,):
                    raise ProbeStop("Single-event credit reservation already exists; no repeat HTTP request")
    except ProbeStop:
        raise
    except Exception:
        raise ProbeStop("Neon pre-call reservation failed; no paid request") from None

    # EXACTLY ONE chargeable request. One bookmaker and one market => <= 1 credit.
    query = urllib.parse.urlencode({
        "bookmakers": BOOK, "markets": MARKET,
        "oddsFormat": "american", "dateFormat": "iso",
    })
    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/events/{target['id']}/odds?{query}"
    try:
        payload, headers, received = fetch_json(url, key)
        usage = headers.get("x-requests-last")
        if usage is None or not usage.isascii() or not usage.isdecimal() or int(usage) > 1:
            raise ProbeStop("Provider reported missing/over-budget billing metadata; hold retained")
        coverage = quote_coverage(payload, target)
        charge = int(usage)
        # Detect impossible quota results; preserve hold on discrepancy.
        if charge == 0 and coverage["market_found"]:
            raise ProbeStop("Market returned but provider reported 0 credits; hold retained")
        with psycopg.connect(dsn, connect_timeout=8, sslmode="require") as conn:
            conn.execute(
                f"UPDATE {SCHEMA}.nba_teamtotal_onecall "
                "SET status=%s, provider_charge=%s, finished_at=NOW() "
                "WHERE probe_id=%s AND status='reserved'",
                (coverage["status"], charge, probe_id),
            )
        print(f"PROBE RESULT: {BOOK} ({'Caesars US'}), market={MARKET}")
        print(f"Home team coverage: {','.join(coverage['home_over_under']) or 'NOT RETURNED'}")
        print(f"Away team coverage: {','.join(coverage['away_over_under']) or 'NOT RETURNED'}")
        print(f"Both teams available: {coverage['status'] == 'both_teams'}")
        print(f"Provider-reported charge: {charge} credit(s), max authorized=1.")
        print("Scope: this proves only the selected game/instant, not Nevada-specific availability.")
        print(f"Response receipt UTC={received.isoformat()}; research-only, NOT training-eligible.")
    except Exception as error:
        # No second paid call, and the unique Neon reservation stays in place.
        print(f"PROBE INCONCLUSIVE: {type(error).__name__}; paid call will NOT be retried.")
        raise ProbeStop("One-time paid probe failed or inconclusive; test hold retained") from None


if __name__ == "__main__":
    try:
        run()
    except ProbeStop as exc:
        print(f"SAFE STOP: {exc}")
        sys.exit(1)
