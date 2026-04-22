from typing import Dict


def calculate_middle_band_ev(
    entry_line: float,
    updated_line: float,
    stake_primary: float,
    stake_secondary: float,
    estimated_middle_hit_rate: float,
    primary_payout_multiple: float,
    secondary_payout_multiple: float,
) -> Dict[str, float]:
    """
    Estimate expected value of a two-entry middle band structure.

    Parameters
    ----------
    entry_line : float
        Original line taken.
    updated_line : float
        Second line taken after market movement.
    stake_primary : float
        Stake on the first ticket.
    stake_secondary : float
        Stake on the second ticket.
    estimated_middle_hit_rate : float
        Probability that the final result lands inside the middle band.
        Must be expressed as decimal form, e.g. 0.18 for 18%.
    primary_payout_multiple : float
        Total return multiple for first ticket, e.g. 1.80 means $1 returns $1.80.
    secondary_payout_multiple : float
        Total return multiple for second ticket.

    Returns
    -------
    Dict[str, float]
        Dictionary with band width, gross middle win, split outcomes,
        full-loss outcome, and total expected profit.
    """

    band_width = abs(updated_line - entry_line)

    gross_win_primary = stake_primary * primary_payout_multiple - stake_primary
    gross_win_secondary = stake_secondary * secondary_payout_multiple - stake_secondary

    middle_profit = gross_win_primary + gross_win_secondary
    split_primary_only = gross_win_primary - stake_secondary
    split_secondary_only = gross_win_secondary - stake_primary
    full_loss = -(stake_primary + stake_secondary)

    # Simple structure model:
    # - middle_hit_rate => both win
    # - remaining mass split evenly across one-ticket wins and total loss bucket lightly penalized
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

    roi_pct = 0.0
    total_staked = stake_primary + stake_secondary
    if total_staked > 0:
        roi_pct = (expected_profit / total_staked) * 100.0

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
