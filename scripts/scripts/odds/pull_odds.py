# scripts/odds/pull_odds.py
import os
import json
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import requests


# -----------------------------
# Config (ENV)
# -----------------------------
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY", "").strip()
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "").strip()
AIRTABLE_ODDS_TABLE_ID = os.getenv("AIRTABLE_ODDS_TABLE_ID", "").strip()

ODDS_API_KEY = os.getenv("ODDS_API_KEY", "").strip()

# Optional filters (you can set these later in workflow env)
SPORT_KEY = os.getenv("SPORT_KEY", "basketball_nba").strip()
REGIONS = os.getenv("ODDS_REGIONS", "us").strip()  # us | eu | uk | au
MARKETS = os.getenv("ODDS_MARKETS", "h2h,spreads,totals").strip()
ODDS_FORMAT = os.getenv("ODDS_FORMAT", "american").strip()  # american | decimal
DATE_FORMAT = os.getenv("DATE_FORMAT", "iso").strip()

# Optional: where to also store raw snapshots (local repo artifact)
SNAPSHOT_DIR = os.getenv("SNAPSHOT_DIR", "data/odds_snapshots").strip()

# Odds API base (The Odds API is a common one; swap if you use another provider)
ODDS_API_BASE = os.getenv("ODDS_API_BASE", "https://api.the-odds-api.com/v4").strip()


# -----------------------------
# Helpers
# -----------------------------
def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def must_env(name: str, value: str) -> None:
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")


def mkdir_p(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def safe_get(d: Dict[str, Any], *keys: str, default=None):
    cur: Any = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def american_to_implied_prob(odds: Optional[float]) -> Optional[float]:
    if odds is None:
        return None
    try:
        odds = float(odds)
    except Exception:
        return None
    if odds == 0:
        return None
    if odds > 0:
        return 100.0 / (odds + 100.0)
    else:
        return (-odds) / ((-odds) + 100.0)


# -----------------------------
# Odds Pull (The Odds API format)
# -----------------------------
def fetch_odds() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Returns (events, meta)
    events: list of games with bookmakers and markets
    meta: request metadata
    """
    must_env("ODDS_API_KEY", ODDS_API_KEY)

    url = f"{ODDS_API_BASE}/sports/{SPORT_KEY}/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": REGIONS,
        "markets": MARKETS,
        "oddsFormat": ODDS_FORMAT,
        "dateFormat": DATE_FORMAT,
    }

    r = requests.get(url, params=params, timeout=20)
    meta = {
        "status_code": r.status_code,
        "url": r.url,
        "pulled_at_utc": utc_now_iso(),
    }

    if r.status_code != 200:
        meta["error"] = r.text[:500]
        return [], meta

    data = r.json()
    if not isinstance(data, list):
        meta["error"] = "Unexpected odds payload (not a list)"
        return [], meta

    return data, meta


# -----------------------------
# Normalize → ODDS_SNAPSHOTS rows
# -----------------------------
def normalize_to_rows(events: List[Dict[str, Any]], snapshot_ts: str) -> List[Dict[str, Any]]:
    """
    Converts provider payload into Airtable-ready rows.
    One row per (event, bookmaker, market, outcome/side).
    """
    rows: List[Dict[str, Any]] = []

    for ev in events:
        event_id = ev.get("id")
        commence_time = ev.get("commence_time")
        home = ev.get("home_team")
        away = ev.get("away_team")
        sport_title = ev.get("sport_title")
        sport_key = ev.get("sport_key")

        for bm in ev.get("bookmakers", []) or []:
            book_key = bm.get("key")
            book_title = bm.get("title")
            last_update = bm.get("last_update")

            for mkt in bm.get("markets", []) or []:
                market_key = mkt.get("key")  # h2h, spreads, totals, etc.
                outcomes = mkt.get("outcomes", []) or []

                for out in outcomes:
                    # Outcome shape differs by market:
                    # h2h: {name, price}
                    # spreads: {name, price, point}
                    # totals: {name: 'Over'/'Under', price, point}
                    name = out.get("name")
                    price = out.get("price")
                    point = out.get("point")  # spread/totals line

                    implied = american_to_implied_prob(price) if ODDS_FORMAT == "american" else None

                    # Build a stable "selection" string
                    selection = name
                    if market_key in ("spreads", "totals") and point is not None:
                        selection = f"{name} {point}"

                    row = {
                        "fields": {
                            # Core identifiers
                            "snapshot_ts_utc": snapshot_ts,
                            "event_id": event_id,
                            "sport_key": sport_key,
                            "sport_title": sport_title,
                            "commence_time": commence_time,

                            # Teams
                            "home_team": home,
                            "away_team": away,

                            # Source
                            "book_key": book_key,
                            "book_title": book_title,
                            "book_last_update": last_update,

                            # Market info
                            "market": market_key,
                            "selection": selection,
                            "outcome_name": name,
                            "line": point,  # spread/totals number, else None
                            "odds": price,

                            # Computed
                            "implied_prob": implied,
                        }
                    }
                    rows.append(row)

    return rows


# -----------------------------
# Airtable Upsert (simple create in batches)
# -----------------------------
def airtable_create_records(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    must_env("AIRTABLE_API_KEY", AIRTABLE_API_KEY)
    must_env("AIRTABLE_BASE_ID", AIRTABLE_BASE_ID)
    must_env("AIRTABLE_ODDS_TABLE_ID", AIRTABLE_ODDS_TABLE_ID)

    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_ODDS_TABLE_ID}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json",
    }

    # Airtable limit: 10 records per request
    batch_size = 10
    created = 0
    errors: List[Dict[str, Any]] = []

    for i in range(0, len(rows), batch_size):
        batch = rows[i : i + batch_size]
        payload = {"records": batch}
        resp = requests.post(url, headers=headers, json=payload, timeout=25)

        if resp.status_code not in (200, 201):
            errors.append(
                {
                    "status_code": resp.status_code,
                    "response": resp.text[:800],
                    "batch_start": i,
                    "batch_count": len(batch),
                }
            )
        else:
            data = resp.json()
            created += len(data.get("records", []))

        # small pause to avoid rate spikes
        time.sleep(0.15)

    return {"created": created, "errors": errors}


# -----------------------------
# Main
# -----------------------------
def main() -> None:
    # Minimal env validation
    must_env("AIRTABLE_API_KEY", AIRTABLE_API_KEY)
    must_env("AIRTABLE_BASE_ID", AIRTABLE_BASE_ID)
    must_env("AIRTABLE_ODDS_TABLE_ID", AIRTABLE_ODDS_TABLE_ID)

    snapshot_ts = utc_now_iso()

    events, meta = fetch_odds()

    # Store raw snapshot locally (optional, but very useful for audits/backtests)
    try:
        mkdir_p(SNAPSHOT_DIR)
        raw_path = os.path.join(SNAPSHOT_DIR, f"odds_raw_{snapshot_ts.replace(':','-')}.json")
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump({"meta": meta, "events": events}, f, ensure_ascii=False, indent=2)
        print(f"[OK] Wrote raw snapshot: {raw_path}")
    except Exception as e:
        print(f"[WARN] Failed writing raw snapshot: {e}")

    if not events:
        print(f"[WARN] No events pulled. Meta: {meta}")
        return

    rows = normalize_to_rows(events, snapshot_ts)
    print(f"[OK] Normalized rows: {len(rows)}")

    result = airtable_create_records(rows)
    print(f"[OK] Airtable created records: {result['created']}")

    if result["errors"]:
        print("[ERROR] Some Airtable batches failed:")
        for err in result["errors"][:5]:
            print(err)
        # Non-zero exit to make it obvious in Actions
        raise RuntimeError("Airtable batch errors occurred")


if __name__ == "__main__":
    main()