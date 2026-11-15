"""API-Basketball v1 historical player rebound ingestion.

Uses the user's *Basketball* subscription, not the separate API-NBA product.
No API keys are stored or printed. Standard-library only.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://v1.basketball.api-sports.io"
KEY_ENV = "APISPORTS_BASKETBALL_KEY"


class BasketballAPIError(RuntimeError):
    """An API or response validation failure."""


def fetch_player_game_stats(*, game_id: int | None = None,
                            player_id: int | None = None,
                            season: str | None = None) -> dict:
    """Fetch raw API-Basketball game/player stats.

    Provide game_id, or player_id plus season. A game ID from API-NBA
    is NOT interchangeable with an API-Basketball game ID.
    """
    if game_id is None and (player_id is None or not season):
        raise ValueError("Provide game_id or player_id together with season")
    key = os.environ.get(KEY_ENV)
    if not key:
        raise BasketballAPIError(f"Missing environment variable {KEY_ENV}")
    params = {}
    if game_id is not None:
        params["id"] = str(int(game_id))
    if player_id is not None:
        params["player"] = str(int(player_id))
    if season:
        params["season"] = str(season)
    url = BASE_URL + "/games/statistics/players?" + urlencode(params)
    req = Request(url, headers={"x-apisports-key": key}, method="GET")
    try:
        with urlopen(req, timeout=20) as response:
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError, ValueError) as exc:
        raise BasketballAPIError(f"Basketball API request failed: {type(exc).__name__}") from exc
    if not isinstance(payload, dict):
        raise BasketballAPIError("Expected a JSON object")
    if payload.get("errors"):
        raise BasketballAPIError(f"Basketball API returned errors: {payload['errors']}")
    if not isinstance(payload.get("response"), list):
        raise BasketballAPIError("Expected response to be a list")
    return payload


def parse_minutes(value: str | int | float | None) -> float | None:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value) if value >= 0 else None
    parts = str(value).split(":")
    if len(parts) != 2:
        return None
    try:
        minutes, seconds = int(parts[0]), int(parts[1])
    except ValueError:
        return None
    if minutes < 0 or not 0 <= seconds < 60:
        return None
    return minutes + seconds / 60


def normalize_player_rebounds(payload: dict) -> list[dict]:
    """Normalize only fields documented for API-Basketball v1.

    This endpoint documents total rebounds, not offensive/defensive splits
    or rebound chances. Missing data remains missing; never fabricate it.
    """
    if payload.get("errors"):
        raise BasketballAPIError(f"Basketball API returned errors: {payload['errors']}")
    records = payload.get("response")
    if not isinstance(records, list):
        raise BasketballAPIError("Expected response list")
    normalized = []
    for row in records:
        if not isinstance(row, dict):
            continue
        game = row.get("game") or {}
        player = row.get("player") or {}
        team = row.get("team") or {}
        rebounds = row.get("rebounds") or {}
        total = rebounds.get("total") if isinstance(rebounds, dict) else None
        if isinstance(total, bool) or not isinstance(total, int) or total < 0:
            continue
        minutes = parse_minutes(row.get("minutes"))
        if minutes is None:
            continue
        normalized.append({
            "source": "api_basketball_v1",
            "game_id": game.get("id"),
            "player_id": player.get("id"),
            "player_name": player.get("name"),
            "team_id": team.get("id"),
            "minutes": round(minutes, 4),
            "total_rebounds": total,
        })
    return normalized


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Read one API-Basketball game box score")
    parser.add_argument("--game-id", type=int, required=True,
                        help="API-Basketball game ID (not API-NBA ID)")
    parser.add_argument("--output", type=Path, default=Path("basketball_rebounds.json"))
    args = parser.parse_args()
    rows = normalize_player_rebounds(fetch_player_game_stats(game_id=args.game_id))
    args.output.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(rows)} player-game rebound records to {args.output}")
