from __future__ import annotations

from typing import Any, Dict, List


ELITE_BIG_POSITIONS = {"C", "PF", "F-C", "C-F"}
FRAGILE_POSITIONS = {"PG", "SG", "SF", "G", "F", "G-F", "F-G"}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def compute_oreb_chaos_score(environment: Dict[str, Any]) -> Dict[str, Any]:
    """
    Scores pregame offensive rebound chaos risk.

    Expected environment keys:
    - opponent_fg_pct_allowed
    - opponent_three_pa_allowed
    - own_team_bench_big_minutes
    - opponent_def_reb_pct
    - opponent_oreb_allowed
    - projected_pace
    - opponent_long_rebound_profile
    """
    opp_fg_allowed = float(environment.get("opponent_fg_pct_allowed", 0.47))
    opp_three_pa_allowed = float(environment.get("opponent_three_pa_allowed", 32.0))
    bench_big_minutes = float(environment.get("own_team_bench_big_minutes", 0.0))
    opp_def_reb_pct = float(environment.get("opponent_def_reb_pct", 0.72))
    opp_oreb_allowed = float(environment.get("opponent_oreb_allowed", 10.0))
    projected_pace = float(environment.get("projected_pace", 99.0))
    long_rebound_profile = float(environment.get("opponent_long_rebound_profile", 0.50))

    miss_factor = clamp((0.46 - opp_fg_allowed) / 0.08, 0.0, 1.0)
    volume_factor = clamp((opp_three_pa_allowed - 30.0) / 18.0, 0.0, 1.0)
    bench_big_factor = clamp(bench_big_minutes / 28.0, 0.0, 1.0)
    weak_dreb_factor = clamp((0.74 - opp_def_reb_pct) / 0.12, 0.0, 1.0)
    oreb_allow_factor = clamp((opp_oreb_allowed - 9.0) / 8.0, 0.0, 1.0)
    pace_factor = clamp((projected_pace - 96.0) / 10.0, 0.0, 1.0)
    long_board_factor = clamp(long_rebound_profile, 0.0, 1.0)

    score = (
        miss_factor * 0.22
        + volume_factor * 0.16
        + bench_big_factor * 0.16
        + weak_dreb_factor * 0.16
        + oreb_allow_factor * 0.14
        + pace_factor * 0.08
        + long_board_factor * 0.08
    )
    score = round(clamp(score, 0.0, 1.0), 3)

    if score >= 0.72:
        tag = "OREB_CHAOS_EXTREME"
    elif score >= 0.58:
        tag = "OREB_CHAOS_ELEVATED"
    elif score >= 0.45:
        tag = "OREB_CHAOS_MODERATE"
    else:
        tag = "OREB_CHAOS_LOW"

    return {
        "score": score,
        "tag": tag,
        "components": {
            "miss_factor": round(miss_factor, 3),
            "volume_factor": round(volume_factor, 3),
            "bench_big_factor": round(bench_big_factor, 3),
            "weak_dreb_factor": round(weak_dreb_factor, 3),
            "oreb_allow_factor": round(oreb_allow_factor, 3),
            "pace_factor": round(pace_factor, 3),
            "long_board_factor": round(long_board_factor, 3),
        },
    }


def detect_oreb_chaos_pregame(environment: Dict[str, Any]) -> Dict[str, Any]:
    result = compute_oreb_chaos_score(environment)
    active = result["score"] >= 0.58

    return {
        "active": active,
        "tag": result["tag"],
        "score": result["score"],
        "components": result["components"],
        "reason": (
            "Pregame offensive rebound chaos risk is elevated"
            if active
            else "Pregame offensive rebound chaos risk is acceptable"
        ),
    }


def adjust_player_for_oreb_chaos(
    player: Dict[str, Any],
    projection: Dict[str, Any],
    chaos_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Adjust player rebound outlook using the OREB chaos signal.

    Elite interior anchors get boosted.
    Fragile wing/guard rebound overs get downgraded.
    """
    adjusted = dict(projection)
    position = str(player.get("position", "")).upper()
    role = str(player.get("role_tag", "")).upper()
    score = float(chaos_result.get("score", 0.0))

    mean = float(adjusted.get("mean", 0.0))
    median = float(adjusted.get("median", mean))
    win_prob = float(adjusted.get("win_prob", adjusted.get("prob", 0.5)))
    tags: List[str] = list(adjusted.get("tags", []))

    if not chaos_result.get("active"):
        adjusted["oreb_chaos_active"] = False
        adjusted["oreb_chaos_tag"] = chaos_result.get("tag", "OREB_CHAOS_LOW")
        adjusted["tags"] = tags
        return adjusted

    if position in ELITE_BIG_POSITIONS or "INTERIOR" in role or "REBOUND_ANCHOR" in role:
        mean *= 1.06 + (score - 0.58) * 0.08
        median *= 1.04 + (score - 0.58) * 0.05
        win_prob += 0.03 + (score - 0.58) * 0.06
        tags.extend(["OREB_CHAOS_ACTIVE", "ANCHOR_BIG_BOOST"])
    elif position in FRAGILE_POSITIONS:
        mean *= 0.96 - max(0.0, score - 0.58) * 0.05
        median *= 0.95 - max(0.0, score - 0.58) * 0.04
        win_prob -= 0.04 + max(0.0, score - 0.58) * 0.05
        tags.extend(["OREB_CHAOS_ACTIVE", "FRAGILE_REBOUND_FADE"])
    else:
        mean *= 1.01
        median *= 1.00
        win_prob += 0.00
        tags.append("OREB_CHAOS_ACTIVE")

    adjusted["mean"] = round(mean, 2)
    adjusted["median"] = round(median, 2)
    adjusted["win_prob"] = round(clamp(win_prob, 0.01, 0.99), 3)
    adjusted["oreb_chaos_active"] = True
    adjusted["oreb_chaos_tag"] = chaos_result["tag"]
    adjusted["oreb_chaos_score"] = round(score, 3)
    adjusted["tags"] = tags
    return adjusted


def build_oreb_chaos_summary(
    environment: Dict[str, Any],
    players: List[Dict[str, Any]],
    projections: List[Dict[str, Any]],
) -> Dict[str, Any]:
    chaos = detect_oreb_chaos_pregame(environment)
    adjusted_players: List[Dict[str, Any]] = []

    for player, projection in zip(players, projections):
        adjusted_players.append(
            {
                "player": player.get("name", ""),
                "position": player.get("position", ""),
                "adjusted": adjust_player_for_oreb_chaos(player, projection, chaos),
            }
        )

    return {
        "environment": chaos,
        "players": adjusted_players,
    }


if __name__ == "__main__":
    sample_environment = {
        "opponent_fg_pct_allowed": 0.43,
        "opponent_three_pa_allowed": 39,
        "own_team_bench_big_minutes": 22,
        "opponent_def_reb_pct": 0.68,
        "opponent_oreb_allowed": 13,
        "projected_pace": 101,
        "opponent_long_rebound_profile": 0.72,
    }

    sample_players = [
        {"name": "Rudy Gobert", "position": "C", "role_tag": "INTERIOR_REBOUND_ANCHOR"},
        {"name": "Naz Reid", "position": "C", "role_tag": "BENCH_BIG"},
        {"name": "Wing Player", "position": "SF", "role_tag": "PERIMETER_SCORER"},
    ]

    sample_projections = [
        {"mean": 11.7, "median": 11.0, "win_prob": 0.59, "tags": []},
        {"mean": 5.8, "median": 5.0, "win_prob": 0.54, "tags": []},
        {"mean": 4.5, "median": 4.0, "win_prob": 0.52, "tags": []},
    ]

    print(build_oreb_chaos_summary(sample_environment, sample_players, sample_projections))
