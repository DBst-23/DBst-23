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
                and q2_end <= updated < cutoff
                and captured_at < cutoff
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
    p.add_argument("--max-credits", type=int, default=60)
    p.add_argument("--budget-cap", type=int, default=60)
    p.add_argument("--ledger", type=Path, default=Path("private/odds_2l2_budget.json"))
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
        if not args.event_id:
            p.error("--event-id required for live requests")
        key = os.getenv("ODDS_API_KEY", "").strip()
        if not key:
            p.error("ODDS_API_KEY required; never commit it")
        # A durable single-writer ledger must be shared across runs. No
        # automatic retries. Reserve before the call, including failures.
        ledger = args.ledger
        if not ledger.exists():
            p.error("Initialize the persistent private budget ledger manually before paid requests")
        state = load_json(ledger, {})
        if state.get("version") != 1 or not isinstance(state.get("reserved_credits"), int):
            p.error("Invalid budget ledger")
        call_id = hashlib.sha256((args.sport + "|" + args.event_id + "|" + ",".join(MARKETS)).encode()).hexdigest()
        if call_id in state.get("requests", {}):
            p.error("Duplicate event/market request blocked by persistent ledger")
        if state["reserved_credits"] + args.max_credits > args.budget_cap:
            p.error("Persistent credit cap exceeded")
        state.setdefault("requests", {})[call_id] = {"reserved": args.max_credits, "at": iso(now), "status": "reserved"}
        state["reserved_credits"] += args.max_credits
        atomic_json(ledger, state)
        payload, headers = live_fetch(args.event_id, args.sport, args.regions, MARKETS, key)
        # Never persist API keys or full raw provider payload to public repositories.
        state["requests"][call_id]["status"] = "requested"
        for header in ("x-requests-last", "x-requests-remaining", "x-requests-used"):
            if header in headers:
                state["requests"][call_id][header] = headers[header]
        atomic_json(ledger, state)
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
