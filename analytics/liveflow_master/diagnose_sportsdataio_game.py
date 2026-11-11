#!/usr/bin/env python3
"""Isolated one-game SportsDataIO NBA PBP diagnostic. Never trains or writes production data."""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_ROOT = "https://api.sportsdata.io/v3/nba/pbp/json/PlayByPlayFinal/"
def integer(value):
    if isinstance(value, bool) or value is None:
        raise ValueError("missing or noninteger score")
    result = int(value)
    if result < 0 or str(result) != str(value).strip():
        raise ValueError("negative or noninteger score")
    return result

def validate(payload, requested_id):
    errors, warnings = [], []
    if not isinstance(payload, dict):
        return ["response is not a JSON object"], warnings, {}
    game = payload.get("Game")
    quarters = payload.get("Quarters")
    plays = payload.get("Plays")
    if not isinstance(game, dict):
        errors.append("missing Game object")
        game = {}
    if not isinstance(quarters, list):
        errors.append("missing Quarters array")
        quarters = []
    if not isinstance(plays, list):
        errors.append("missing Plays array")
        plays = []
    try:
        actual_id = integer(game.get("GameID"))
        if actual_id != int(requested_id):
            errors.append("GameID does not match requested game")
    except (ValueError, TypeError):
        errors.append("missing/invalid Game.GameID")
    score_by_period = {}
    for q in quarters:
        if not isinstance(q, dict):
            errors.append("quarter entry is not an object")
            continue
        try:
            number = integer(q.get("Number"))
            away = integer(q.get("AwayScore"))
            home = integer(q.get("HomeScore"))
            if number in score_by_period:
                errors.append("duplicate quarter number")
            score_by_period[number] = (away, home)
        except (ValueError, TypeError):
            errors.append("invalid quarter number or score")
    if any(n not in score_by_period for n in (1, 2, 3, 4)):
        errors.append("missing regulation quarter(s) 1-4")
    if len(plays) == 0:
        errors.append("no play events")
    for index, play in enumerate(plays):
        if not isinstance(play, dict):
            errors.append("play event is not an object")
            break
        if play.get("PotentialPoints") is not None:
            try:
                pp = integer(play["PotentialPoints"])
                if pp > 3:
                    errors.append("impossible PotentialPoints > 3 in play " + str(index))
                    break
            except (ValueError, TypeError):
                errors.append("invalid PotentialPoints in play " + str(index))
                break
    if all(n in score_by_period for n in (1, 2, 3, 4)):
        away_reg = sum(score_by_period[n][0] for n in (1, 2, 3, 4))
        home_reg = sum(score_by_period[n][1] for n in (1, 2, 3, 4))
        away_all = sum(pair[0] for pair in score_by_period.values())
        home_all = sum(pair[1] for pair in score_by_period.values())
        try:
            game_away = integer(game.get("AwayTeamScore"))
            game_home = integer(game.get("HomeTeamScore"))
            if (away_all, home_all) != (game_away, game_home):
                errors.append("quarter sums disagree with Game final score")
        except (ValueError, TypeError):
            errors.append("missing/invalid Game final scores")
    else:
        away_reg = home_reg = None
    if not errors:
        warnings.append("Internal consistency does NOT establish that trial values are unscrambled or historically authentic.")
        warnings.append("Independent official-score cross-check and entitlement verification are required before training.")
    return errors, warnings, {
        "game_id": requested_id,
        "quarter_count": len(quarters),
        "play_count": len(plays),
        "regulation_away_points": away_reg,
        "regulation_home_points": home_reg,
        "overtime_periods": sum(n > 4 for n in score_by_period),
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--game-id", required=True, type=int)
    parser.add_argument("--input-json", help="Offline local fixture; bypasses API and requires no key")
    parser.add_argument("--audit", default="artifacts/nba_one_game_diagnostic.json")
    args = parser.parse_args()
    audit = {"provider": "SportsDataIO", "game_id": args.game_id,
             "generated_utc": datetime.now(timezone.utc).isoformat(),
             "status": "NOT_RUN", "training_eligible": False}
    try:
        if args.input_json:
            payload = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
            audit["source"] = "offline_fixture"
        else:
            key = os.environ.get("SPORTSDATAIO_API_KEY", "").strip()
            if not key:
                raise ValueError("SPORTSDATAIO_API_KEY secret is not configured")
            if args.game_id <= 0:
                raise ValueError("game ID must be positive")
            req = urllib.request.Request(
                API_ROOT + str(args.game_id),
                headers={"Ocp-Apim-Subscription-Key": key, "Accept": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=25) as response:
                payload = json.load(response)
            audit["source"] = "SportsDataIO PlayByPlayFinal"
        errors, warnings, metrics = validate(payload, args.game_id)
        audit.update(metrics)
        audit["errors"] = errors
        audit["warnings"] = warnings
        audit["status"] = "REJECTED" if errors else "STRUCTURE_PASSED_AUTHENTICITY_UNVERIFIED"
    except urllib.error.HTTPError as exc:
        audit.update(status="API_ERROR", errors=["HTTP " + str(exc.code) + " (check subscription, game ID, or endpoint)"])
    except (urllib.error.URLError, TimeoutError):
        audit.update(status="NETWORK_ERROR", errors=["API connection or timeout failure"])
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        # Never include raw HTTP responses or request URLs containing secrets.
        audit.update(status="ERROR", errors=[str(exc) if "SPORTSDATAIO_API_KEY" in str(exc) else type(exc).__name__ + ": invalid input or response"])
    path = Path(args.audit)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2))
    return 0 if audit["status"] == "STRUCTURE_PASSED_AUTHENTICITY_UNVERIFIED" else 2

if __name__ == "__main__":
    sys.exit(main())
