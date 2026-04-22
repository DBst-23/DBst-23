import json
from pathlib import Path
import streamlit as st

try:
    from streamlit_autorefresh import st_autorefresh
except Exception:
    st_autorefresh = None


st.set_page_config(page_title="SharpEdge LiveFlow AutoRefresh Dashboard", layout="wide")

st.title("🔥 SharpEdge LiveFlow AutoRefresh Dashboard")
st.caption("Reads the latest LiveFlow payload JSON automatically and refreshes on a loop.")

DEFAULT_PAYLOAD_PATH = "runtime/latest_liveflow_payload.json"
DEFAULT_REFRESH_MS = 5000

with st.sidebar:
    st.header("Source")
    payload_path = st.text_input("Payload JSON path", value=DEFAULT_PAYLOAD_PATH)
    enable_autorefresh = st.checkbox("Enable auto-refresh", value=True)
    refresh_ms = st.number_input(
        "Refresh interval (ms)",
        min_value=1000,
        max_value=60000,
        value=DEFAULT_REFRESH_MS,
        step=1000,
    )
    st.button("Refresh now")

if enable_autorefresh:
    if st_autorefresh is not None:
        st_autorefresh(interval=int(refresh_ms), key="liveflow_dashboard_refresh")
    else:
        st.warning("Install streamlit-autorefresh to enable timed refresh: pip install streamlit-autorefresh")

payload_file = Path(payload_path)

if not payload_file.exists():
    st.warning(f"No payload file found at: {payload_file}")
    st.info("Run your trigger/bridge script and export the payload JSON to this path, then refresh.")
    st.stop()

try:
    payload = json.loads(payload_file.read_text(encoding="utf-8"))
except Exception as e:
    st.error(f"Could not read payload JSON: {e}")
    st.stop()

odds = payload.get("odds_snapshot", {})
heat = payload.get("heat_result", {})
classifier = payload.get("classifier_result", {})
auto = payload.get("auto_adjustment", {})
confidence = payload.get("confidence_result", {})
trigger = payload.get("trigger_result", {})
kelly = payload.get("kelly_result", {})
middle = payload.get("middle_band", {}) or trigger.get("middle_band", {})

col1, col2, col3, col4 = st.columns(4)
col1.metric("Game", odds.get("game_label", "—"))
col2.metric("Live Total", odds.get("live_total", "—"))
col3.metric("Heat Index", heat.get("heat_index", "—"))
col4.metric("Confidence", f"{confidence.get('confidence_emoji', '')} {confidence.get('confidence_tier', '—')}")

st.divider()

left, right = st.columns([1, 1])

with left:
    st.subheader("📡 Market Snapshot")
    st.json(odds)

    st.subheader("🔥 Heat Engine")
    st.write(f"**Classification:** {heat.get('classification', '—')}")
    st.write(f"**Action Tag:** {heat.get('action_tag', '—')}")
    st.write(f"**Shooting Heat Score:** {heat.get('shooting_heat_score', '—')}")
    st.write(f"**Market Inflation Score:** {heat.get('market_inflation_score', '—')}")
    st.write(f"**Pace Support Score:** {heat.get('pace_support_score', '—')}")

with right:
    st.subheader("🧠 Classifier")
    st.write(f"**Environment Type:** {classifier.get('environment_type', '—')}")
    st.write(f"**Confidence:** {classifier.get('confidence', '—')}")
    st.write(f"**Action Bias:** {classifier.get('action_bias', '—')}")

    st.subheader("🤖 Auto Adjuster")
    st.write(f"**Recommendation:** {auto.get('recommendation', '—')}")
    st.write(f"**Confidence Tier:** {auto.get('confidence_tier', '—')}")
    st.write(f"**Weight Delta:** {auto.get('weight_delta', '—')}")
    for reason in auto.get("reasons", []):
        st.write(f"- {reason}")

st.divider()

st.subheader("🎯 Execution")
exec_col1, exec_col2, exec_col3, exec_col4 = st.columns(4)
exec_col1.metric("Confidence Score", confidence.get("confidence_score", "—"))
exec_col2.metric("Recommended Units", confidence.get("recommended_units", "—"))
exec_col3.metric("Execution Tier", f"{confidence.get('confidence_emoji', '')} {confidence.get('confidence_tier', '—')}")
exec_col4.metric("Should Fire", trigger.get("should_fire", payload.get("should_fire", "—")))

for reason in confidence.get("reasons", []):
    st.write(f"- {reason}")

st.divider()

st.subheader("💰 Kelly Sizing")
kelly_col1, kelly_col2, kelly_col3, kelly_col4 = st.columns(4)
kelly_col1.metric("Kelly Total Stake", kelly.get("recommended_total_stake", "—"))
kelly_col2.metric("Kelly Each Leg", kelly.get("recommended_each_leg", "—"))
kelly_col3.metric("Half Kelly %", kelly.get("half_kelly_fraction", "—"))
kelly_col4.metric("Expected ROI %", kelly.get("expected_roi_pct", "—"))

if kelly:
    st.json(kelly)

st.divider()

st.subheader("🎯 Middle Band")
if middle:
    middle_col1, middle_col2, middle_col3 = st.columns(3)
    middle_col1.metric("Band Width", middle.get("band_width", "—"))
    middle_col2.metric("Classification", middle.get("classification", "—"))
    middle_col3.metric("Confidence Boost", payload.get("confidence_boost", trigger.get("confidence_boost", "—")))
    st.json(middle)
else:
    st.info("No active middle band on current payload.")

st.divider()
st.subheader("Raw Payload")
st.json(payload)
