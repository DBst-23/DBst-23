"""
SharpEdge NBA B.003 — Flat vs Kelly Performance Comparison

Purpose:
Compare flat-unit staking vs fractional Kelly staking using the output files
created by rolling_window_runner.pie.

Expected inputs:
- outputs/model_validation/bankroll_filtered_active.csv
- outputs/model_validation/bankroll_kelly_active.csv

Outputs:
- outputs/model_validation/flat_vs_kelly_summary.csv
- outputs/model_validation/flat_vs_kelly_report.md
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

OUTPUT_DIR = Path("outputs/model_validation")
FLAT_PATH = OUTPUT_DIR / "bankroll_filtered_active.csv"
KELLY_PATH = OUTPUT_DIR / "bankroll_kelly_active.csv"
SUMMARY_PATH = OUTPUT_DIR / "flat_vs_kelly_summary.csv"
REPORT_PATH = OUTPUT_DIR / "flat_vs_kelly_report.md"


def summarize_bankroll(df: pd.DataFrame, strategy_name: str) -> dict:
    if df.empty:
        return {
            "strategy": strategy_name,
            "bets": 0,
            "wins": 0,
            "losses": 0,
            "hit_rate": np.nan,
            "total_staked": 0.0,
            "profit": 0.0,
            "roi": np.nan,
            "ending_bankroll": np.nan,
            "max_drawdown": np.nan,
            "avg_stake": np.nan,
            "largest_stake": np.nan,
        }

    wins = int((df["actual"] == 1).sum()) if "actual" in df.columns else np.nan
    losses = int((df["actual"] == 0).sum()) if "actual" in df.columns else np.nan
    bets = int(len(df))
    total_staked = float(df["stake"].sum()) if "stake" in df.columns else np.nan
    profit = float(df["profit"].sum()) if "profit" in df.columns else np.nan
    roi = profit / total_staked if total_staked else np.nan
    ending_bankroll = float(df["bankroll"].iloc[-1]) if "bankroll" in df.columns else np.nan
    max_drawdown = float(df["drawdown"].min()) if "drawdown" in df.columns else np.nan

    return {
        "strategy": strategy_name,
        "bets": bets,
        "wins": wins,
        "losses": losses,
        "hit_rate": wins / bets if bets else np.nan,
        "total_staked": total_staked,
        "profit": profit,
        "roi": roi,
        "ending_bankroll": ending_bankroll,
        "max_drawdown": max_drawdown,
        "avg_stake": float(df["stake"].mean()) if "stake" in df.columns else np.nan,
        "largest_stake": float(df["stake"].max()) if "stake" in df.columns else np.nan,
    }


def main() -> None:
    missing = [str(path) for path in [FLAT_PATH, KELLY_PATH] if not path.exists()]
    if missing:
        print("Missing bankroll output files:")
        for path in missing:
            print(f"- {path}")
        print("Run nba/model_validation/rolling_window_runner.pie first.")
        return

    flat = pd.read_csv(FLAT_PATH)
    kelly = pd.read_csv(KELLY_PATH)

    summary_df = pd.DataFrame([
        summarize_bankroll(flat, "flat_unit_active"),
        summarize_bankroll(kelly, "fractional_kelly_active"),
    ])

    summary_df.to_csv(SUMMARY_PATH, index=False)

    flat_row = summary_df.iloc[0]
    kelly_row = summary_df.iloc[1]

    report = f"""# SharpEdge B.003 — Flat vs Kelly Performance Comparison

## Summary

| Strategy | Bets | Hit Rate | Total Staked | Profit | ROI | Ending Bankroll | Max Drawdown | Avg Stake | Largest Stake |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Flat Unit | {flat_row['bets']} | {flat_row['hit_rate']:.3f} | {flat_row['total_staked']:.2f} | {flat_row['profit']:.2f} | {flat_row['roi']:.3f} | {flat_row['ending_bankroll']:.2f} | {flat_row['max_drawdown']:.2f} | {flat_row['avg_stake']:.2f} | {flat_row['largest_stake']:.2f} |
| Fractional Kelly | {kelly_row['bets']} | {kelly_row['hit_rate']:.3f} | {kelly_row['total_staked']:.2f} | {kelly_row['profit']:.2f} | {kelly_row['roi']:.3f} | {kelly_row['ending_bankroll']:.2f} | {kelly_row['max_drawdown']:.2f} | {kelly_row['avg_stake']:.2f} | {kelly_row['largest_stake']:.2f} |

## Interpretation Rules

- If Kelly profit > flat profit and max drawdown is controlled, the probability model is sizing edge efficiently.
- If Kelly profit < flat profit but drawdown is lower, the sizing is safer but may be too conservative.
- If Kelly drawdown is much worse, reduce kelly_multiplier or max_unit_multiple.
- If flat outperforms Kelly consistently, probability calibration needs work before aggressive sizing.

## Current B.003 Default Risk Settings

- Kelly multiplier: 0.25
- Base unit: 10
- Max unit multiple: 2.0
- Max stake cap: 20

## Next Tuning Step

Run multiple Kelly profiles:
- 0.10 Kelly
- 0.25 Kelly
- 0.50 Kelly

Then compare ROI, ending bankroll, and max drawdown.
"""

    REPORT_PATH.write_text(report, encoding="utf-8")

    print("Flat vs Kelly Summary:")
    print(summary_df)
    print(f"\nSaved: {SUMMARY_PATH}")
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
