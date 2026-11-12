"""Build an isolated API-NBA halftime outcome dataset from season feeds.

Only Q1/Q2 scores are features. Final scores are labels, never features.
The outputs are local files; the calling workflow uploads them as artifacts.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

BASE_URL = "https://v2.nba.api-sports.io/games"
SEASONS = (2022, 2023, 2024)


def fetch_season(season: int, key: str) -> list[dict]:
    url = BASE_URL + "?" + urllib.parse.urlencode(
        {"league": "standard", "season": season}
    )
    request = urllib.request.Request(url, headers={"x-apisports-key": key})
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.load(response)
    if payload.get("errors"):
        raise RuntimeError(f"API-NBA season {season}: {payload['errors']}")
    games = payload.get("response")
    if not isinstance(games, list) or not games:
        raise RuntimeError(f"API-NBA season {season}: empty or invalid response")
    return games


def normalize(game: dict, season: int) -> tuple[dict | None, str | None]:
    """Return a regular-season, regulation game or a reason to quarantine it."""
    if not isinstance(game, dict):
        return None, "invalid_game"
    if str((game.get("status") or {}).get("short")) != "3":
        return None, "not_finished"
    if str(game.get("stage")) != "2":
        return None, "outside_regular_stage"
    if str(game.get("league")) != "standard" or str(game.get("season")) != str(season):
        return None, "league_or_season_mismatch"

    teams = game.get("teams") or {}
    scores = game.get("scores") or {}
    home, away = teams.get("home") or {}, teams.get("visitors") or {}
    if not home.get("id") or not away.get("id") or home["id"] == away["id"]:
        return None, "invalid_teams"
    try:
        game_id = int(game["id"])
        start = datetime.fromisoformat(game["date"]["start"].replace("Z", "+00:00"))
        if start.tzinfo is None:
            return None, "missing_timezone"
        q = {}
        final = {}
        for side in ("home", "visitors"):
            side_score = scores[side]
            raw = side_score["linescore"]
            if not isinstance(raw, list) or len(raw) < 4:
                return None, "missing_quarters"
            if len(raw) != 4:
                return None, "overtime_or_extra_periods"
            q[side] = [int(x) for x in raw]
            final[side] = int(side_score["points"])
            if min(q[side]) < 0 or final[side] < 0:
                return None, "negative_score"
            if sum(q[side]) != final[side]:
                return None, "quarter_total_mismatch"
    except (KeyError, TypeError, ValueError, OverflowError, AttributeError):
        return None, "invalid_score_or_date"

    h1_home, h1_away = sum(q["home"][:2]), sum(q["visitors"][:2])
    h2_home, h2_away = sum(q["home"][2:]), sum(q["visitors"][2:])
    return {
        "game_id": game_id,
        "season": season,
        "stage": 2,
        "start_utc": start.isoformat(),
        "game_date_eastern": start.astimezone(ZoneInfo("America/New_York")).date().isoformat(),
        "home_team_id": home["id"],
        "away_team_id": away["id"],
        "home_team": home.get("name"),
        "away_team": away.get("name"),
        "home_q1": q["home"][0],
        "home_q2": q["home"][1],
        "away_q1": q["visitors"][0],
        "away_q2": q["visitors"][1],
        "halftime_home": h1_home,
        "halftime_away": h1_away,
        "halftime_total": h1_home + h1_away,
        "halftime_margin_home": h1_home - h1_away,
        "second_half_home": h2_home,
        "second_half_away": h2_away,
        "second_half_total": h2_home + h2_away,
        "second_half_margin_home": h2_home - h2_away,
        "final_home": final["home"],
        "final_away": final["visitors"],
    }, None


def build(season_games: dict[int, list[dict]]) -> tuple[list[dict], list[dict], dict]:
    accepted, quarantine = [], []
    reasons = Counter()
    seen = set()
    counts = {}
    for season in sorted(season_games):
        games = season_games[season]
        counts[str(season)] = {"received": len(games), "accepted": 0}
        for game in games:
            row, reason = normalize(game, season)
            if row is not None:
                if row["game_id"] in seen:
                    row, reason = None, "duplicate_game_id"
                else:
                    seen.add(row["game_id"])
                    accepted.append(row)
                    counts[str(season)]["accepted"] += 1
            if row is None:
                reasons[reason] += 1
                quarantine.append({"season": season,
                                   "game_id": game.get("id") if isinstance(game, dict) else None,
                                   "reason": reason})
    accepted.sort(key=lambda r: (r["start_utc"], r["game_id"]))
    summary = {
        "source": "API-Sports API-NBA v2 /games?league=standard&season=YYYY",
        "seasons": counts,
        "accepted": len(accepted),
        "quarantined": len(quarantine),
        "reasons": dict(sorted(reasons.items())),
        "features_available_at_halftime": ["home_q1", "home_q2", "away_q1", "away_q2",
                                           "halftime_home", "halftime_away", "halftime_total",
                                           "halftime_margin_home"],
        "labels_observed_after_halftime": ["second_half_home", "second_half_away",
                                           "second_half_total", "second_half_margin_home",
                                           "final_home", "final_away"],
        "safe_for_betting_edge_backtest": False,
        "note": "No archived halftime odds or halftime team/player stat snapshots. "
                "Betting EV requires timestamped halftime prices; probability calibration "
                "requires an independently fitted model and chronological holdout.",
    }
    return accepted, quarantine, summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("nba_halftime_artifact"))
    args = parser.parse_args()
    key = os.environ.get("API_SPORTS_KEY")
    if not key:
        parser.error("API_SPORTS_KEY is required")
    season_games = {season: fetch_season(season, key) for season in SEASONS}
    accepted, quarantine, summary = build(season_games)
    if not accepted:
        raise RuntimeError("No valid games; refusing to produce an empty dataset")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, rows in (("halftime_outcomes.jsonl", accepted),
                       ("quarantine.jsonl", quarantine)):
        with (args.output_dir / name).open("w") as out:
            for row in rows:
                out.write(json.dumps(row, separators=(",", ":")) + "\n")
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"accepted": summary["accepted"],
                      "quarantined": summary["quarantined"],
                      "reasons": summary["reasons"],
                      "safe_for_betting_edge_backtest": False}))


if __name__ == "__main__":
    main()
