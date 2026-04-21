import json
from pathlib import Path
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SharpEdge Bankroll Dashboard", layout="wide")

st.title("📈 SharpEdge Bankroll Curve + Performance")
st.caption("Tracks bankroll growth, ROI progression, and drawdowns from outcome logs.")

OUTCOME_PATH = "runtime/liveflow_outcomes_log.jsonl"

file = Path(OUTCOME_PATH)

if not file.exists():
    st.warning("No outcome log found. Run outcome tracker first.")
    st.stop()

rows = []
with file.open("r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            rows.append(json.loads(line))

df = pd.DataFrame(rows)

if df.empty:
    st.warning("No data available.")
    st.stop()

df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"])
df = df.sort_values("timestamp_utc")

starting_bankroll = st.sidebar.number_input("Starting Bankroll", value=100.0)

df["cumulative_profit"] = df["profit"].cumsum()
df["bankroll"] = starting_bankroll + df["cumulative_profit"]
df["peak"] = df["bankroll"].cummax()
df["drawdown"] = df["bankroll"] - df["peak"]

total_profit = df["profit"].sum()
roi = (total_profit / df["stake"].sum()) * 100 if df["stake"].sum() > 0 else 0
win_rate = (df["result"] == "WIN").mean() * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("Bankroll", round(df["bankroll"].iloc[-1], 2))
col2.metric("Total Profit", round(total_profit, 2))
col3.metric("ROI %", round(roi, 2))
col4.metric("Win Rate %", round(win_rate, 2))

st.divider()

st.subheader("📈 Bankroll Curve")
fig, ax = plt.subplots()
ax.plot(df["timestamp_utc"], df["bankroll"])
ax.set_title("Bankroll Over Time")
ax.set_xlabel("Time")
ax.set_ylabel("Bankroll")
st.pyplot(fig)

st.subheader("📉 Drawdown")
fig2, ax2 = plt.subplots()
ax2.plot(df["timestamp_utc"], df["drawdown"])
ax2.set_title("Drawdown Over Time")
st.pyplot(fig2)

st.subheader("📊 Profit Per Bet")
fig3, ax3 = plt.subplots()
ax3.bar(range(len(df)), df["profit"])
ax3.set_title("Profit Distribution")
st.pyplot(fig3)

st.divider()
st.subheader("Raw Data")
st.dataframe(df)
