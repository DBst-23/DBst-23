from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import streamlit as st

from modules.performance_dashboard_engine import build_dashboard_payload


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = ROOT / "investor_audit" / "daily"


@st.cache_data
def load_jsonl_records(folder: Path) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    if not folder.exists():
        return records

    for path in sorted(folder.glob("settled_bets_*.jsonl")):
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return records


def records_to_dataframe(records: List[Dict[str, Any]]) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    for r in records:
        rows.append(
            {
                "date": r.get("date"),
                "entry_id": r.get("entry_id"),
                "sport": r.get("sport"),
                "matchup": r.get("matchup"),
                "mode": r.get("mode"),
                "market": r.get("market"),
                "platform": r.get("platform", r.get("book")),
                "result": r.get("result"),
                "stake": r.get("stake", r.get("filled_stake", 0.0)),
                "return_actual": r.get("return_actual", 0.0),
                "profit": float(r.get("return_actual", 0.0)) - float(r.get("stake", r.get("filled_stake", 0.0))),
                "clv_delta": r.get("clv_delta"),
                "legs_hit": r.get("legs_hit"),
                "legs_miss": r.get("legs_miss"),
            }
        )
    df = pd.DataFrame(rows)
    if not df.empty and "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def build_cumulative_profit(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    working = df.copy().sort_values("date")
    working["cumulative_profit"] = working["profit"].cumsum()
    return working


def main() -> None:
    st.set_page_config(page_title="SharpEdge Performance Dashboard", layout="wide")
    st.title("SharpEdge Performance Dashboard")
    st.caption("CLV, ROI, accuracy, and settled-bet performance from GitHub audit logs")

    records = load_jsonl_records(AUDIT_DIR)
    dashboard = build_dashboard_payload(records)
    df = records_to_dataframe(records)
    cumulative_df = build_cumulative_profit(df)

    summary = dashboard.get("summary", {})

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Bets", summary.get("total_bets", 0))
    c2.metric("Accuracy %", summary.get("accuracy_pct", 0.0))
    c3.metric("ROI %", summary.get("roi_pct", 0.0))
    c4.metric("Profit", f"${summary.get('total_profit', 0.0):,.2f}")
    c5.metric("Avg CLV", summary.get("avg_clv_delta", 0.0))

    st.subheader("Summary")
    st.json(dashboard.get("summary", {}))

    left, right = st.columns(2)

    with left:
        st.subheader("CLV Buckets")
        st.json(dashboard.get("clv_buckets", {}))

        st.subheader("Accuracy by Market")
        market_df = pd.DataFrame.from_dict(dashboard.get("accuracy_by_market", {}), orient="index")
        if not market_df.empty:
            st.dataframe(market_df)
        else:
            st.info("No market data available yet.")

    with right:
        st.subheader("ROI by Mode")
        roi_mode_df = pd.DataFrame.from_dict(dashboard.get("roi_by_mode", {}), orient="index")
        if not roi_mode_df.empty:
            st.dataframe(roi_mode_df)
        else:
            st.info("No mode data available yet.")

        st.subheader("Settled Bets Table")
        if not df.empty:
            st.dataframe(df.sort_values("date", ascending=False), use_container_width=True)
        else:
            st.info("No settled bet records found in investor_audit/daily.")

    st.subheader("Cumulative Profit")
    if not cumulative_df.empty:
        chart_df = cumulative_df[["date", "cumulative_profit"]].dropna()
        if not chart_df.empty:
            st.line_chart(chart_df.set_index("date"))
        else:
            st.info("Not enough dated records to chart cumulative profit.")
    else:
        st.info("No cumulative profit data available yet.")


if __name__ == "__main__":
    main()
