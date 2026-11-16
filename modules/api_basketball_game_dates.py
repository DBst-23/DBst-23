"""Attach verified API-Basketball schedule dates to normalized player rebound rows.

Fetch /games?id=<id> from API-Basketball v1. Never infer dates from game IDs,
player statistics, or local system time. A missing or conflicting schedule date
fails closed. All requests use APISPORTS_BASKETBALL_KEY from the environment.
"""
from __future__ import annotations

import json
import os
from datetime import date, datetime
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://v1.basketball.api-sports.io"
KEY_ENV = "APISPORTS_BASKETBALL_KEY"


class GameDateVerificationError(ValueError):
    """Schedule provenance could not be verified."""


def fetch_game_schedule(game_id: int) -> dict:
    """Retrieve one game's schedule from the authenticated Basketball API."""
    if type(game_id) is not int or game_id <= 0:
        raise GameDateVerificationError("game_id must be a positive integer")
    key = os.environ.get(KEY_ENV)
    if not key:
        raise GameDateVerificationError(f"Missing environment variable {KEY_ENV}")
    url = BASE_URL + "/games?" + urlencode({"id": game_id})
    request = Request(url, headers={"x-apisports-key": key}, method="GET")
    try:
        with urlopen(request, timeout=20) as response:
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError, ValueError) as exc:
        raise GameDateVerificationError(
            f"Schedule lookup failed for game {game_id}: {type(exc).__name__}"
        ) from exc
    return payload


def verified_game_date(payload: dict, game_id: int) -> str:
    """Accept exactly one matching schedule game with a valid explicit date."""
    if not isinstance(payload, dict) or payload.get("errors"):
        raise GameDateVerificationError("Invalid schedule response or API errors")
    matches = payload.get("response")
    if not isinstance(matches, list) or len(matches) != 1:
        raise GameDateVerificationError("Expected exactly one schedule game")
    game = matches[0]
    if not isinstance(game, dict) or type(game.get("id")) is not int or game["id"] != game_id:
        raise GameDateVerificationError("Schedule game ID mismatch")
    raw = game.get("date")
    if not isinstance(raw, str) or not raw:
        raise GameDateVerificationError("Missing schedule date")
    try:
        # API-Basketball schedule dates may be ISO timestamps or YYYY-MM-DD.
        if len(raw) == 10:
            parsed = date.fromisoformat(raw)
        else:
            parsed = datetime.fromisoformat(raw.replace("Z", "+00:00")).date()
        if parsed.isoformat() != raw[:10]:
            raise ValueError("Noncanonical date")
    except ValueError as exc:
        raise GameDateVerificationError("Invalid ISO schedule date") from exc
    return parsed.isoformat()


def enrich_verified_dates(rows: list[dict], *, schedule_fetcher=fetch_game_schedule) -> list[dict]:
    """Join schedules by game_id; reject any preexisting conflicting date.

    Date-only sorting is conservative: the walk-forward backtester excludes
    ALL same-day games. This does not certify data publication timestamps.
    """
    if not isinstance(rows, list):
        raise GameDateVerificationError("Expected normalized rows list")
    cache: dict[int, str] = {}
    output = []
    for row in rows:
        if not isinstance(row, dict) or row.get("source") != "api_basketball_v1":
            raise GameDateVerificationError("Expected normalized API-Basketball row")
        game_id = row.get("game_id")
        if type(game_id) is not int or game_id <= 0:
            raise GameDateVerificationError("Missing or invalid game_id")
        if game_id not in cache:
            cache[game_id] = verified_game_date(schedule_fetcher(game_id), game_id)
        verified = cache[game_id]
        if row.get("game_date") is not None and row["game_date"] != verified:
            raise GameDateVerificationError(f"Conflicting game_date for game {game_id}")
        output.append({**row, "game_date": verified})
    return output


def main() -> None:
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    rows = json.loads(args.input.read_text(encoding="utf-8"))
    enriched = enrich_verified_dates(rows)
    args.output.write_text(json.dumps(enriched, indent=2) + "\n", encoding="utf-8")
    print(f"Verified schedule dates for {len(enriched)} player-game records")


if __name__ == "__main__":
    main()
