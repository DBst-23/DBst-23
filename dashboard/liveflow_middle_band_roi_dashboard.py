import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="SharpEdge Middle Band ROI Dashboard", layout="wide")

st.title("📈 SharpEdge Middle Band ROI + Hit Rate Dashboard")
st.caption("Tracks middle-band opportunities, hit rate, and their contribution to ROI.")

DEFAULT_MIDDLE_PATH = "runtime/liveflow_middle_band_log.jsonl"
DEFAULT_LINKED_PATH = "runtime/liveflow_bet_records_linked.jsonl"

with st.sidebar:
    st.header("Sources")
    middle_path = st.text_input("Middle band log path", value=DEFAULT_MIDDLE_PATH)
    linked_path = st.text_input("Linked bet records path", value=DEFAULT_LINKED_PATH)
    st.button("Refresh")

middle_file = Path(middle_path)
linked_file = Path(linked_path)

if not middle_file.exists():
    st.warning(f"Middle band log not found: {middle_file}")
    st.info("Run the middle-band bridge logging flow first.")
    st.stop()

rows = []
with middle_file.open("r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except Exception:
                continue

if not rows:
    st.warning("No middle-band records available yet.")
    st.stop()

linked_rows = []
if linked_file.exists():
    with linked_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    linked_rows.append(json.loads(line))
                except Exception:
                    continue

active = [r for r in rows if r.get("middle_active")]
hit_rows = [r for r in rows if r.get("middle_active") and r.get("middle_hit") is True]
miss_rows = [r for r in rows if r.get("middle_active") and r.get("middle_hit") is False]

hit_rate = round((len(hit_rows) / len(active)) * 100, 2) if active else 0.0
avg_band_width = round(sum(float(r.get("band_width", 0.0) or 0.0) for r in active) / len(active), 3) if active else 0.0

linked_middle = [r for r in linked_rows if r.get("middle_band") or r.get("notes", "").find("middle") != -1]
linked_middle_profit = round(sum(float(r.get("profit", 0.0) or 0.0) for r in linked_middle), 2) if linked_middle else 0.0
linked_middle_count = len(linked_middle)
linked_middle_roi = round((linked_middle_profit / sum(float(r.get("stake", 0.0) or 0.0) for r in linked_middle)) * 100, 2) if linked_middle and sum(float(r.get("stake", 0.0) or 0.0) for r in linked_middle) > 0 else 0.0

latest = rows[-1]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Middle Signals Logged", len(rows))
col2.metric("Active Middles", len(active))
col3.metric("Middle Hit Rate %", hit_rate)
col4.metric("Avg Band Width", avg_band_width)

col5, col6, col7 = st.columns(3)
col5.metric("Linked Middle Bets", linked_middle_count)
col6.metric("Middle Profit", linked_middle_profit)
col7.metric("Middle ROI %", linked_middle_roi)

st.divider()

st.subheader("Latest Middle Band Signal")
st.json(latest)

st.subheader("Middle Hit / Miss Breakdown")
st.json({
    "active_middle_count": len(active),
    "middle_hits": len(hit_rows),
    "middle_misses": len(miss_rows),
    "middle_hit_rate_pct": hit_rate,
    "avg_band_width": avg_band_width,
})

st.subheader("Linked Bet ROI Contribution")
st.json({
    "linked_middle_count": linked_middle_count,
    "linked_middle_profit": linked_middle_profit,
    "linked_middle_roi_pct": linked_middle_roi,
})

if active:
    st.subheader("Recent Active Middle Signals")
    for idx, row in enumerate(reversed(active[-20:]), 1):
        with st.expander(f"Middle {idx}: {row.get('classification', 'MIDDLE_CAPTURE_WINDOW')}"):
            st.json(row)

if linked_middle:
    st.subheader("Linked Middle Bet Records")
    st.json(linked_middle)

st.divider()
st.subheader("Raw Middle Band Log")
st.json(rows)
