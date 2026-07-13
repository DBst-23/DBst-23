import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

API_KEY = os.getenv("SPORTRADAR_API_KEY")
ACCESS_LEVEL = os.getenv("SPORTRADAR_ACCESS_LEVEL", "trial")
VERSION = os.getenv("SPORTRADAR_WNBA_VERSION", "v8")
LANGUAGE = os.getenv("SPORTRADAR_LANGUAGE", "en")
BASE_URL = f"https://api.sportradar.com/wnba/{ACCESS_LEVEL}/{VERSION}/{LANGUAGE}"
OUTPUT_DIR = Path(os.getenv("WNBA_MONITOR_OUTPUT_DIR", "data/wnba_monitor"))
LOOKAHEAD_HOURS = int(os.getenv("WNBA_LOOKAHEAD_HOURS", "18"))

if not API_KEY:
    print("ERROR: SPORTRADAR_API_KEY is not available.")
    sys.exit(1)


def api_get(path: str) -> dict[str, Any]:
    url = f"{BASE_URL}{path}?{urllib.parse.urlencode({'api_key': API_KEY})}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "SharpEdge-WNBA-Lineup-Monitor/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} for {path}: {body[:500]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error for {path}: {exc.reason}") from exc


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def team_name(team: dict[str, Any] | None) -> str:
    if not isinstance(team, dict):
        return "Unknown"
    return str(team.get("market") or team.get("name") or team.get("alias") or team.get("id") or "Unknown")


def extract_starters(node: Any, path: str = "root") -> list[dict[str, Any]]:
    starters: list[dict[str, Any]] = []
    if isinstance(node, dict):
        lowered = {str(k).lower(): v for k, v in node.items()}
        starter_flag = lowered.get("starter")
        lineup_flag = lowered.get("starting_lineup")
        if starter_flag is True or lineup_flag is True or str(starter_flag).lower() in {"true", "yes", "1"}:
            starters.append(
                {
                    "id": node.get("id"),
                    "name": node.get("full_name") or node.get("name") or node.get("preferred_name"),
                    "jersey": node.get("jersey_number") or node.get("jersey"),
                    "position": node.get("position") or node.get("primary_position"),
                    "source_path": path,
                }
            )
        for key, value in node.items():
            starters.extend(extract_starters(value, f"{path}.{key}"))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            starters.extend(extract_starters(value, f"{path}[{index}]"))
    return starters


def dedupe_players(players: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for player in players:
        key = str(player.get("id") or player.get("name") or player.get("source_path"))
        if key not in seen:
            seen.add(key)
            result.append(player)
    return result


def previous_snapshot(game_id: str) -> dict[str, Any] | None:
    path = OUTPUT_DIR / f"{game_id}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def save_snapshot(game_id: str, payload: dict[str, Any]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / f"{game_id}.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def schedule_dates(now: datetime) -> list[datetime]:
    dates = [now]
    if (now + timedelta(hours=LOOKAHEAD_HOURS)).date() != now.date():
        dates.append(now + timedelta(days=1))
    return dates


def main() -> None:
    now = datetime.now(timezone.utc)
    games: dict[str, dict[str, Any]] = {}

    for day in schedule_dates(now):
        payload = api_get(f"/games/{day.year}/{day.month:02d}/{day.day:02d}/schedule.json")
        for game in payload.get("games", []):
            game_id = game.get("id")
            if game_id:
                games[str(game_id)] = game

    if not games:
        print("No WNBA games found in the monitoring window.")
        return

    summary_rows: list[dict[str, Any]] = []
    for game_id, game in games.items():
        scheduled = parse_time(game.get("scheduled"))
        if scheduled and scheduled > now + timedelta(hours=LOOKAHEAD_HOURS):
            continue

        status = str(game.get("status", "scheduled"))
        home = team_name(game.get("home"))
        away = team_name(game.get("away"))
        detail: dict[str, Any] = {}
        error: str | None = None

        try:
            detail = api_get(f"/games/{game_id}/summary.json")
        except RuntimeError as exc:
            error = str(exc)

        starters = dedupe_players(extract_starters(detail)) if detail else []
        snapshot = {
            "checked_at_utc": now.isoformat(),
            "game_id": game_id,
            "scheduled_utc": scheduled.isoformat() if scheduled else game.get("scheduled"),
            "status": status,
            "away": away,
            "home": home,
            "starter_count": len(starters),
            "starters": starters,
            "summary_error": error,
        }

        previous = previous_snapshot(game_id)
        changed = previous is None or previous.get("starters") != starters or previous.get("status") != status
        snapshot["changed_since_previous_run"] = changed
        save_snapshot(game_id, snapshot)
        summary_rows.append(snapshot)

        marker = "CHANGED" if changed else "NO CHANGE"
        print(f"[{marker}] {away} at {home} | {status} | starters found: {len(starters)}")
        if starters:
            for player in starters:
                print(f"  - {player.get('name') or player.get('id')} ({player.get('position') or 'position n/a'})")
        elif error:
            print(f"  Summary unavailable: {error}")
        else:
            print("  No confirmed starter flags returned yet.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "latest.json").write_text(json.dumps(summary_rows, indent=2), encoding="utf-8")
    print(f"Saved {len(summary_rows)} game snapshot(s) to {OUTPUT_DIR}.")


if __name__ == "__main__":
    main()
