"""SharpEdge WNBA confirmed-lineup monitor.

Polls Sportradar's WNBA schedule and game-summary feeds, detects starter flags,
persists state between GitHub Actions runs, opens a GitHub issue, and sends a
Pushover phone notification when a complete lineup first appears or changes.

Quota protection:
- schedule feeds are checked for the configured look-ahead window;
- summary feeds are requested only near tipoff;
- games closest to tip are prioritized;
- per-run summary requests are capped;
- a Sportradar HTTP 429 stops further API calls for that run.
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
PRETIP_WINDOW_MINUTES = int(os.getenv("WNBA_PRETIP_WINDOW_MINUTES", "90"))
POSTTIP_GRACE_MINUTES = int(os.getenv("WNBA_POSTTIP_GRACE_MINUTES", "15"))
MAX_SUMMARY_REQUESTS = int(os.getenv("WNBA_MAX_SUMMARY_REQUESTS_PER_RUN", "3"))
OUTPUT_DIR = Path(os.getenv("WNBA_MONITOR_OUTPUT_DIR", "data/wnba_monitor"))
STATE_FILE = OUTPUT_DIR / "state.json"
BASE_URL = f"https://api.sportradar.com/wnba/{ACCESS_LEVEL}/{VERSION}/{LANGUAGE}"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY", "").strip()
GITHUB_RUN_ID = os.getenv("GITHUB_RUN_ID", "").strip()

PUSHOVER_APP_TOKEN = os.getenv("PUSHOVER_APP_TOKEN", "").strip()
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY", "").strip()
PUSHOVER_DEVICE = os.getenv("PUSHOVER_DEVICE", "").strip()

if not API_KEY:
    print("ERROR: SPORTRADAR_API_KEY is unavailable.")
    sys.exit(1)


class RateLimitError(RuntimeError):
    """Raised when Sportradar returns HTTP 429."""


def request_json(
    url: str,
    *,
    method: str = "GET",
    body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    headers = {
        "Accept": "application/json",
        "User-Agent": "SharpEdge-WNBA-Lineup-Monitor/3.0",
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
        if exc.code == 429:
            retry_after = exc.headers.get("Retry-After", "unknown")
            raise RateLimitError(
                f"HTTP 429 Too Many Requests (Retry-After: {retry_after}): {raw[:300]}"
            ) from exc
        raise RuntimeError(f"HTTP {exc.code}: {raw[:600]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc


def post_form(url: str, fields: dict[str, str]) -> dict[str, Any]:
    data = urllib.parse.urlencode(fields).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "SharpEdge-WNBA-Lineup-Monitor/3.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Pushover HTTP {exc.code}: {raw[:600]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Pushover network error: {exc.reason}") from exc


def sportradar_get(path: str) -> dict[str, Any]:
    separator = "&" if "?" in path else "?"
    query = urllib.parse.urlencode({"api_key": API_KEY})
    return request_json(f"{BASE_URL}{path}{separator}{query}")


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
    return value is True or str(value).strip().lower() in {
        "true",
        "yes",
        "1",
        "starter",
        "starting",
    }


def player_record(node: dict[str, Any], source_path: str, team_hint: str | None) -> dict[str, Any]:
    return {
        "id": node.get("id"),
        "name": node.get("full_name") or node.get("name") or node.get("preferred_name"),
        "jersey": node.get("jersey_number") or node.get("jersey"),
        "position": node.get("position") or node.get("primary_position"),
        "team": team_hint,
        "source_path": source_path,
    }


def extract_starters(
    node: Any,
    path: str = "root",
    team_hint: str | None = None,
) -> list[dict[str, Any]]:
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
    return sorted(result, key=lambda player: (str(player.get("team")), str(player.get("name"))))


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
        f"**Minutes to tip when detected:** {snapshot.get('minutes_to_tip')}",
        "",
    ]
    for side in ("away", "home", None):
        players = [player for player in snapshot["starters"] if player.get("team") == side]
        if not players:
            continue
        heading = side.title() if side else "Unassigned"
        lines.extend([f"### {heading}", ""])
        for player in players:
            details = " · ".join(
                value
                for value in [
                    str(player.get("position") or "").strip(),
                    str(player.get("jersey") or "").strip(),
                ]
                if value
            )
            lines.append(
                f"- **{player.get('name') or player.get('id')}**"
                + (f" — {details}" if details else "")
            )
        lines.append("")
    if GITHUB_REPOSITORY and GITHUB_RUN_ID:
        lines.append(
            f"[Open monitor run](https://github.com/{GITHUB_REPOSITORY}/actions/runs/{GITHUB_RUN_ID})"
        )
    return "\n".join(lines)


def compact_lineup(snapshot: dict[str, Any]) -> str:
    away_players = [
        str(player.get("name") or player.get("id"))
        for player in snapshot["starters"]
        if player.get("team") == "away"
    ]
    home_players = [
        str(player.get("name") or player.get("id"))
        for player in snapshot["starters"]
        if player.get("team") == "home"
    ]
    return (
        f"{snapshot['away']}: {', '.join(away_players)}\n"
        f"{snapshot['home']}: {', '.join(home_players)}\n"
        f"Status: {snapshot['status']} | Detected: {snapshot['checked_at_utc']}"
    )


def send_github_alert(snapshot: dict[str, Any]) -> None:
    if not GITHUB_TOKEN or not GITHUB_REPOSITORY:
        print("GitHub alert skipped: token or repository unavailable.")
        return
    title = f"🏀 WNBA lineup confirmed: {snapshot['away']} @ {snapshot['home']}"
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/issues"
    request_json(
        url,
        method="POST",
        body={"title": title, "body": issue_body(snapshot), "labels": ["wnba-lineup-alert"]},
    )
    print(f"GitHub alert created: {title}")


def send_pushover_alert(snapshot: dict[str, Any], *, changed: bool) -> None:
    if not PUSHOVER_APP_TOKEN or not PUSHOVER_USER_KEY:
        print("Pushover alert skipped: PUSHOVER_APP_TOKEN or PUSHOVER_USER_KEY unavailable.")
        return

    title = (
        f"WNBA lineup changed: {snapshot['away']} @ {snapshot['home']}"
        if changed
        else f"WNBA lineup confirmed: {snapshot['away']} @ {snapshot['home']}"
    )
    fields = {
        "token": PUSHOVER_APP_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "title": title,
        "message": compact_lineup(snapshot),
        "priority": "1",
        "sound": "siren",
    }
    if PUSHOVER_DEVICE:
        fields["device"] = PUSHOVER_DEVICE
    if GITHUB_REPOSITORY and GITHUB_RUN_ID:
        fields["url"] = f"https://github.com/{GITHUB_REPOSITORY}/actions/runs/{GITHUB_RUN_ID}"
        fields["url_title"] = "Open monitor run"

    response = post_form("https://api.pushover.net/1/messages.json", fields)
    if response.get("status") != 1:
        raise RuntimeError(f"Unexpected Pushover response: {response}")
    print(f"Pushover alert sent: {title}")


def dispatch_alert(snapshot: dict[str, Any], *, changed: bool) -> None:
    errors: list[str] = []
    for sender in (
        lambda: send_github_alert(snapshot),
        lambda: send_pushover_alert(snapshot, changed=changed),
    ):
        try:
            sender()
        except RuntimeError as exc:
            errors.append(str(exc))
    for error in errors:
        print(f"Alert warning: {error}")


def schedule_days(now: datetime) -> list[datetime]:
    last = now + timedelta(hours=LOOKAHEAD_HOURS)
    days: list[datetime] = []
    cursor = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
    while cursor.date() <= last.date():
        days.append(cursor)
        cursor += timedelta(days=1)
    return days


def minutes_to_tip(scheduled: datetime | None, now: datetime) -> int | None:
    if scheduled is None:
        return None
    return int((scheduled - now).total_seconds() // 60)


def summary_is_eligible(game: dict[str, Any], now: datetime) -> bool:
    scheduled = parse_time(game.get("scheduled"))
    if scheduled is None:
        return False
    delta_minutes = (scheduled - now).total_seconds() / 60
    return -POSTTIP_GRACE_MINUTES <= delta_minutes <= PRETIP_WINDOW_MINUTES


def main() -> None:
    now = datetime.now(timezone.utc)
    state = load_state()
    prior_games = state.setdefault("games", {})
    games: dict[str, dict[str, Any]] = {}
    rate_limited = False

    for day in schedule_days(now):
        try:
            schedule = sportradar_get(
                f"/games/{day.year}/{day.month:02d}/{day.day:02d}/schedule.json"
            )
        except RateLimitError as exc:
            print(f"RATE LIMIT: {exc}")
            rate_limited = True
            break
        except RuntimeError as exc:
            print(f"Schedule warning for {day.date()}: {exc}")
            continue
        for game in schedule.get("games", []):
            if game.get("id"):
                games[str(game["id"])] = game

    eligible_games = [
        (game_id, game)
        for game_id, game in games.items()
        if summary_is_eligible(game, now)
    ]
    eligible_games.sort(
        key=lambda item: abs(
            (parse_time(item[1].get("scheduled")) - now).total_seconds()
        )
        if parse_time(item[1].get("scheduled"))
        else float("inf")
    )
    eligible_games = eligible_games[:MAX_SUMMARY_REQUESTS]

    snapshots: list[dict[str, Any]] = []
    summary_requests = 0

    for game_id, game in eligible_games:
        scheduled = parse_time(game.get("scheduled"))
        away = team_name(game.get("away"))
        home = team_name(game.get("home"))
        status = str(game.get("status") or "scheduled")
        detail: dict[str, Any] = {}
        error: str | None = None

        if rate_limited:
            error = "Skipped because an earlier Sportradar request hit HTTP 429."
        else:
            try:
                summary_requests += 1
                detail = sportradar_get(f"/games/{game_id}/summary.json")
            except RateLimitError as exc:
                error = str(exc)
                rate_limited = True
            except RuntimeError as exc:
                error = str(exc)

        starters = dedupe_players(extract_starters(detail)) if detail else []
        signature = lineup_signature(starters)
        previous = prior_games.get(game_id, {})
        previous_signature = previous.get("lineup_signature", [])
        changed = bool(signature) and signature != previous_signature
        first_complete_lineup = len(signature) >= 10 and len(previous_signature) < 10
        complete_lineup_change = (
            changed and len(signature) >= 10 and len(previous_signature) >= 10
        )

        snapshot = {
            "checked_at_utc": now.isoformat(),
            "game_id": game_id,
            "scheduled_utc": scheduled.isoformat() if scheduled else game.get("scheduled"),
            "minutes_to_tip": minutes_to_tip(scheduled, now),
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
        print(
            f"[{marker}] {away} at {home} | {status} | "
            f"tip in {snapshot['minutes_to_tip']} min | starters: {len(starters)}"
        )
        for player in starters:
            print(f"  - {player.get('team') or '?'}: {player.get('name') or player.get('id')}")
        if error:
            print(f"  Summary warning: {error}")

        if first_complete_lineup or complete_lineup_change:
            dispatch_alert(snapshot, changed=complete_lineup_change)

        # Never replace a known lineup with an empty result caused by a temporary
        # feed omission, network error, or rate limit response.
        stored_signature = signature if signature else previous_signature
        stored_starters = starters if starters else previous.get("starters", [])
        prior_games[game_id] = {
            "checked_at_utc": now.isoformat(),
            "status": status,
            "lineup_signature": stored_signature,
            "starter_count": len(stored_signature),
            "starters": stored_starters,
            "last_summary_error": error,
        }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "latest.json").write_text(
        json.dumps(snapshots, indent=2), encoding="utf-8"
    )
    state["last_checked_at_utc"] = now.isoformat()
    state["last_run_rate_limited"] = rate_limited
    state["last_run_summary_requests"] = summary_requests
    save_state(state)

    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as summary:
            summary.write("# WNBA Lineup Monitor\n\n")
            summary.write(f"Checked **{len(snapshots)}** near-tip game(s) at `{now.isoformat()}`.\n\n")
            summary.write(f"Summary requests used: **{summary_requests}/{MAX_SUMMARY_REQUESTS}**.\n\n")
            summary.write(f"Rate limited: **{rate_limited}**.\n\n")
            for item in snapshots:
                summary.write(
                    f"- **{item['away']} @ {item['home']}** — "
                    f"{item['starter_count']} starters, {item['minutes_to_tip']} minutes to tip\n"
                )

    print(
        f"Saved {len(snapshots)} snapshot(s) to {OUTPUT_DIR}. "
        f"Summary requests: {summary_requests}/{MAX_SUMMARY_REQUESTS}."
    )


if __name__ == "__main__":
    main()
