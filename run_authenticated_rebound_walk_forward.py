"""Authenticated chronological NBA rebound backtest smoke run.

Reads real NBA schedule and player box scores using GitHub Actions secret.
No sportsbook odds, betting EV, or out-of-sample model validation is claimed.
"""
import hashlib
import json
import os
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from modules.api_basketball_rebounds import fetch_player_game_stats, normalize_player_rebounds
from modules.api_basketball_game_dates import enrich_verified_dates
from modules.rebound_walk_forward_backtest import backtest

SEASON = "2024-2025"
LEAGUE = 12
MAX_GAMES = int(os.getenv('SHARPEDGE_MAX_GAMES', '180'))
MIN_PLAYER_GAMES = 4
TARGET_PREDICTIONS = int(os.getenv('SHARPEDGE_TARGET_PREDICTIONS', '200'))


def main():
    key = os.environ.get("APISPORTS_BASKETBALL_KEY")
    if not key:
        raise RuntimeError("Missing APISPORTS_BASKETBALL_KEY")
    url = "https://v1.basketball.api-sports.io/games?" + urlencode({"league": LEAGUE, "season": SEASON})
    with urlopen(Request(url, headers={"x-apisports-key": key}), timeout=30) as response:
        payload = json.load(response)
    if payload.get("errors") or not isinstance(payload.get("response"), list):
        raise RuntimeError("Authenticated NBA schedule unavailable")
    # The schedule is the authoritative game-ID/date mapping; reject conflicting IDs.
    schedule = {}
    for game in payload["response"]:
        if isinstance(game, dict) and type(game.get("id")) is int:
            game_id = game["id"]
            if game_id in schedule and schedule[game_id] != game:
                raise RuntimeError(f"Conflicting schedule entry for {game_id}")
            schedule[game_id] = game
    # Prefer earlier games, but never rely on game IDs for chronology.
    # Sorting by raw date is only for efficient selection, not validation.
    candidates = sorted(schedule.values(), key=lambda g: str(g.get("date", "")))
    by_player = defaultdict(list)
    seen = set()
    scanned = 0
    if not 1 <= MAX_GAMES <= 1387 or not 1 <= TARGET_PREDICTIONS <= 100000:
        raise ValueError('Invalid scan limits')
    for game in candidates:
        if scanned >= MAX_GAMES:
            break
        game_id = game["id"]
        scanned += 1
        try:
            rows = normalize_player_rebounds(fetch_player_game_stats(game_id=game_id))
        except Exception as exc:
            print(f"Skipped game {game_id}: {type(exc).__name__}")
            continue
        for row in rows:
            pid = row.get("player_id")
            pair = (pid, row.get("game_id"))
            if type(pid) is int and pair not in seen and row.get("minutes", 0) > 0:
                if row["game_id"] != game_id:
                    raise RuntimeError("Box-score game ID does not match requested schedule game")
                seen.add(pair)
                by_player[pid].append(row)
    eligible = [(pid, records) for pid, records in by_player.items() if len(records) >= MIN_PLAYER_GAMES]
    if not eligible:
        raise RuntimeError(f"No player with {MIN_PLAYER_GAMES} distinct games in {scanned} scanned games")
    def schedule_fetcher(game_id):
        if game_id not in schedule:
            raise RuntimeError(f"Missing authenticated schedule game {game_id}")
        return {"response": [schedule[game_id]], "errors": []}
    # Preserve every eligible player. The backtester groups players and
    # restricts each target to strictly earlier dates, never game IDs.
    records = [row for _, player_rows in sorted(eligible) for row in player_rows]
    dated = enrich_verified_dates(records, schedule_fetcher=schedule_fetcher)
    result = backtest(dated, line=4.5, min_games=3, window=10)
    if result["summary"]["predictions"] < 1:
        raise RuntimeError("No real chronological out-of-sample predictions produced")
    for prediction in result["predictions"]:
        if not prediction["training_last_date"] < prediction["game_date"]:
            raise RuntimeError("Chronological training leakage detected")
    result["summary"]["target_predictions"] = TARGET_PREDICTIONS
    result["summary"]["target_met"] = result["summary"]["predictions"] >= TARGET_PREDICTIONS
    result["summary"]["eligible_players"] = len(eligible)
    Path("verified_nba_rebound_records.json").write_text(json.dumps(dated, indent=2, sort_keys=True) + "\n")
    result["provenance"] = {
        "league": LEAGUE, "season": SEASON, "authenticated_schedule_entries": len(schedule),
        "scanned_games": scanned, "eligible_players": len(eligible),
        "verified_records": len(dated),
        "input_sha256": hashlib.sha256(json.dumps(dated, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "note": "Multi-player chronological baseline; illustrative line, no market odds or betting edge. Sample-size target is reported, not assumed."
    }
    Path("authenticated_rebound_walk_forward.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"provenance": result["provenance"], "summary": result["summary"]}, indent=2))


if __name__ == "__main__":
    main()
