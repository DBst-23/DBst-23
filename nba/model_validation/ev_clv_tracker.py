"""
SharpEdge NBA B.003 — EV + CLV Tracking Module

Purpose:
- Attach market-implied probability, expected value, ROI, and CLV diagnostics
  to every EDGE_CALL_ACTIVE prediction.
- Support singles and card-level tracking.
- Preserve strict out-of-sample workflow by using only logged pregame prices
  and later comparing them to closing lines/results.

Expected input:
    data/predictions_log.json

Recommended required columns:
    prediction_id
    prediction_date
    game_id
    player
    market
    line
    side
    market_price
    closing_price
    model_probability
    stake
    payout
    result
    actual_value
    hit
    edge_status
    leg_count
    card_id

Notes:
- American odds are supported.
- Decimal payout multiple is supported if payout/stake are present.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


DATA_PATH = Path("data/predictions_log.json")
OUTPUT_DIR = Path("outputs/model_validation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def american_to_decimal(odds: Optional[float]) -> float:
    """Convert American odds to decimal odds."""
    if odds is None or pd.isna(odds):
        return np.nan
    odds = float(odds)
    if odds > 0:
        return 1.0 + odds / 100.0
    if odds < 0:
        return 1.0 + 100.0 / abs(odds)
    return np.nan


def american_to_implied_prob(odds: Optional[float]) -> float:
    """Convert American odds to implied probability before vig removal."""
    if odds is None or pd.isna(odds):
        return np.nan
    odds = float(odds)
    if odds > 0:
        return 100.0 / (odds + 100.0)
    if odds < 0:
        return abs(odds) / (abs(odds) + 100.0)
    return np.nan


def expected_value_per_dollar(model_prob: float, decimal_odds: float) -> float:
    """EV per $1 risked."""
    if pd.isna(model_prob) or pd.isna(decimal_odds):
        return np.nan
    profit_if_win = decimal_odds - 1.0
    return model_prob * profit_if_win - (1.0 - model_prob)


def add_ev_clv_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Market price fields
    if "market_price" not in df.columns:
        df["market_price"] = np.nan
    if "closing_price" not in df.columns:
        df["closing_price"] = np.nan
    if "model_probability" not in df.columns:
        df["model_probability"] = df.get("sharpedge_prob", np.nan)

    df["decimal_odds"] = df["market_price"].apply(american_to_decimal)
    df["market_implied_probability"] = df["market_price"].apply(american_to_implied_prob)
    df["closing_implied_probability"] = df["closing_price"].apply(american_to_implied_prob)

    df["edge_pct"] = df["model_probability"] - df["market_implied_probability"]
    df["ev_per_dollar"] = df.apply(
        lambda row: expected_value_per_dollar(row["model_probability"], row["decimal_odds"]),
        axis=1,
    )

    # CLV: positive when our entry beat the closing implied probability for our side.
    df["clv_implied_delta"] = df["closing_implied_probability"] - df["market_implied_probability"]

    # Stake and realized P/L
    if "stake" not in df.columns:
        df["stake"] = 1.0
    if "payout" not in df.columns:
        df["payout"] = np.nan

    if "hit" in df.columns:
        df["realized_profit"] = np.where(
            df["hit"] == 1,
            np.where(df["payout"].notna(), df["payout"] - df["stake"], df["stake"] * (df["decimal_odds"] - 1.0)),
            np.where(df["hit"] == 0, -df["stake"], 0.0),
        )
    else:
        df["realized_profit"] = np.nan

    df["expected_profit"] = df["stake"] * df["ev_per_dollar"]

    return df


def summarize(df: pd.DataFrame) -> dict:
    active = df.copy()
    if "edge_status" in active.columns:
        active = active[active["edge_status"].fillna("") == "EDGE_CALL_ACTIVE"]

    settled = active[active.get("hit", pd.Series(index=active.index, dtype=float)).isin([0, 1])]

    total_stake = float(settled["stake"].sum()) if "stake" in settled.columns else 0.0
    total_profit = float(settled["realized_profit"].sum()) if "realized_profit" in settled.columns else 0.0
    roi = total_profit / total_stake if total_stake else np.nan

    return {
        "active_predictions": int(len(active)),
        "settled_predictions": int(len(settled)),
        "hit_rate": float(settled["hit"].mean()) if len(settled) else np.nan,
        "total_stake": total_stake,
        "realized_profit": total_profit,
        "roi": roi,
        "average_model_probability": float(active["model_probability"].mean()) if "model_probability" in active.columns and len(active) else np.nan,
        "average_edge_pct": float(active["edge_pct"].mean()) if "edge_pct" in active.columns and len(active) else np.nan,
        "average_ev_per_dollar": float(active["ev_per_dollar"].mean()) if "ev_per_dollar" in active.columns and len(active) else np.nan,
        "average_clv_implied_delta": float(active["clv_implied_delta"].mean()) if "clv_implied_delta" in active.columns and len(active) else np.nan,
    }


def group_report(df: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    available = [col for col in group_cols if col in df.columns]
    if not available:
        return pd.DataFrame()

    settled = df[df.get("hit", pd.Series(index=df.index, dtype=float)).isin([0, 1])].copy()
    if settled.empty:
        return pd.DataFrame()

    grouped = settled.groupby(available).agg(
        bets=("prediction_id", "count") if "prediction_id" in settled.columns else ("hit", "count"),
        hit_rate=("hit", "mean"),
        stake=("stake", "sum"),
        profit=("realized_profit", "sum"),
        avg_edge=("edge_pct", "mean"),
        avg_ev=("ev_per_dollar", "mean"),
        avg_clv=("clv_implied_delta", "mean"),
    ).reset_index()

    grouped["roi"] = grouped["profit"] / grouped["stake"].replace(0, np.nan)
    return grouped.sort_values("profit", ascending=False)


def main() -> None:
    if not DATA_PATH.exists():
        print(f"Missing input file: {DATA_PATH}")
        print("Create data/predictions_log.json or point DATA_PATH to the active predictions file.")
        return

    df = pd.read_json(DATA_PATH)
    enriched = add_ev_clv_columns(df)

    summary = summarize(enriched)
    print("EV + CLV Summary:")
    print(summary)

    enriched_path = OUTPUT_DIR / "predictions_with_ev_clv.csv"
    enriched.to_csv(enriched_path, index=False)
    print(f"\nSaved enriched predictions: {enriched_path}")

    for cols, name in [
        (["market"], "by_market"),
        (["leg_count"], "by_leg_count"),
        (["home_away"], "by_home_away"),
        (["playoff_flag"], "by_playoff_flag"),
        (["confidence_tier"], "by_confidence_tier"),
        (["edge_status"], "by_edge_status"),
    ]:
        report = group_report(enriched, cols)
        if not report.empty:
            path = OUTPUT_DIR / f"ev_clv_{name}.csv"
            report.to_csv(path, index=False)
            print(f"Saved report: {path}")


if __name__ == "__main__":
    main()
