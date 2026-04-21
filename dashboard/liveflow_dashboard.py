import json
import streamlit as st


st.set_page_config(page_title="SharpEdge LiveFlow Dashboard", layout="wide")

st.title("🔥 SharpEdge LiveFlow Dashboard")
st.caption("Paste a LiveFlow payload to visualize signals, confidence, and execution status.")

sample_payload = {
    "odds_snapshot": {
        "game_label": "MIN @ DEN",
        "sportsbook": "Kalshi",
        "closing_spread": -4.5,
        "closing_total": 231.5,
        "live_spread": -4.5,
        "live_total": 245.5,
    },
    "heat_result": {
        "heat_index": 68,
        "classification": "EXTREME_HEAT",
        "action_tag": "UNDER_TRIGGER",
        "shooting_heat_score": 19.2,
        "market_inflation_score": 38.0,
        "pace_support_score": 4.1,
    },
    "classifier_result": {
        "environment_type": "FAKE_INFLATION",
        "confidence": 0.71,
        "action_bias": "LEAN_UNDER",
    },
    "auto_adjustment": {
        "recommendation": "FIRE_UNDER",
        "confidence_tier": "HIGH",
        "weight_delta": 0.10,
        "reasons": [
            "heat index and halftime classifier aligned on under"
        ],
    },
    "confidence_result": {
        "confidence_score": 84,
        "confidence_tier": "LOCK",
        "confidence_emoji": "🔒",
        "recommended_units": "1.00u",
        "reasons": [
            "full under alignment across heat + classifier: +18",
            "meaningful repricing delta supports edge clarity: +6"
        ],
    }
}

with st.sidebar:
    st.header("Input")
    use_sample = st.checkbox("Load sample payload", value=True)

payload_text = st.text_area(
    "Paste JSON payload",
    value=json.dumps(sample_payload, indent=2) if use_sample else "",
    height=420,
)

try:
    payload = json.loads(payload_text) if payload_text.strip() else sample_payload
except Exception as e:
    st.error(f"Invalid JSON payload: {e}")
    st.stop()

odds = payload.get("odds_snapshot", {})
heat = payload.get("heat_result", {})
classifier = payload.get("classifier_result", {})
auto = payload.get("auto_adjustment", {})
confidence = payload.get("confidence_result", {})

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
exec_col1, exec_col2, exec_col3 = st.columns(3)
exec_col1.metric("Confidence Score", confidence.get("confidence_score", "—"))
exec_col2.metric("Recommended Units", confidence.get("recommended_units", "—"))
exec_col3.metric("Execution Tier", f"{confidence.get('confidence_emoji', '')} {confidence.get('confidence_tier', '—')}")

for reason in confidence.get("reasons", []):
    st.write(f"- {reason}")

st.divider()
st.subheader("Raw Payload")
st.json(payload)
