"""SharpEdge WNBA confirmed-lineup monitor.

Polls Sportradar's WNBA schedule and game-summary feeds, detects starter flags,
persists state between GitHub Actions runs, and opens a GitHub issue when a
matchup's confirmed starting lineup changes.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

API_KEY = os.getenv("SPORTRADAR_API_KEY", "").strip()
ACCESS_LEVEL = os.getenv("SPORTRADAR_ACCESS_LEVEL", "trial").strip()
VERSION = os.getenv("SPORTRADAR_WNBA_VERSION", "v8").strip()
LANGUAGE = os.getenv("SPORTRADAR_LANGUAGE", "en").strip()
LOOKAHEAD_HOURS = int(os.getenv("WNBA_LOOKAHEAD_HOURS", "24"))
OUTPUT_DIR = Path(os.getenv("WNBA_MONITOR_OUTPUT_DIR", "data/wnba_monitor"))
STATE_FILE = OUTPUT_DIR / "state.json"
BASE_URL = f"https://api.sportradar.com/wnba/{ACCESS_LEVEL}/{VERSION}/{LANGUAGE}"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY", "").strip()
GITHUB_RUN_ID = os.getenv("GITHUB_RUN_ID", "").strip()

if not API_KEY:
    print("ERROR: SPORTRADAR_API_KEY is unavailable.")
    sys.exit(1)


def request_json(url: str, *, method: str = "GET", body: dict[str, Any] | None = None) -> dict[str, Any]:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    headers = {
        "Accept": "application/json",
        "User-Agent": "SharpEdge-WNBA-Lineup-Monitor/2.0",
    }
    if data is not None:
        headers["Content-Type"] = "application/json"
    if url.startswith("https://api.github.com/") and GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
        headers["X-GitHub-Api-Version"] = "2022-11-28"

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {raw[:600]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc


def sportradar_get(path: str) -> dict[str, Any]:
    separator = "&" if "?" in path else "?"
    return request_json(f"{BASE_URL}{path}{separator}{urllib.parse.urlencode({'api_key': API_KEY})}")


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def team_name(team: Any) -> str:
    if not isinstance(team, dict):
        return "Unknown"
    market = str(team.get("market") or "").strip()
    name = str(team.get("name") or team.get("alias") or team.get("id") or "Unknown").strip()
    return f"{market} {name}".strip()


def truthy(value: Any) -> bool:
    return value is True or str(value).strip().lower() in {"true", "yes", "1", "starter", "starting"}


def player_record(node: dict[str, Any], source_path: str, team_hint: str | None) -> dict[str, Any]:
    return {
        "id": node.get("id"),
        "name": node.get("full_name") or node.get("name") or node.get("preferred_name"),
        "jersey": node.get("jersey_number") or node.get("jersey"),
        "position": node.get("position") or node.get("primary_position"),
        "team": team_hint,
        "source_path": source_path,
    }


def extract_starters(node: Any, path: str = "root", team_hint: str | None = None) -> list[dict[str, Any]]:
    starters: list[dict[str, Any]] = []
    if isinstance(node, dict):
        lowered = {str(key).lower(): value for key, value in node.items()}
        local_team = team_hint
        if path.endswith(".home") or ".home." in path:
            local_team = "home"
        elif path.endswith(".away") or ".away." in path:
            local_team = "away"

        starter_values = [
            lowered.get("starter"),
            lowered.get("starting_lineup"),
            lowered.get("is_starter"),
            lowered.get("starting"),
        ]
        if any(truthy(value) for value in starter_values):
            starters.append(player_record(node, path, local_team))

        # Some feeds expose a dedicated starters array without per-player flags.
        for key, value in node.items():
            key_lower = str(key).lower()
            child_path = f"{path}.{key}"
            if key_lower in {"starters", "starting_lineup", "startinglineup"} and isinstance(value, list):
                for index, player in enumerate(value):
                    if isinstance(player, dict):
                        starters.append(player_record(player, f"{child_path}[{index}]", local_team))
            starters.extend(extract_starters(value, child_path, local_team))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            starters.extend(extract_starters(value, f"{path}[{index}]", team_hint))
    return starters


def dedupe_players(players: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for player in players:
        key = str(player.get("id") or player.get("name") or player.get("source_path"))
        if key not in seen and (player.get("id") or player.get("name")):
            seen.add(key)
            result.append(player)
    return sorted(result, key=lambda p: (str(p.get("team")), str(p.get("name"))))


def load_state() -> dict[str, Any]:
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"games": {}}


def save_state(state: dict[str, Any]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


def lineup_signature(starters: list[dict[str, Any]]) -> list[str]:
    return sorted(str(player.get("id") or player.get("name")) for player in starters)


def issue_body(snapshot: dict[str, Any]) -> str:
    lines = [
        "## Confirmed WNBA lineup update",
        "",
        f"**Matchup:** {snapshot['away']} at {snapshot['home']}",
        f"**Scheduled:** {snapshot.get('scheduled_utc') or 'Unknown'}",
        f"**Game status:** {snapshot['status']}",
        f"**Detected starters:** {snapshot['starter_count']}",
        "",
    ]
    for side in ("away", "home", None):
        players = [p for p in snapshot["starters"] if p.get("team") == side]
        if not players:
            continue
        heading = side.title() if side else "Unassigned"
        lines.extend([f"### {heading}", ""])
        for player in players:
            details = " · ".join(
                value for value in [str(player.get("position") or "").strip(), str(player.get("jersey") or "").strip()] if value
            )
            lines.append(f"- **{player.get('name') or player.get('id')}**" + (f" — {details}" if details else ""))
        lines.append("")
    if GITHUB_REPOSITORY and GITHUB_RUN_ID:
        lines.append(f"[Open monitor run](https://github.com/{GITHUB_REPOSITORY}/actions/runs/{GITHUB_RUN_ID})")
    return "\n".join(lines)


def send_github_alert(snapshot: dict[str, Any]) -> None:
    if not GITHUB_TOKEN or not GITHUB_REPOSITORY:
        print("GitHub alert skipped: token or repository unavailable.")
        return
    title = f"🏀 WNBA lineup confirmed: {snapshot['away']} @ {snapshot['home']}"
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/issues"
    request_json(url, method="POST", body={"title": title, "body": issue_body(snapshot), "labels": ["wnba-lineup-alert"]})
    print(f"GitHub alert created: {title}")


def schedule_days(now: datetime) -> list[datetime]:
    last = now + timedelta(hours=LOOKAHEAD_HOURS)
    days: list[datetime] = []
    cursor = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
    while cursor.date() <= last.date():
        days.append(cursor)
        cursor += timedelta(days=1)
    return days


def main() -> None:
    now = datetime.now(timezone.utc)
    state = load_state()
    prior_games = state.setdefault("games", {})
    games: dict[str, dict[str, Any]] = {}

    for day in schedule_days(now):
        schedule = sportradar_get(f"/games/{day.year}/{day.month:02d}/{day.day:02d}/schedule.json")
        for game in schedule.get("games", []):
            if game.get("id"):
                games[str(game["id"])] = game

    snapshots: list[dict[str, Any]] = []
    for game_id, game in games.items():
        scheduled = parse_time(game.get("scheduled"))
        if scheduled and scheduled > now + timedelta(hours=LOOKAHEAD_HOURS):
            continue

        away = team_name(game.get("away"))
        home = team_name(game.get("home"))
        status = str(game.get("status") or "scheduled")
        detail: dict[str, Any] = {}
        error: str | None = None
        try:
            detail = sportradar_get(f"/games/{game_id}/summary.json")
        except RuntimeError as exc:
            error = str(exc)

        starters = dedupe_players(extract_starters(detail)) if detail else []
        signature = lineup_signature(starters)
        previous = prior_games.get(game_id, {})
        previous_signature = previous.get("lineup_signature", [])
        changed = bool(signature) and signature != previous_signature
        first_complete_lineup = len(signature) >= 10 and len(previous_signature) < 10

        snapshot = {
            "checked_at_utc": now.isoformat(),
            "game_id": game_id,
            "scheduled_utc": scheduled.isoformat() if scheduled else game.get("scheduled"),
            "status": status,
            "away": away,
            "home": home,
            "starter_count": len(starters),
            "starters": starters,
            "lineup_signature": signature,
            "changed_since_previous_run": changed,
            "summary_error": error,
        }
        snapshots.append(snapshot)

        marker = "LINEUP CHANGE" if changed else "NO CHANGE"
        print(f"[{marker}] {away} at {home} | {status} | starters: {len(starters)}")
        for player in starters:
            print(f"  - {player.get('team') or '?'}: {player.get('name') or player.get('id')}")
        if error:
            print(f"  Summary warning: {error}")

        # Alert only once a complete 10-player lineup first appears, then on later changes.
        if first_complete_lineup or (changed and len(signature) >= 10 and len(previous_signature) >= 10):
            send_github_alert(snapshot)

        prior_games[game_id] = {
            "checked_at_utc": now.isoformat(),
            "status": status,
            "lineup_signature": signature,
            "starter_count": len(starters),
        }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "latest.json").write_text(json.dumps(snapshots, indent=2), encoding="utf-8")
    state["last_checked_at_utc"] = now.isoformat()
    save_state(state)

    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as summary:
            summary.write("# WNBA Lineup Monitor\n\n")
            summary.write(f"Checked **{len(snapshots)}** game(s) at `{now.isoformat()}`.\n\n")
            for item in snapshots:
                summary.write(f"- **{item['away']} @ {item['home']}** — {item['starter_count']} starters detected\n")

    print(f"Saved {len(snapshots)} snapshot(s) to {OUTPUT_DIR}.")


if __name__ == "__main__":
    main()
