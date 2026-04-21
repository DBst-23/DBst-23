import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="SharpEdge CLV vs ROI Dashboard", layout="wide")

st.title("📊 SharpEdge CLV vs ROI Dashboard")
st.caption("Compares closing line value with realized ROI to validate true edge vs variance.")

DEFAULT_ROI_PATH = "runtime/liveflow_roi_tracker_summary.json"
DEFAULT_CLV_PATH = "runtime/liveflow_clv_summary.json"
DEFAULT_EDGE_PATH = "runtime/liveflow_edge_tracker_summary.json"

with st.sidebar:
    st.header("Sources")
    roi_path = st.text_input("ROI tracker path", value=DEFAULT_ROI_PATH)
    clv_path = st.text_input("CLV summary path", value=DEFAULT_CLV_PATH)
    edge_path = st.text_input("Edge tracker path", value=DEFAULT_EDGE_PATH)
    st.button("Refresh")

roi_file = Path(roi_path)
clv_file = Path(clv_path)
edge_file = Path(edge_path)

if not roi_file.exists():
    st.warning(f"ROI tracker file not found: {roi_file}")
    st.info("Run scripts/liveflow_outcome_roi_tracker.py first, then refresh.")
    st.stop()

if not clv_file.exists():
    st.warning(f"CLV summary file not found: {clv_file}")
    st.info("Run scripts/liveflow_clv_tracker.py first, then refresh.")
    st.stop()

try:
    roi = json.loads(roi_file.read_text(encoding="utf-8"))
except Exception as e:
    st.error(f"Could not read ROI tracker JSON: {e}")
    st.stop()

try:
    clv = json.loads(clv_file.read_text(encoding="utf-8"))
except Exception as e:
    st.error(f"Could not read CLV summary JSON: {e}")
    st.stop()

edge = {}
if edge_file.exists():
    try:
        edge = json.loads(edge_file.read_text(encoding="utf-8"))
    except Exception:
        edge = {}

col1, col2, col3, col4 = st.columns(4)
col1.metric("ROI %", roi.get("roi_pct", 0.0))
col2.metric("Win Rate %", roi.get("win_rate_pct", 0.0))
col3.metric("Avg CLV", clv.get("avg_clv_delta", 0.0))
col4.metric("Beat Close %", clv.get("beat_closing_rate_pct", 0.0))

st.divider()

left, right = st.columns([1, 1])

with left:
    st.subheader("💰 ROI Summary")
    st.json({
        "total_bets": roi.get("total_bets", 0),
        "total_staked": roi.get("total_staked", 0.0),
        "total_payout": roi.get("total_payout", 0.0),
        "total_profit": roi.get("total_profit", 0.0),
        "roi_pct": roi.get("roi_pct", 0.0),
        "win_rate_pct": roi.get("win_rate_pct", 0.0),
    })

    st.subheader("🎯 ROI by Confidence Tier")
    st.json(roi.get("by_confidence_tier", {}))

with right:
    st.subheader("📉 CLV Summary")
    st.json({
        "total_tracked": clv.get("total_tracked", 0),
        "avg_clv_delta": clv.get("avg_clv_delta", 0.0),
        "beat_closing_count": clv.get("beat_closing_count", 0),
        "beat_closing_rate_pct": clv.get("beat_closing_rate_pct", 0.0),
    })

    st.subheader("📊 CLV by Market Type")
    st.json(clv.get("by_market_type", {}))

st.divider()

st.subheader("🧠 Edge Truth Overlay")
roi_pct = float(roi.get("roi_pct", 0.0) or 0.0)
beat_close_pct = float(clv.get("beat_closing_rate_pct", 0.0) or 0.0)
avg_clv = float(clv.get("avg_clv_delta", 0.0) or 0.0)

if roi_pct > 0 and beat_close_pct >= 50 and avg_clv > 0:
    st.success("True edge confirmed: profitable results + positive CLV + beating the market.")
elif roi_pct > 0 and (beat_close_pct < 50 or avg_clv <= 0):
    st.warning("Profit is positive, but CLV is weak. Possible variance-driven results or slow market timing.")
elif roi_pct <= 0 and beat_close_pct >= 50:
    st.info("Beating the close but not yet profitable. Edge may be real, results may be lagging.")
else:
    st.error("No validated edge yet: ROI and CLV both weak.")

if edge:
    st.subheader("📡 Edge Tracker Snapshot")
    st.json(edge)

st.divider()
st.subheader("Raw ROI Summary")
st.json(roi)

st.subheader("Raw CLV Summary")
st.json(clv)
