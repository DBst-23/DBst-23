#!/usr/bin/env python3
"""SharpEdge NBA half-split validation v2. Read-only; never invent odds or stats."""
import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

def call_with_retry(factory, attempts=3):
    for i in range(attempts):
        try:
            return factory()
        except Exception:
            if i == attempts - 1:
                raise
            time.sleep(3 * (2 ** i))

def stat(row, *names):
    for name in names:
        if name in row and row[name] is not None:
            return int(row[name])
    raise KeyError("Missing stat: " + "/".join(names))

def teams_for_period(game_id, first, last):
    from nba_api.stats.endpoints import boxscoretraditionalv3
    response = call_with_retry(lambda: boxscoretraditionalv3.BoxScoreTraditionalV3(
        game_id=game_id, start_period=first, end_period=last, range_type=0,
        timeout=45
    ))
    rows = response.team_stats.get_data_frame().to_dict("records")
    if len(rows) != 2:
        raise ValueError(f"Period {first}-{last}: expected 2 teams, got {len(rows)}")
    teams = {str(stat(r, "teamId", "TEAM_ID")): r for r in rows}
    if len(teams) != 2:
        raise ValueError("Duplicate team IDs")
    return teams

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", default="data/nba/half_split_smoke_audit.json")
    args = parser.parse_args()
    audit = {
        "status": "FAIL", "season": "2025-26", "mode": "ONE_GAME_SMOKE_TEST",
        "markets": "NOT_COLLECTED", "source": "nba_api / NBA stats",
        "generated_utc": datetime.now(timezone.utc).isoformat()
    }
    try:
        from nba_api.stats.endpoints import leaguegamefinder
        finder = call_with_retry(lambda: leaguegamefinder.LeagueGameFinder(
            season_nullable="2025-26", season_type_nullable="Regular Season",
            league_id_nullable="00", timeout=45
        ))
        frame = finder.get_data_frames()[0]
        frame = frame[frame.GAME_ID.astype(str).str.zfill(10).str.startswith("002")]
        game_ids = sorted(set(frame.GAME_ID.astype(str).str.zfill(10)))
        if not game_ids:
            raise ValueError("No regular-season games returned")
        gid = game_ids[0]
        audit["game_id"] = gid
        official_rows = frame[frame.GAME_ID.astype(str).str.zfill(10) == gid]
        official = {str(int(r.TEAM_ID)): int(r.PTS) for r in official_rows.itertuples()}
        if len(official) != 2:
            raise ValueError("Official final score must contain two teams")
        # Independently request each quarter AND each half. Comparing the
        # two catches endpoints that ignore period filters or return full-game data.
        quarters = [teams_for_period(gid, p, p) for p in range(1, 5)]
        halves = [teams_for_period(gid, 1, 2), teams_for_period(gid, 3, 4)]
        if any(set(block) != set(official) for block in quarters + halves):
            raise ValueError("Team IDs differ between periods and official box score")
        fields = {
            "points": ("points", "PTS"),
            "3pm": ("threePointersMade", "FG3M"),
            "3pa": ("threePointersAttempted", "FG3A"),
            "fga": ("fieldGoalsAttempted", "FGA"),
            "fta": ("freeThrowsAttempted", "FTA"),
            "orb": ("reboundsOffensive", "OREB"),
            "tov": ("turnovers", "TOV"),
        }
        comparisons = []
        for team in sorted(official):
            for half_index, period_indices in ((0, (0, 1)), (1, (2, 3))):
                for label, aliases in fields.items():
                    half_value = stat(halves[half_index][team], *aliases)
                    quarter_sum = sum(stat(quarters[i][team], *aliases) for i in period_indices)
                    if half_value != quarter_sum:
                        raise ValueError(
                            f"HALF_SPLIT_MISMATCH team={team} half={half_index+1} "
                            f"stat={label} half={half_value} quarters={quarter_sum}"
                        )
                comparisons.append({
                    "team_id": team, "half": half_index + 1,
                    "points": stat(halves[half_index][team], *fields["points"]),
                    "3pm": stat(halves[half_index][team], *fields["3pm"]),
                    "3pa": stat(halves[half_index][team], *fields["3pa"])
                })
            reg = sum(stat(q[team], *fields["points"]) for q in quarters)
            if reg > official[team]:
                raise ValueError(f"Regulation points exceed final for {team}")
        audit["team_halves"] = comparisons
        audit["official_final_points"] = official
        audit["overtime_possible"] = any(
            sum(stat(q[t], *fields["points"]) for q in quarters) < official[t]
            for t in official
        )
        audit["status"] = "PASS"
    except Exception as exc:
        audit["error_type"] = type(exc).__name__
        audit["error"] = str(exc)
    finally:
        output = Path(args.audit)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(audit, indent=2) + "\n")
        print(json.dumps(audit, indent=2), flush=True)
    return 0 if audit["status"] == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())
