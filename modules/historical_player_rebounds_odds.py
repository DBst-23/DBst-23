"""The Odds API historical NBA player-rebounds adapter (offline-first).

No paid requests are performed here. Feed previously authorized, privately stored
historical event-odds JSON into normalize_rebound_snapshot(). Never commit raw
provider responses or API keys to a public repository.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

SPORT = "basketball_nba"
MARKET = "player_rebounds"
HISTORICAL_EVENTS_PATH = "/v4/historical/sports/{sport}/events"
HISTORICAL_MARKETS_PATH = "/v4/historical/sports/{sport}/events/{event_id}/markets"
HISTORICAL_ODDS_PATH = "/v4/historical/sports/{sport}/events/{event_id}/odds"


def _timestamp(value: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError("Missing required ISO-8601 timestamp")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Timestamp must contain a timezone")
    return parsed.astimezone(timezone.utc)


def normalize_rebound_snapshot(
    payload: dict[str, Any], *, event_id: str, requested_at: str,
    decision_cutoff: str,
) -> list[dict[str, Any]]:
    """Normalize historical rebound lines, rejecting unavailable/late prices.

    The provider's returned snapshot timestamp is distinct from the requested
    date. Both snapshot and bookmaker/market last_update must be <= cutoff.
    Caller must additionally establish the historical decision time and any
    feed/processing/placement latency. No odds are inferred or fabricated.
    """
    cutoff = _timestamp(decision_cutoff)
    requested = _timestamp(requested_at)
    snapshot = _timestamp(payload["timestamp"])
    if requested > cutoff or snapshot > cutoff:
        raise ValueError("Requested/returned snapshot is later than decision cutoff")
    data = payload.get("data")
    if not isinstance(data, dict) or str(data.get("id")) != str(event_id):
        raise ValueError("Historical event ID mismatch or missing data")
    rows: list[dict[str, Any]] = []
    for book in data.get("bookmakers", []):
        for market in book.get("markets", []):
            if market.get("key") != MARKET:
                continue
            updated = _timestamp(market["last_update"])
            if updated > cutoff or updated > snapshot:
                continue
            for outcome in market.get("outcomes", []):
                side = outcome.get("name")
                if side not in ("Over", "Under"):
                    continue
                player = outcome.get("description")
                line, price = outcome.get("point"), outcome.get("price")
                if not isinstance(player, str) or not player.strip():
                    continue
                if isinstance(line, bool) or not isinstance(line, (int, float)):
                    continue
                if isinstance(price, bool) or not isinstance(price, (int, float)) or price <= 1:
                    continue
                rows.append({
                    "sport": SPORT, "event_id": str(event_id),
                    "home_team": data.get("home_team"), "away_team": data.get("away_team"),
                    "commence_time": data.get("commence_time"),
                    "requested_at": requested.isoformat(), "snapshot_at": snapshot.isoformat(),
                    "market_updated_at": updated.isoformat(),
                    "bookmaker_key": book.get("key"), "bookmaker_title": book.get("title"),
                    "market": MARKET, "player": player.strip(), "side": side,
                    "line": float(line), "decimal_odds": float(price),
                    "decision_cutoff": cutoff.isoformat(),
                    "status": "RESEARCH_ONLY_UNVERIFIED_EXECUTABILITY",
                })
    return rows
