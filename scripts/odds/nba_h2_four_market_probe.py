"""Manual, single-shot The Odds API NBA second-half four-market coverage test.

This is NOT the locked PR #53 collector, a scheduler, or a betting signal.
One bookmaker, one event, one request; all output to PUBLIC GitHub logs is
coverage-only. No raw prices/outcomes are logged or persisted.
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

UTC = dt.timezone.utc
SPORT = "basketball_nba"
BOOK = "williamhill_us"
MARKETS = ("h2h_h2", "spreads_h2", "totals_h2", "team_totals_h2")
MAX_CREDITS = len(MARKETS)
CONFIRMATION = "AUTHORIZE_FOUR_CREDITS_HALFTIME"
SCHEMA = "sharpedge_ci_crossrun"
ID_PATTERN = re.compile(r"[A-Za-z0-9_-]{8,80}\Z")


class SafeStop(Exception):
    pass


def parse_utc(value):
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise SafeStop("Provider timestamp missing timezone")
    return parsed.astimezone(UTC)


def request_json(url, api_key):
    """One HTTP request, no retry, x-api-key header (never a query parameter)."""
    request = urllib.request.Request(url, headers={
        "x-api-key": api_key, "User-Agent": "SharpEdge-Halftime-Research/one-shot",
    })
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            body = response.read()
            received_at = dt.datetime.now(UTC)
            headers = {str(k).lower(): str(v) for k, v in response.headers.items()}
            return json.loads(body), headers, received_at
    except urllib.error.HTTPError as exc:
        raise SafeStop(f"Provider HTTP {exc.code}; no retry") from None
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        raise SafeStop("Provider request failed; no retry") from None


def quota_int(headers, key):
    value = headers.get(key)
    if not isinstance(value, str) or not value.isascii() or not value.isdecimal():
        raise SafeStop("Provider quota headers missing or invalid")
    return int(value)


def select_event(events, event_id):
    if not isinstance(events, list):
        raise SafeStop("Invalid events payload")
    if not ID_PATTERN.fullmatch(event_id):
        raise SafeStop("Event ID invalid")
    matches = [event for event in events
               if isinstance(event, dict) and event.get("id") == event_id]
    if len(matches) != 1:
        raise SafeStop("Event not uniquely found in live free-event feed")
    game = matches[0]
    if (not isinstance(game.get("home_team"), str)
            or not isinstance(game.get("away_team"), str)
            or game["home_team"] == game["away_team"]
            or not isinstance(game.get("commence_time"), str)):
        raise SafeStop("Incomplete event metadata")
    return game


def summarize_odds(payload, game):
    """Collect only per-market coverage; NEVER return prices or payload excerpts."""
    if not isinstance(payload, dict) or payload.get("id") != game["id"]:
        raise SafeStop("Paid event ID does not match free-event identity")
    if (payload.get("home_team") != game["home_team"]
            or payload.get("away_team") != game["away_team"]):
        raise SafeStop("Paid event teams do not match preflight")
    books = payload.get("bookmakers")
    if not isinstance(books, list) or any(
        not isinstance(b, dict) or b.get("key") != BOOK for b in books
    ):
        raise SafeStop("Unexpected bookmaker response")
    if len(books) > 1:
        raise SafeStop("Duplicate bookmaker response")
    returned = set()
    report = {market: {"market_returned": False, "usable_selections": 0}
              for market in MARKETS}
    for book in books:
        markets = book.get("markets")
        if not isinstance(markets, list):
            raise SafeStop("Malformed markets")
        for entry in markets:
            if not isinstance(entry, dict) or entry.get("key") not in MARKETS:
                raise SafeStop("Unexpected provider market")
            key = entry["key"]
            if key in returned:
                raise SafeStop("Duplicate market in bookmaker payload")
            returned.add(key)
            outcomes = entry.get("outcomes")
            if not isinstance(outcomes, list):
                raise SafeStop("Malformed outcomes")
            report[key]["market_returned"] = True
            for outcome in outcomes:
                if not isinstance(outcome, dict):
                    raise SafeStop("Malformed outcome")
                if outcome.get("price") is None:
                    continue
                if key in ("spreads_h2", "totals_h2", "team_totals_h2") and outcome.get("point") is None:
                    continue
                if key == "team_totals_h2":
                    if (outcome.get("description") not in
                            (game["home_team"], game["away_team"])
                            or outcome.get("name") not in ("Over", "Under")):
                        continue
                report[key]["usable_selections"] += 1
    # Distinguish a market absent from one present but unparseable.
    return report, returned


def free_event_list(events, now):
    if not isinstance(events, list):
        raise SafeStop("Malformed free-event listing")
    eligible = []
    for e in events:
        if not isinstance(e, dict):
            continue
        try:
            tip = parse_utc(e["commence_time"])
        except (KeyError, TypeError, ValueError, AttributeError, SafeStop):
            continue
        if (-120 <= (tip - now).total_seconds() / 60 <= 1440
                and isinstance(e.get("id"), str)
                and ID_PATTERN.fullmatch(e["id"])
                and isinstance(e.get("home_team"), str)
                and isinstance(e.get("away_team"), str)):
            eligible.append((tip, e))
    return sorted(eligible, key=lambda item: item[0])[:20]


def reserve_single_pilot(psycopg, dsn, event_id):
    """Isolated DB schema with GLOBAL four-credit lifetime cap, not one cap per run."""
    try:
        with psycopg.connect(dsn, connect_timeout=8, sslmode="require", autocommit=True) as conn:
            with conn.transaction():
                conn.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
                conn.execute(f"""CREATE TABLE IF NOT EXISTS {SCHEMA}.nba_h2_pilot_budget (
                    budget_id TEXT PRIMARY KEY,
                    cap INTEGER NOT NULL CHECK (cap = 4),
                    held INTEGER NOT NULL DEFAULT 0 CHECK (held >= 0 AND held <= 4)
                )""")
                conn.execute(f"""CREATE TABLE IF NOT EXISTS {SCHEMA}.nba_h2_pilot_calls (
                    request_id TEXT PRIMARY KEY,
                    event_id TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'reserved',
                    held_credits INTEGER NOT NULL CHECK (held_credits = 4),
                    reported_charge INTEGER,
                    coverage_json JSONB,
                    received_utc TIMESTAMPTZ,
                    created_utc TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )""")
                conn.execute(
                    f"INSERT INTO {SCHEMA}.nba_h2_pilot_budget (budget_id,cap) "
                    "VALUES ('single-pilot-v1',4) ON CONFLICT DO NOTHING"
                )
                row = conn.execute(
                    f"SELECT cap,held FROM {SCHEMA}.nba_h2_pilot_budget "
                    "WHERE budget_id='single-pilot-v1' FOR UPDATE"
                ).fetchone()
                if row != (4, 0):
                    raise SafeStop("Pilot cap already reserved or invalid; no second paid request")
                rid = f"{SPORT}:{event_id}:{BOOK}:{','.join(sorted(MARKETS))}"
                inserted = conn.execute(
                    f"INSERT INTO {SCHEMA}.nba_h2_pilot_calls "
                    "(request_id,event_id,held_credits) VALUES (%s,%s,4) "
                    "ON CONFLICT DO NOTHING RETURNING request_id", (rid, event_id)
                ).fetchone()
                if inserted != (rid,):
                    raise SafeStop("Duplicate request blocked before paid call")
                updated = conn.execute(
                    f"UPDATE {SCHEMA}.nba_h2_pilot_budget SET held=held+4 "
                    "WHERE budget_id='single-pilot-v1' AND held+4<=cap"
                )
                if updated.rowcount != 1:
                    raise SafeStop("Credit ceiling exceeded")
        return rid
    except SafeStop:
        raise
    except Exception:
        raise SafeStop("Durable credit reservation unavailable; no paid call") from None


def record_report(psycopg, dsn, rid, report, usage, received):
    try:
        with psycopg.connect(dsn, connect_timeout=8, sslmode="require") as conn:
            updated = conn.execute(
                f"UPDATE {SCHEMA}.nba_h2_pilot_calls "
                "SET status='verified', reported_charge=%s, coverage_json=%s::jsonb, "
                "received_utc=%s WHERE request_id=%s AND status='reserved'",
                (usage["last"], json.dumps(report, sort_keys=True), received, rid)
            )
            if updated.rowcount != 1:
                raise SafeStop("Reservation finalization refused")
    except Exception:
        raise SafeStop("Coverage persistence failed; credit hold retained") from None


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("preflight", "probe"), required=True)
    parser.add_argument("--event-id", default="")
    parser.add_argument("--confirmation", default="")
    args = parser.parse_args(argv)
    key = os.environ.get("ODDS_API_KEY", "").strip()
    if not key:
        raise SafeStop("ODDS_API_KEY unavailable")
    if args.phase == "probe" and args.confirmation != CONFIRMATION:
        raise SafeStop("Four-credit authorization and halftime confirmation missing")
    if args.phase == "probe" and not ID_PATTERN.fullmatch(args.event_id):
        raise SafeStop("Valid event ID required before paid call")
    events, hdr, _ = request_json(
        "https://api.the-odds-api.com/v4/sports/basketball_nba/events", key
    )
    if quota_int(hdr, "x-requests-last") != 0:
        raise SafeStop("Free event listing reported nonzero charge")
    now = dt.datetime.now(UTC)
    if args.phase == "preflight":
        print("FREE PREFLIGHT: 0 credits charged; NO database writes or paid odds.")
        print("Eligible event IDs (copy the correct ID for the manual halftime probe):")
        for tip, game in free_event_list(events, now):
            print(f"{game['id']} | {game['away_team']} @ {game['home_team']} | tip UTC {tip.isoformat()}")
        return
    game = select_event(events, args.event_id)
    tip = parse_utc(game["commence_time"])
    age = (now - tip).total_seconds() / 60
    if not 35 <= age <= 100:
        raise SafeStop("Outside 35–100 minutes post-scheduled tip; no paid call")
    if quota_int(hdr, "x-requests-remaining") < MAX_CREDITS:
        raise SafeStop("Provider remaining credits less than four-credit ceiling")
    dsn = os.environ.get("SHARPEDGE_ODDS_POSTGRES_DSN", "").strip()
    if not dsn:
        raise SafeStop("Neon connection unavailable; no paid call")
    import psycopg
    rid = reserve_single_pilot(psycopg, dsn, game["id"])
    # Exactly ONE billed request. No retry on HTTP, parsing, database or quota errors.
    params = urllib.parse.urlencode({
        "bookmakers": BOOK, "markets": ",".join(MARKETS),
        "oddsFormat": "american", "dateFormat": "iso",
    })
    url = (f"https://api.the-odds-api.com/v4/sports/{SPORT}/"
           f"events/{game['id']}/odds?{params}")
    try:
        payload, headers, captured = request_json(url, key)
        report, returned = summarize_odds(payload, game)
        charge = quota_int(headers, "x-requests-last")
        if charge != len(returned) or charge > MAX_CREDITS:
            raise SafeStop("Provider billing mismatched market count; hold retained")
        used = quota_int(headers, "x-requests-used")
        quota_int(headers, "x-requests-remaining")
        if charge > used:
            raise SafeStop("Provider charge exceeds used counter")
        record_report(psycopg, dsn, rid, report, {"last": charge}, captured)
    except Exception as exc:
        # The reservation remains durable even if the call's billing is ambiguous.
        print(f"INCONCLUSIVE: {type(exc).__name__}. No retry; four-credit hold retained.")
        raise SafeStop("One paid provider call may have occurred; do NOT rerun") from None
    print(f"PAID PROBE COMPLETED | {game['away_team']} @ {game['home_team']}")
    print(f"Bookmaker={BOOK}; actual provider charge={charge}; held safety cap=4.")
    for market in MARKETS:
        row = report[market]
        print(f"{market}: {'RETURNED' if row['market_returned'] else 'NOT RETURNED'}; "
              f"usable selections={row['usable_selections']}")
    print(f"Response received UTC={captured.isoformat()}; research only.")
    print("Prices deliberately withheld from PUBLIC GitHub logs; no training or bets.")


if __name__ == "__main__":
    try:
        run()
    except SafeStop as error:
        print(f"SAFE STOP: {error}")
        sys.exit(1)
