"""
SharpEdge Rebound Detector Runner V1

Purpose:
- Run the AutoReboundEdgeDetector from CSV inputs.
- Produce a ranked JSON edge board and optional CSV report.

Expected CSV formats:
1) markets_csv columns:
   player,team,opponent,line,side,price_decimal

2) minutes_csv columns:
   player,team,projected_minutes

3) tracking_csv columns:
   player,team,games,minutes,rebounds,rebound_chances,
   rebound_chance_pct,adjusted_rebound_chance_pct,
   contested_rebound_pct,avg_rebound_distance

Usage example:
python sharpedge/tools/run_rebound_detector.py \
  --markets data/nba/inputs/PHI_BOS_rebound_markets.csv \
  --minutes data/nba/inputs/PHI_BOS_projected_minutes.csv \
  --tracking data/nba/inputs/PHI_BOS_player_rebound_tracking.csv \
  --output-json outputs/PHI_BOS_rebound_edges.json \
  --output-csv outputs/PHI_BOS_rebound_edges.csv \
  --blowout-prob 0.60 \
  --pace-scalar 0.98 \
  --missed-shot-scalar 1.04 \
  --long-rebound-scalar 1.03
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from dataclasses import asdict
from typing import Dict, List, Optional

try:
    from sharpedge.tools.auto_rebound_edge_detector import (
        AutoReboundEdgeDetector,
        ReboundMarket,
        PlayerMinutes,
        PlayerReboundTracking,
        ReboundEdgeResult,
    )
except ModuleNotFoundError:
    from auto_rebound_edge_detector import (  # type: ignore
        AutoReboundEdgeDetector,
        ReboundMarket,
        PlayerMinutes,
        PlayerReboundTracking,
        ReboundEdgeResult,
    )


def _to_float(value: object, default: float = 0.0) -> float:
    if value is None:
        return default
    text = str(value).strip().replace("%", "")
    if text == "":
        return default
    try:
        return float(text)
    except ValueError:
        return default


def _to_int(value: object, default: int = 0) -> int:
    return int(round(_to_float(value, float(default))))


def read_csv(path: str) -> List[Dict[str, str]]:
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_markets(path: str) -> List[ReboundMarket]:
    rows = read_csv(path)
    markets: List[ReboundMarket] = []
    for row in rows:
        markets.append(
            ReboundMarket(
                player=row.get("player", "").strip(),
                team=row.get("team", "").strip(),
                opponent=row.get("opponent", "").strip(),
                line=_to_float(row.get("line"), 0.0),
                side=(row.get("side") or "over").strip().lower(),
                price_decimal=(
                    _to_float(row.get("price_decimal"), 0.0)
                    if row.get("price_decimal") not in (None, "")
                    else None
                ),
            )
        )
    return markets


def load_minutes(path: str) -> List[PlayerMinutes]:
    rows = read_csv(path)
    minutes: List[PlayerMinutes] = []
    for row in rows:
        minutes.append(
            PlayerMinutes(
                player=row.get("player", "").strip(),
                team=row.get("team", "").strip(),
                projected_minutes=_to_float(row.get("projected_minutes"), 0.0),
            )
        )
    return minutes


def load_tracking(path: str) -> List[PlayerReboundTracking]:
    rows = read_csv(path)
    tracking: List[PlayerReboundTracking] = []
    for row in rows:
        tracking.append(
            PlayerReboundTracking(
                player=row.get("player", "").strip(),
                team=row.get("team", "").strip(),
                games=_to_int(row.get("games"), 0),
                minutes=_to_float(row.get("minutes"), 0.0),
                rebounds=_to_float(row.get("rebounds"), 0.0),
                rebound_chances=_to_float(row.get("rebound_chances"), 0.0),
                rebound_chance_pct=_to_float(row.get("rebound_chance_pct"), 0.0),
                adjusted_rebound_chance_pct=_to_float(
                    row.get("adjusted_rebound_chance_pct"), 0.0
                ),
                contested_rebound_pct=_to_float(row.get("contested_rebound_pct"), 0.0),
                avg_rebound_distance=_to_float(row.get("avg_rebound_distance"), 0.0),
            )
        )
    return tracking


def parse_modifier_string(raw: Optional[str]) -> Dict[str, float]:
    """
    Parse simple modifier strings.

    Example:
      "BOS=1.04,PHI=0.98"
    """
    modifiers: Dict[str, float] = {}
    if not raw:
        return modifiers

    for chunk in raw.split(","):
        if "=" not in chunk:
            continue
        key, value = chunk.split("=", 1)
        key = key.strip()
        if not key:
            continue
        modifiers[key] = _to_float(value, 1.0)
    return modifiers


def ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def write_json(results: List[ReboundEdgeResult], path: str) -> None:
    ensure_parent_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(result) for result in results], f, indent=2)


def write_csv(results: List[ReboundEdgeResult], path: str) -> None:
    ensure_parent_dir(path)
    fieldnames = [
        "confidence_tier",
        "player",
        "team",
        "opponent",
        "side",
        "line",
        "mean",
        "median",
        "hit_probability",
        "edge_score",
        "risk_tags",
        "notes",
    ]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            row = asdict(result)
            row["risk_tags"] = "|".join(result.risk_tags)
            row["notes"] = "|".join(result.notes)
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def print_edge_board(results: List[ReboundEdgeResult], top_n: int = 20) -> None:
    print("\nSharpEdge Auto Rebound Edge Board")
    print("=" * 72)
    for idx, result in enumerate(results[:top_n], start=1):
        pct = round(result.hit_probability * 100, 1)
        tags = ", ".join(result.risk_tags) if result.risk_tags else "clean"
        print(
            f"{idx:02d}. {result.confidence_tier:<6} | "
            f"{result.player} {result.side.upper()} {result.line} | "
            f"Mean {result.mean} | Median {result.median} | Hit {pct}% | "
            f"Edge {result.edge_score} | Tags: {tags}"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run SharpEdge rebound edge detector.")
    parser.add_argument("--markets", required=True, help="Path to rebound market CSV.")
    parser.add_argument("--minutes", required=True, help="Path to projected minutes CSV.")
    parser.add_argument("--tracking", required=True, help="Path to player rebound tracking CSV.")
    parser.add_argument("--output-json", default="outputs/rebound_edges.json")
    parser.add_argument("--output-csv", default=None)
    parser.add_argument("--top-n", type=int, default=20)
    parser.add_argument("--blowout-prob", type=float, default=0.50)
    parser.add_argument("--competitive-prob", type=float, default=None)
    parser.add_argument("--pace-scalar", type=float, default=1.00)
    parser.add_argument("--missed-shot-scalar", type=float, default=1.00)
    parser.add_argument("--long-rebound-scalar", type=float, default=1.00)
    parser.add_argument("--team-rebound-modifiers", default=None)
    parser.add_argument("--opponent-miss-modifiers", default=None)
    parser.add_argument("--role-modifiers", default=None)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    competitive_prob = (
        1.0 - args.blowout_prob if args.competitive_prob is None else args.competitive_prob
    )

    markets = load_markets(args.markets)
    minutes = load_minutes(args.minutes)
    tracking = load_tracking(args.tracking)

    detector = AutoReboundEdgeDetector(
        blowout_probability=args.blowout_prob,
        competitive_probability=competitive_prob,
        pace_scalar=args.pace_scalar,
        missed_shot_scalar=args.missed_shot_scalar,
        long_rebound_scalar=args.long_rebound_scalar,
    )

    results = detector.run(
        markets=markets,
        minutes=minutes,
        tracking=tracking,
        team_rebound_modifiers=parse_modifier_string(args.team_rebound_modifiers),
        opponent_miss_modifiers=parse_modifier_string(args.opponent_miss_modifiers),
        role_modifiers=parse_modifier_string(args.role_modifiers),
    )

    write_json(results, args.output_json)
    if args.output_csv:
        write_csv(results, args.output_csv)

    print_edge_board(results, top_n=args.top_n)
    print(f"\nJSON saved: {args.output_json}")
    if args.output_csv:
        print(f"CSV saved: {args.output_csv}")


if __name__ == "__main__":
    main()
