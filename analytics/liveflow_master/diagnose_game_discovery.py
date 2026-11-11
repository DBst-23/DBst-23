#!/usr/bin/env python3
"""Read-only NBA schedule discovery diagnostic. Never creates training data."""
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

URL = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_1.json"
OUT = Path("data/nba/game_discovery_diagnostic.json")

def main():
    report = {"source": URL, "target_season": "2025-26",
              "generated_utc": datetime.now(timezone.utc).isoformat(),
              "status": "NOT_VERIFIED", "games_discovered": 0,
              "game_ids_sample": [], "warnings": []}
    try:
        req = urllib.request.Request(URL, headers={"User-Agent": "SharpEdge-ReadOnly-Diagnostic/1.0", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=25) as response:
            payload = json.load(response)
        league = payload.get("leagueSchedule", {})
        dates = league.get("gameDates", [])
        if not isinstance(dates, list):
            raise ValueError("gameDates is not a list")
        games = [g for day in dates for g in day.get("games", []) if isinstance(g, dict)]
        # NBA regular season IDs start with 002; exclude preseason, playoffs and All-Star.
        regular = [g for g in games if str(g.get("gameId", "")).startswith("002")]
        # Explicitly verify schedule season rather than assuming all games belong to target.
        target = [g for g in regular if str(g.get("gameDateEst", g.get("gameDateTimeEst", "")))[:4] in ("2025", "2026")]
        # Filter NBA season boundaries, not calendar year alone.
        target = [g for g in target if "2025-10-01" <= str(g.get("gameDateEst", g.get("gameDateTimeEst", "")))[:10] <= "2026-06-30"]
        unique = sorted({str(g["gameId"]) for g in target})
        report.update(schedule_season=league.get("seasonYear"), total_schedule_games=len(games),
                      regular_games_in_schedule=len(regular), games_discovered=len(unique),
                      game_ids_sample=unique[:5])
        season_label = str(league.get("seasonYear", ""))
        if season_label not in ("2025-26", "2025", "2025-2026"):
            report["warnings"].append("Schedule season metadata does not confirm target season")
        if len(unique) != 1230:
            report["warnings"].append("Expected 1230 regular-season games; observed count differs")
        report["status"] = "DISCOVERY_VALIDATED" if len(unique) == 1230 and not report["warnings"] else "NEEDS_REVIEW"
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        report["status"] = "DISCOVERY_FAILED"
        report["error_type"] = type(exc).__name__
        report["error"] = str(exc)[:350]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "DISCOVERY_VALIDATED" else 2

if __name__ == "__main__":
    sys.exit(main())
