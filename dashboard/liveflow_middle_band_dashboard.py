import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="SharpEdge Middle Band Dashboard", layout="wide")

st.title("🎯 SharpEdge Middle Band Dashboard")
st.caption("Visualizes live middle-band opportunities detected by the LiveFlow bridge.")

DEFAULT_PATH = "runtime/liveflow_middle_band_log.jsonl"

with st.sidebar:
    st.header("Source")
    log_path = st.text_input("Middle band log path", value=DEFAULT_PATH)
    st.button("Refresh")

log_file = Path(log_path)

if not log_file.exists():
    st.warning(f"Middle band log not found: {log_file}")
    st.info("Run the bridge logging workflow so middle-band signals are written to runtime/liveflow_middle_band_log.jsonl.")
    st.stop()

rows = []
with log_file.open("r", encoding="utf-8") as f:
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

latest = rows[-1]
active = [r for r in rows if r.get("middle_active")]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Logged", len(rows))
col2.metric("Active Middles", len(active))
col3.metric("Latest Band Width", latest.get("band_width", 0))
col4.metric("Latest Classification", latest.get("classification", "N/A"))

st.divider()

st.subheader("Latest Middle Band Signal")
st.json(latest)

st.subheader("Active Middle Band Signals")
for idx, row in enumerate(reversed(active[-20:]), 1):
    with st.expander(f"Signal {idx}: {row.get('classification', 'MIDDLE_CAPTURE_WINDOW')}"):
        st.json(row)

st.divider()
st.subheader("Raw Middle Band Log")
st.json(rows)
