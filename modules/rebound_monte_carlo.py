from __future__ import annotations

import math
import random
from statistics import mean, median
from typing import Any, Dict, List, Optional


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _poisson_sample(lam: float, rng: random.Random) -> int:
    if lam <= 0:
        return 0
    l = math.exp(-lam)
    k = 0
    p = 1.0
    while p > l:
        k += 1
        p *= rng.random()
    return k - 1


def _bernoulli(prob: float, rng: random.Random) -> int:
    return 1 if rng.random() < prob else 0


def _player_rebound_projection(player: Dict[str, Any], game_context: Dict[str, Any]) -> Dict[str, float]:
    minutes = float(player.get("projected_minutes", player.get("minutes", 28.0)) or 28.0)
    rebound_chances = float(player.get("rebound_chances", 0.0) or 0.0)
    rebound_chance_pct = float(player.get("rebound_chance_pct", 0.0) or 0.0)
    adjusted_rebound_chance_pct = float(player.get("adjusted_rebound_chance_pct", rebound_chance_pct) or rebound_chance_pct)
    contested_rebound_pct = float(player.get("contested_rebound_pct", 0.0) or 0.0)
    avg_rebound_distance = float(player.get("avg_rebound_distance", 6.0) or 6.0)
    recent_rebounds = [float(x) for x in player.get("recent_rebounds", [])]
    role_stability = float(player.get("role_stability", 1.0) or 1.0)
    lineup_stability = float(player.get("lineup_stability", 1.0) or 1.0)
    z_bound_pct = float(player.get("z_bound_pct", 0.0) or 0.0)
    offensive_rebound_rate = float(player.get("offensive_rebound_rate", 0.0) or 0.0)

    pace_factor = float(game_context.get("pace_factor", 1.0) or 1.0)
    miss_volume_factor = float(game_context.get("miss_volume_factor", 1.0) or 1.0)
    script_factor = float(player.get("script_factor", 1.0) or 1.0)

    expected_chances = rebound_chances * (minutes / 36.0)
    expected_chances *= pace_factor * miss_volume_factor
    expected_chances *= _clamp(role_stability * lineup_stability, 0.75, 1.2)

    conversion = (rebound_chance_pct + adjusted_rebound_chance_pct) / 2.0
    conversion *= (0.92 + min(contested_rebound_pct, 60.0) / 300.0)
    conversion *= (0.95 + min(avg_rebound_distance, 12.0) / 120.0)
    conversion *= (0.94 + min(z_bound_pct, 35.0) / 250.0)
    conversion *= (0.96 + min(offensive_rebound_rate, 25.0) / 250.0)
    conversion *= script_factor
    conversion = _clamp(conversion / 100.0 if conversion > 1.5 else conversion, 0.12, 0.88)

    base_mean = expected_chances * conversion
    if recent_rebounds:
        base_mean = base_mean * 0.7 + mean(recent_rebounds) * 0.3

    variance = max(1.0, base_mean * (1.15 - min(role_stability, 1.0) * 0.25))

    return {
        "expected_chances": expected_chances,
        "conversion": conversion,
        "mean_rebounds": base_mean,
        "variance_proxy": variance,
    }


def simulate_player_rebounds(
    player: Dict[str, Any],
    game_context: Dict[str, Any],
    iterations: int = 10000,
    seed: Optional[int] = 42,
) -> Dict[str, Any]:
    rng = random.Random(seed)
    projection = _player_rebound_projection(player, game_context)

    results: List[int] = []
    threshold = int(player.get("line", 0) or 0)

    for _ in range(iterations):
        chances = _poisson_sample(projection["expected_chances"], rng)
        rebounds = 0
        for _ in range(chances):
            rebounds += _bernoulli(projection["conversion"], rng)
        results.append(rebounds)

    hit_prob = sum(1 for x in results if x >= threshold) / iterations if threshold > 0 else 0.0

    return {
        "player": player.get("name", "UNKNOWN"),
        "line": threshold,
        "iterations": iterations,
        "mean": round(mean(results), 3),
        "median": round(median(results), 3),
        "min": min(results) if results else 0,
        "max": max(results) if results else 0,
        "hit_probability": round(hit_prob, 4),
        "expected_chances": round(projection["expected_chances"], 3),
        "conversion": round(projection["conversion"], 4),
        "results": results,
    }


def simulate_rebound_combo(
    players: List[Dict[str, Any]],
    game_context: Dict[str, Any],
    iterations: int = 10000,
    seed: Optional[int] = 42,
) -> Dict[str, Any]:
    rng = random.Random(seed)
    prepared = [_player_rebound_projection(p, game_context) for p in players]

    combo_hits = 0
    leg_hit_counts = [0 for _ in players]
    combo_samples: List[Dict[str, int]] = []

    for _ in range(iterations):
        leg_results = {}
        all_hit = True

        for idx, player in enumerate(players):
            projection = prepared[idx]
            chances = _poisson_sample(projection["expected_chances"], rng)
            rebounds = 0
            for _ in range(chances):
                rebounds += _bernoulli(projection["conversion"], rng)
            leg_results[player["name"]] = rebounds
            if rebounds >= int(player.get("line", 0) or 0):
                leg_hit_counts[idx] += 1
            else:
                all_hit = False

        if all_hit:
            combo_hits += 1
        combo_samples.append(leg_results)

    leg_summaries = []
    for idx, player in enumerate(players):
        rebounds_list = [sample[player["name"]] for sample in combo_samples]
        leg_summaries.append(
            {
                "player": player["name"],
                "line": int(player.get("line", 0) or 0),
                "mean": round(mean(rebounds_list), 3),
                "median": round(median(rebounds_list), 3),
                "hit_probability": round(leg_hit_counts[idx] / iterations, 4),
            }
        )

    combo_prob = combo_hits / iterations if iterations > 0 else 0.0

    return {
        "iterations": iterations,
        "combo_hit_probability": round(combo_prob, 4),
        "leg_summaries": leg_summaries,
    }


def build_hou_lal_game3_context() -> Dict[str, Any]:
    return {
        "pace_factor": 0.98,
        "miss_volume_factor": 1.08,
        "notes": "Game 3 style lower-total environment with elevated miss volume and strong Houston offensive rebounding pressure.",
    }


def build_hou_lal_game3_players() -> List[Dict[str, Any]]:
    return [
        {
            "name": "Tari Eason",
            "line": 6,
            "projected_minutes": 27,
            "rebound_chances": 11.5,
            "rebound_chance_pct": 0.785,
            "adjusted_rebound_chance_pct": 0.815,
            "contested_rebound_pct": 35.0,
            "avg_rebound_distance": 4.9,
            "recent_rebounds": [10, 8],
            "role_stability": 0.92,
            "lineup_stability": 0.95,
            "z_bound_pct": 0.30,
            "offensive_rebound_rate": 0.18,
            "script_factor": 1.03,
        },
        {
            "name": "LeBron James",
            "line": 8,
            "projected_minutes": 39,
            "rebound_chances": 13.5,
            "rebound_chance_pct": 0.593,
            "adjusted_rebound_chance_pct": 0.641,
            "contested_rebound_pct": 43.0,
            "avg_rebound_distance": 7.1,
            "recent_rebounds": [8, 8],
            "role_stability": 0.98,
            "lineup_stability": 0.97,
            "z_bound_pct": 0.12,
            "offensive_rebound_rate": 0.03,
            "script_factor": 1.0,
        },
        {
            "name": "Alperen Sengun",
            "line": 9,
            "projected_minutes": 36,
            "rebound_chances": 19.0,
            "rebound_chance_pct": 0.50,
            "adjusted_rebound_chance_pct": 0.54,
            "contested_rebound_pct": 36.0,
            "avg_rebound_distance": 6.0,
            "recent_rebounds": [8, 11],
            "role_stability": 0.99,
            "lineup_stability": 0.98,
            "z_bound_pct": 0.19,
            "offensive_rebound_rate": 0.12,
            "script_factor": 1.04,
        },
    ]


if __name__ == "__main__":
    context = build_hou_lal_game3_context()
    players = build_hou_lal_game3_players()

    for player in players:
        print(simulate_player_rebounds(player, context, iterations=5000))

    combo_players = [players[0], players[1]]
    print(simulate_rebound_combo(combo_players, context, iterations=5000))
