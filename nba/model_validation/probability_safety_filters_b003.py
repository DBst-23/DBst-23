"""
SharpEdge NBA B.003 — Probability Safety Filters

Purpose:
Apply high-priority probability downgrades and skip filters before a play can be
classified as EDGE_CALL_ACTIVE.

These rules came directly from postmortem + mental-run diagnostics:
- Secondary rebounders get overestimated when rebound chances are shared.
- Low-minute rebound props create hook-loss and rotation volatility.
- High-usage scorers can lose rebound equity.
- Low edge percentage plays should be skipped before card construction.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class FilterResult:
    pred_prob: float
    rebound_prob: float
    downgrade_prob: float
    skip_bet: bool
    tags: list[str]
    notes: list[str]


def apply_probability_safety_filters(row: Dict[str, Any]) -> FilterResult:
    """Apply B.003 safety filters to a prediction row.

    Expected row keys when available:
    - pred_prob
    - rebound_prob
    - downgrade_prob
    - player_role
    - rebound_chances_shared
    - projected_minutes
    - usage_rate
    - edge_pct
    """
    pred_prob = float(row.get("pred_prob", row.get("model_probability", 0.50)))
    rebound_prob = float(row.get("rebound_prob", pred_prob))
    downgrade_prob = float(row.get("downgrade_prob", 0.00))
    skip_bet = bool(row.get("skip_bet", False))

    tags: list[str] = []
    notes: list[str] = []

    player_role = row.get("player_role")
    rebound_chances_shared = bool(row.get("rebound_chances_shared", False))
    projected_minutes = row.get("projected_minutes")
    usage_rate = row.get("usage_rate")
    edge_pct = row.get("edge_pct")

    # 1. Secondary rebounder shared-chance downgrade
    if player_role == "secondary_rebounder" and rebound_chances_shared:
        downgrade_prob -= 0.04
        pred_prob -= 0.04
        rebound_prob -= 0.04
        tags.append("SECONDARY_REBOUNDER_SHARED_CHANCES_DOWNGRADE")
        notes.append("Secondary rebounder with shared rebound chances: downgrade_prob -= 0.04")

    # 2. Low-minute cap
    if projected_minutes is not None and float(projected_minutes) < 20:
        pred_prob = min(pred_prob, 0.55)
        rebound_prob = min(rebound_prob, 0.55)
        tags.append("LOW_MINUTES_PROBABILITY_CAP")
        notes.append("Projected minutes < 20: pred_prob capped at 0.55")

    # 3. High-usage rebound suppression
    if usage_rate is not None and float(usage_rate) > 30:
        rebound_prob -= 0.03
        pred_prob -= 0.03
        tags.append("HIGH_USAGE_REBOUND_SUPPRESSOR")
        notes.append("Usage rate > 30%: rebound_prob -= 0.03")

    # 4. Minimum edge filter
    if edge_pct is not None and float(edge_pct) < 0.03:
        skip_bet = True
        tags.append("EDGE_BELOW_3_PERCENT_SKIP")
        notes.append("edge_pct < 0.03: skip_bet = True")

    # Bounds
    pred_prob = max(0.01, min(0.99, pred_prob))
    rebound_prob = max(0.01, min(0.99, rebound_prob))

    return FilterResult(
        pred_prob=pred_prob,
        rebound_prob=rebound_prob,
        downgrade_prob=downgrade_prob,
        skip_bet=skip_bet,
        tags=tags,
        notes=notes,
    )


if __name__ == "__main__":
    sample = {
        "model_probability": 0.59,
        "rebound_prob": 0.59,
        "downgrade_prob": 0.00,
        "player_role": "secondary_rebounder",
        "rebound_chances_shared": True,
        "projected_minutes": 18,
        "usage_rate": 31.5,
        "edge_pct": 0.025,
    }

    result = apply_probability_safety_filters(sample)
    print(result)
