"""
SharpEdge Auto Rebound Edge Detector V1

Purpose:
- Ingest rebound market lines, projected minutes, player rebound tracking, and optional lineup context.
- Produce mean, median, hit probability, edge grade, and risk tags.
- Designed for NBA playoff prop scouting.

Core idea:
Projection = minutes-based rebound rate + chance quality + matchup environment + role volatility.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional, Dict, List, Any
import math
import csv
import json


@dataclass
class ReboundMarket:
    player: str
    team: str
    opponent: str
    line: float
    side: str = "over"
    price_decimal: Optional[float] = None


@dataclass
class PlayerMinutes:
    player: str
    team: str
    projected_minutes: float


@dataclass
class PlayerReboundTracking:
    player: str
    team: str
    games: int
    minutes: float
    rebounds: float
    rebound_chances: float
    rebound_chance_pct: float
    adjusted_rebound_chance_pct: float
    contested_rebound_pct: float
    avg_rebound_distance: float


@dataclass
class ReboundEdgeResult:
    player: str
    team: str
    opponent: str
    line: float
    side: str
    mean: float
    median: float
    hit_probability: float
    edge_score: float
    confidence_tier: str
    risk_tags: List[str]
    notes: List[str]


class AutoReboundEdgeDetector:
    def __init__(
        self,
        blowout_probability: float = 0.50,
        competitive_probability: float = 0.50,
        pace_scalar: float = 1.00,
        missed_shot_scalar: float = 1.00,
        long_rebound_scalar: float = 1.00,
    ) -> None:
        self.blowout_probability = blowout_probability
        self.competitive_probability = competitive_probability
        self.pace_scalar = pace_scalar
        self.missed_shot_scalar = missed_shot_scalar
        self.long_rebound_scalar = long_rebound_scalar

    @staticmethod
    def _normal_cdf(x: float) -> float:
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

    @staticmethod
    def _clean_name(name: str) -> str:
        return (
            name.lower()
            .replace(".", "")
            .replace("'", "")
            .replace("’", "")
            .replace("-", " ")
            .strip()
        )

    def _match_player(
        self,
        player_name: str,
        tracking: Dict[str, PlayerReboundTracking],
    ) -> Optional[PlayerReboundTracking]:
        key = self._clean_name(player_name)
        if key in tracking:
            return tracking[key]

        for k, record in tracking.items():
            if key in k or k in key:
                return record

        return None

    def _minutes_lookup(
        self,
        player_name: str,
        minutes: Dict[str, PlayerMinutes],
    ) -> Optional[PlayerMinutes]:
        key = self._clean_name(player_name)
        if key in minutes:
            return minutes[key]

        for k, record in minutes.items():
            if key in k or k in key:
                return record

        return None

    def project_player(
        self,
        market: ReboundMarket,
        minutes_map: Dict[str, PlayerMinutes],
        tracking_map: Dict[str, PlayerReboundTracking],
        team_rebound_modifier: float = 1.00,
        opponent_miss_modifier: float = 1.00,
        role_modifier: float = 1.00,
    ) -> ReboundEdgeResult:

        minutes_record = self._minutes_lookup(market.player, minutes_map)
        tracking_record = self._match_player(market.player, tracking_map)

        risk_tags: List[str] = []
        notes: List[str] = []

        if minutes_record is None:
            projected_minutes = 30.0
            risk_tags.append("MISSING_MINUTES_PROJECTION")
            notes.append("Projected minutes missing; defaulted to 30.0.")
        else:
            projected_minutes = minutes_record.projected_minutes

        if tracking_record is None:
            baseline_rebounds = market.line
            rebound_chance_quality = 1.00
            chance_volume_modifier = 1.00
            adjusted_chance_modifier = 1.00
            risk_tags.append("MISSING_REBOUND_TRACKING")
            notes.append("Player tracking missing; centered baseline near market.")
        else:
            minutes_base = max(tracking_record.minutes, 1.0)
            rebounds_per_min = tracking_record.rebounds / minutes_base
            baseline_rebounds = rebounds_per_min * projected_minutes

            chance_volume_modifier = min(
                1.18,
                max(0.84, tracking_record.rebound_chances / max(tracking_record.minutes * 0.33, 1.0)),
            )

            rebound_chance_quality = min(
                1.15,
                max(0.85, tracking_record.adjusted_rebound_chance_pct / 60.0),
            )

            adjusted_chance_modifier = min(
                1.12,
                max(0.88, tracking_record.rebound_chance_pct / 55.0),
            )

            if tracking_record.games < 3:
                risk_tags.append("SMALL_SAMPLE_TRACKING")

            if tracking_record.avg_rebound_distance >= 8.5:
                risk_tags.append("LONG_REBOUND_DEPENDENT")

            if tracking_record.contested_rebound_pct >= 45:
                risk_tags.append("CONTESTED_REBOUND_HEAVY")

        environment_modifier = (
            self.pace_scalar
            * self.missed_shot_scalar
            * self.long_rebound_scalar
            * team_rebound_modifier
            * opponent_miss_modifier
            * role_modifier
        )

        mean = (
            baseline_rebounds
            * chance_volume_modifier
            * rebound_chance_quality
            * adjusted_chance_modifier
            * environment_modifier
        )

        blowout_mean = mean * 0.97
        competitive_mean = mean * 1.03
        blended_mean = (
            blowout_mean * self.blowout_probability
            + competitive_mean * self.competitive_probability
        )

        mean = round(blended_mean, 2)
        median = round(mean - 0.20, 2)

        std_dev = max(1.65, 0.27 * market.line + 1.10)

        if market.side.lower() == "over":
            hit_probability = 1.0 - self._normal_cdf((market.line + 0.5 - mean) / std_dev)
            edge_score = mean - market.line
        else:
            hit_probability = self._normal_cdf((market.line - 0.5 - mean) / std_dev)
            edge_score = market.line - mean

        hit_probability = round(hit_probability, 4)
        edge_score = round(edge_score, 2)

        if hit_probability >= 0.62:
            confidence_tier = "A"
        elif hit_probability >= 0.58:
            confidence_tier = "B"
        elif hit_probability >= 0.54:
            confidence_tier = "C"
        elif hit_probability >= 0.51:
            confidence_tier = "Lean"
        else:
            confidence_tier = "No Bet"

        if projected_minutes < 24:
            risk_tags.append("MINUTES_CAP_RISK")

        if abs(edge_score) < 0.35:
            risk_tags.append("THIN_EDGE")

        if hit_probability < 0.54:
            risk_tags.append("NO_CALL_ZONE")

        notes.append(f"Projected minutes: {projected_minutes}")
        notes.append(f"Environment modifier: {round(environment_modifier, 3)}")
        notes.append(f"Blowout probability: {round(self.blowout_probability, 2)}")

        return ReboundEdgeResult(
            player=market.player,
            team=market.team,
            opponent=market.opponent,
            line=market.line,
            side=market.side,
            mean=mean,
            median=median,
            hit_probability=hit_probability,
            edge_score=edge_score,
            confidence_tier=confidence_tier,
            risk_tags=sorted(set(risk_tags)),
            notes=notes,
        )

    def run(
        self,
        markets: List[ReboundMarket],
        minutes: List[PlayerMinutes],
        tracking: List[PlayerReboundTracking],
        team_rebound_modifiers: Optional[Dict[str, float]] = None,
        opponent_miss_modifiers: Optional[Dict[str, float]] = None,
        role_modifiers: Optional[Dict[str, float]] = None,
    ) -> List[ReboundEdgeResult]:

        minutes_map = {self._clean_name(m.player): m for m in minutes}
        tracking_map = {self._clean_name(t.player): t for t in tracking}

        team_rebound_modifiers = team_rebound_modifiers or {}
        opponent_miss_modifiers = opponent_miss_modifiers or {}
        role_modifiers = role_modifiers or {}

        results = []

        for market in markets:
            result = self.project_player(
                market=market,
                minutes_map=minutes_map,
                tracking_map=tracking_map,
                team_rebound_modifier=team_rebound_modifiers.get(market.team, 1.00),
                opponent_miss_modifier=opponent_miss_modifiers.get(market.opponent, 1.00),
                role_modifier=role_modifiers.get(market.player, 1.00),
            )
            results.append(result)

        results.sort(key=lambda x: x.hit_probability, reverse=True)
        return results


def load_csv_dicts(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def save_results_json(results: List[ReboundEdgeResult], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump([asdict(r) for r in results], f, indent=2)


if __name__ == "__main__":
    markets = [
        ReboundMarket("Jayson Tatum", "BOS", "PHI", 9.5, "over"),
        ReboundMarket("Joel Embiid", "PHI", "BOS", 8.5, "over"),
        ReboundMarket("Jaylen Brown", "BOS", "PHI", 6.5, "over"),
        ReboundMarket("Neemias Queta", "BOS", "PHI", 6.5, "over"),
        ReboundMarket("Kelly Oubre Jr.", "PHI", "BOS", 4.5, "over"),
        ReboundMarket("Paul George", "PHI", "BOS", 4.5, "over"),
    ]

    minutes = [
        PlayerMinutes("Jayson Tatum", "BOS", 40),
        PlayerMinutes("Jaylen Brown", "BOS", 38),
        PlayerMinutes("Joel Embiid", "PHI", 34),
        PlayerMinutes("Kelly Oubre Jr.", "PHI", 35),
        PlayerMinutes("Paul George", "PHI", 36),
        PlayerMinutes("Neemias Queta", "BOS", 24),
    ]

    tracking = [
        PlayerReboundTracking("Jayson Tatum", "BOS", 4, 38, 10.0, 17.0, 58.8, 63.0, 30.0, 7.2),
        PlayerReboundTracking("Joel Embiid", "PHI", 2, 30, 8.5, 15.0, 56.7, 61.0, 42.0, 4.1),
        PlayerReboundTracking("Jaylen Brown", "BOS", 4, 36, 6.2, 11.0, 56.4, 60.0, 28.0, 7.8),
        PlayerReboundTracking("Neemias Queta", "BOS", 4, 24, 6.0, 10.0, 60.0, 64.0, 44.0, 3.5),
        PlayerReboundTracking("Kelly Oubre Jr.", "PHI", 4, 34, 4.0, 9.0, 44.4, 48.0, 25.0, 8.9),
        PlayerReboundTracking("Paul George", "PHI", 4, 36, 4.5, 9.5, 47.4, 51.0, 26.0, 8.2),
    ]

    detector = AutoReboundEdgeDetector(
        blowout_probability=0.60,
        competitive_probability=0.40,
        pace_scalar=0.98,
        missed_shot_scalar=1.04,
        long_rebound_scalar=1.03,
    )

    results = detector.run(
        markets=markets,
        minutes=minutes,
        tracking=tracking,
        team_rebound_modifiers={"BOS": 1.04, "PHI": 0.98},
        opponent_miss_modifiers={"BOS": 1.02, "PHI": 1.05},
        role_modifiers={
            "Jayson Tatum": 1.03,
            "Joel Embiid": 1.02,
            "Kelly Oubre Jr.": 0.94,
            "Paul George": 0.96,
        },
    )

    save_results_json(results, "auto_rebound_edge_results.json")

    for r in results:
        print(
            f"{r.confidence_tier} | {r.player} {r.side.upper()} {r.line} | "
            f"Mean {r.mean} | Median {r.median} | Hit {round(r.hit_probability * 100, 1)}% | "
            f"Tags: {', '.join(r.risk_tags)}"
        )
