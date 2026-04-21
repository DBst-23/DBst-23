import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="SharpEdge ROI Dashboard", layout="wide")

st.title("📈 SharpEdge ROI Dashboard")
st.caption("Displays LiveFlow ROI, win rate, tier performance, and market-type performance from the runtime tracker.")

DEFAULT_ROI_PATH = "runtime/liveflow_roi_tracker_summary.json"
DEFAULT_EDGE_PATH = "runtime/liveflow_edge_tracker_summary.json"

with st.sidebar:
    st.header("Sources")
    roi_path = st.text_input("ROI tracker path", value=DEFAULT_ROI_PATH)
    edge_path = st.text_input("Edge tracker path", value=DEFAULT_EDGE_PATH)
    st.button("Refresh")

roi_file = Path(roi_path)
edge_file = Path(edge_path)

if not roi_file.exists():
    st.warning(f"ROI tracker file not found: {roi_file}")
    st.info("Run scripts/liveflow_outcome_roi_tracker.py first, then refresh.")
    st.stop()

try:
    roi = json.loads(roi_file.read_text(encoding="utf-8"))
except Exception as e:
    st.error(f"Could not read ROI tracker JSON: {e}")
    st.stop()

edge = {}
if edge_file.exists():
    try:
        edge = json.loads(edge_file.read_text(encoding="utf-8"))
    except Exception:
        edge = {}

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Bets", roi.get("total_bets", 0))
col2.metric("Win Rate %", roi.get("win_rate_pct", 0.0))
col3.metric("ROI %", roi.get("roi_pct", 0.0))
col4.metric("Profit", roi.get("total_profit", 0.0))

st.divider()

left, right = st.columns([1, 1])

with left:
    st.subheader("💰 Bankroll / ROI Summary")
    st.json({
        "total_staked": roi.get("total_staked", 0.0),
        "total_payout": roi.get("total_payout", 0.0),
        "total_profit": roi.get("total_profit", 0.0),
        "win_rate_pct": roi.get("win_rate_pct", 0.0),
        "roi_pct": roi.get("roi_pct", 0.0),
    })

    st.subheader("🎯 Confidence Tier Performance")
    st.json(roi.get("by_confidence_tier", {}))

with right:
    st.subheader("📊 Market Type Performance")
    st.json(roi.get("by_market_type", {}))

    st.subheader("🧠 Edge Tracker Snapshot")
    if edge:
        st.json(edge)
    else:
        st.info("No edge tracker summary found yet.")

st.divider()
st.subheader("Raw ROI Summary")
st.json(roi)
