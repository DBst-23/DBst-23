import json
from pathlib import Path
from typing import Dict

HIT_RATE_PATH = Path("runtime/liveflow_middle_band_hit_rate.json")


def load_middle_hit_rate(default_rate: float = 0.18) -> float:
    if not HIT_RATE_PATH.exists():
        return default_rate
    try:
        data = json.loads(HIT_RATE_PATH.read_text(encoding="utf-8"))
        rate = float(data.get("middle_hit_rate", default_rate))
        if 0.0 <= rate <= 1.0:
            return rate
    except Exception:
        pass
    return default_rate


def calculate_middle_band_ev(
    entry_line: float,
    updated_line: float,
    stake_primary: float,
    stake_secondary: float,
    estimated_middle_hit_rate: float,
    primary_payout_multiple: float,
    secondary_payout_multiple: float,
) -> Dict[str, float]:
    band_width = abs(updated_line - entry_line)

    gross_win_primary = stake_primary * primary_payout_multiple - stake_primary
    gross_win_secondary = stake_secondary * secondary_payout_multiple - stake_secondary

    middle_profit = gross_win_primary + gross_win_secondary
    split_primary_only = gross_win_primary - stake_secondary
    split_secondary_only = gross_win_secondary - stake_primary
    full_loss = -(stake_primary + stake_secondary)

    remaining = max(0.0, 1.0 - estimated_middle_hit_rate)
    primary_only_rate = remaining * 0.30
    secondary_only_rate = remaining * 0.35
    full_loss_rate = max(0.0, 1.0 - estimated_middle_hit_rate - primary_only_rate - secondary_only_rate)

    expected_profit = (
        estimated_middle_hit_rate * middle_profit
        + primary_only_rate * split_primary_only
        + secondary_only_rate * split_secondary_only
        + full_loss_rate * full_loss
    )

    total_staked = stake_primary + stake_secondary
    roi_pct = (expected_profit / total_staked) * 100.0 if total_staked > 0 else 0.0

    return {
        "band_width": round(band_width, 3),
        "middle_profit": round(middle_profit, 3),
        "primary_only_profit": round(split_primary_only, 3),
        "secondary_only_profit": round(split_secondary_only, 3),
        "full_loss": round(full_loss, 3),
        "estimated_middle_hit_rate": round(estimated_middle_hit_rate, 4),
        "expected_profit": round(expected_profit, 3),
        "expected_roi_pct": round(roi_pct, 3),
    }


def calculate_middle_band_kelly(
    bankroll: float,
    entry_line: float,
    updated_line: float,
    primary_payout_multiple: float = 1.80,
    secondary_payout_multiple: float = 1.80,
    base_stake_fraction: float = 0.01,
    hit_rate_override: float | None = None,
) -> Dict[str, float]:
    hit_rate = hit_rate_override if hit_rate_override is not None else load_middle_hit_rate()

    probe_stake = max(1.0, bankroll * base_stake_fraction)
    ev = calculate_middle_band_ev(
        entry_line=entry_line,
        updated_line=updated_line,
        stake_primary=probe_stake,
        stake_secondary=probe_stake,
        estimated_middle_hit_rate=hit_rate,
        primary_payout_multiple=primary_payout_multiple,
        secondary_payout_multiple=secondary_payout_multiple,
    )

    total_staked = probe_stake * 2
    b = max(0.0001, ((primary_payout_multiple + secondary_payout_multiple) / 2.0) - 1.0)
    p = max(0.0, min(1.0, hit_rate))
    q = 1.0 - p

    raw_kelly = (b * p - q) / b
    raw_kelly = max(0.0, raw_kelly)

    ev_scale = max(0.0, ev["expected_roi_pct"] / 100.0)
    adjusted_kelly = raw_kelly * min(1.0, max(0.1, ev_scale * 5.0))

    half_kelly_fraction = adjusted_kelly * 0.5
    recommended_total_stake = bankroll * half_kelly_fraction
    recommended_each_leg = recommended_total_stake / 2.0

    return {
        "bankroll": round(bankroll, 2),
        "loaded_hit_rate": round(hit_rate, 4),
        "band_width": ev["band_width"],
        "expected_profit_probe": ev["expected_profit"],
        "expected_roi_pct": ev["expected_roi_pct"],
        "raw_kelly_fraction": round(raw_kelly, 4),
        "adjusted_kelly_fraction": round(adjusted_kelly, 4),
        "half_kelly_fraction": round(half_kelly_fraction, 4),
        "recommended_total_stake": round(recommended_total_stake, 2),
        "recommended_each_leg": round(recommended_each_leg, 2),
        "probe_total_stake": round(total_staked, 2),
    }
