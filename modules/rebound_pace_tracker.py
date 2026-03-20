from __future__ import annotations

from typing import Dict, Any


def track_rebound_pace(payload: Dict[str, Any]) -> Dict[str, Any]:
    current_rebounds = float(payload.get("current_rebounds", 0.0))
    minutes_played = float(payload.get("minutes_played", 1.0))
    projected_minutes = float(payload.get("projected_minutes", 36.0))

    pace = current_rebounds / max(minutes_played, 1.0)
    projected_total = pace * projected_minutes

    pace_flag = "NORMAL"
    if pace > 0.35:
        pace_flag = "HIGH"
    elif pace < 0.22:
        pace_flag = "LOW"

    return {
        "rebound_pace": round(pace, 3),
        "projected_total_rebounds": round(projected_total, 1),
        "pace_flag": pace_flag
    }
