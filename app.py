import streamlit as st
import json
from src.graph.workflow import build_graph

# ----------------------------
# Helpers
# ----------------------------
def safe_json(data):
    """Safely handle dict / string / nested JSON"""
    if isinstance(data, str):
        try:
            return json.loads(data)
        except:
            return {"raw": data}
    return data or {}

def extract_bull(data):
    data = safe_json(data)

    if isinstance(data, dict) and "bull_argument" in data:
        inner = data["bull_argument"]
        return safe_json(inner)

    return data

def extract_bear(data):
    data = safe_json(data)

    if isinstance(data, dict) and "bear_argument" in data:
        inner = data["bear_argument"]
        return safe_json(inner)

    return data

def deep_update(original, update):
    """Safely merge nested state updates"""
    for k, v in update.items():
        if isinstance(v, dict) and isinstance(original.get(k), dict):
            original[k].update(v)
        else:
            original[k] = v
    return original


# ----------------------------
# UI Setup
# ----------------------------
st.set_page_config(layout="wide")
st.title("🏛️ Trading Agent Debate Terminal (v2)")

ticker = st.text_input("Ticker", "AAPL")
run = st.button("Run Analysis")


# ----------------------------
# RUN GRAPH
# ----------------------------
if run:
    app = build_graph()

    initial_state = {
        "ticker": ticker,

        "technical": {},
        "sentiment": {},
        "news": {},
        "fundamentals": {},

        "bull_argument": {},
        "bear_argument": {},

        "turn": "BULL_1",
        "debate_history": [],
    }

    final_state = initial_state.copy()

    st.info("Running workflow...")

    for step in app.stream(initial_state):
        for node, update in step.items():
            final_state = deep_update(final_state, update)

            st.write(f"### Node: {node}")
            st.json(update)

    st.success("Workflow complete")


    # ----------------------------
    # TECHNICAL
    # ----------------------------
    st.header("📊 Technical")

    tech = safe_json(final_state.get("technical"))
    st.write(tech.get("summary", "No summary"))

    with st.expander("Full technical data"):
        st.json(tech)


    # ----------------------------
    # SENTIMENT
    # ----------------------------
    st.header("💬 Sentiment")

    sent = safe_json(final_state.get("sentiment"))
    st.write(sent.get("insight", "No insight"))

    with st.expander("Full sentiment data"):
        st.json(sent)


    # ----------------------------
    # NEWS
    # ----------------------------
    st.header("📰 News")

    news = safe_json(final_state.get("news"))
    st.write(news.get("summary", "No summary"))

    with st.expander("Full news data"):
        st.json(news)


    # ----------------------------
    # FUNDAMENTALS
    # ----------------------------
    st.header("📈 Fundamentals")

    fund = safe_json(final_state.get("fundamentals"))
    st.write(fund.get("summary", "No summary"))

    with st.expander("Full fundamentals data"):
        st.json(fund)


    # ----------------------------
    # BULL CASE
    # ----------------------------
    st.header("🐂 Bull Case")

    bull = extract_bull(final_state.get("bull_argument"))

    st.subheader(bull.get("summary", "No summary"))

    st.write("### Catalysts")
    st.write(bull.get("key_catalysts", []))

    st.write("### Risk Acknowledgement")
    st.write(bull.get("risk_acknowledgement", []))

    st.write(f"Confidence: {bull.get('confidence', 0)}")

    with st.expander("Full bull data"):
        st.json(bull)


    # ----------------------------
    # BEAR CASE
    # ----------------------------
    st.header("🐻 Bear Case")

    bear = extract_bear(final_state.get("bear_argument"))

    st.subheader(bear.get("summary", "No summary"))

    st.write("### Key Risks")
    st.write(bear.get("key_risks", []))

    st.write("### Counter to Bull")
    st.write(bear.get("counter_to_bull", []))

    st.write("### Risk Drivers")
    st.write(bear.get("risk_drivers", []))

    st.write(f"Confidence: {bear.get('confidence', 0)}")

    with st.expander("Full bear data"):
        st.json(bear)


    # ----------------------------
    # DEBATE TIMELINE (NEW)
    # ----------------------------
    st.header("🧠 Debate Timeline")

    history = final_state.get("debate_history", [])

    if history:
        for i, msg in enumerate(history):
            speaker = msg.get("speaker", "unknown")
            content = msg.get("content", {})

            if speaker == "bull":
                st.markdown(f"### 🐂 Bull (Turn {i+1})")
            elif speaker == "bear":
                st.markdown(f"### 🐻 Bear (Turn {i+1})")
            else:
                st.markdown(f"### ❓ {speaker}")

            st.json(content)
            st.divider()
    else:
        st.write("No debate history available")


    # ----------------------------
    # FINAL DECISION
    # ----------------------------
    st.header("⚖️ Final Decision")

    dec = safe_json(final_state.get("decision"))

    st.subheader(f"Decision: {dec.get('decision', 'N/A')}")
    st.write(f"Confidence: {dec.get('confidence', 0)}")

    st.write(dec.get("reasoning", "No reasoning provided"))

    st.write("### Key Factors")
    st.write(dec.get("key_factors", []))

    with st.expander("Full decision data"):
        st.json(dec)


    # ----------------------------
    # DEBUG STATE
    # ----------------------------
    st.divider()
    st.header("🧠 Full State Debug")

    st.json(final_state)