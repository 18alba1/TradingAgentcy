import streamlit as st
import json
from src.graph.workflow import build_graph

# ----------------------------
# Helpers
# ----------------------------
def safe(data):
    """Safely handle dict / string / nested JSON"""
    if isinstance(data, str):
        try:
            return json.loads(data)
        except:
            return {"raw": data}
    return data or {}

def extract_bull(data):
    """Fix nested bull output"""
    if not data:
        return {}
    if isinstance(data, dict) and "bull_argument" in data:
        inner = data["bull_argument"]
        if isinstance(inner, str):
            try:
                return json.loads(inner)
            except:
                return {"raw": inner}
        return inner
    return data

def extract_bear(data):
    if not data:
        return {}
    if isinstance(data, dict) and "bear_argument" in data:
        inner = data["bear_argument"]
        if isinstance(inner, str):
            try:
                return json.loads(inner)
            except:
                return {"raw": inner}
        return inner
    return data


# ----------------------------
# UI
# ----------------------------
st.set_page_config(layout="wide")
st.title("🏛️ Trading Agent Debug Terminal")

ticker = st.text_input("Ticker", "AAPL")

run = st.button("Run Analysis")

# ----------------------------
# RUN GRAPH
# ----------------------------
if run:
    app = build_graph()

    initial_state = {
        "ticker": ticker,
        "round": 0,
        "debate_history": [],
        "technical": {},
        "sentiment": {},
        "news": {},
        "fundamentals": {},
        "bull_argument": {},
        "bear_argument": {},
        "decision": {}
    }

    final_state = initial_state.copy()

    st.info("Running workflow...")

    for step in app.stream(initial_state):
        for node, update in step.items():
            final_state.update(update)
            st.write(f"### Node: {node}")
            st.json(update)

    st.success("Workflow complete")

    # ----------------------------
    # DISPLAY RESULTS
    # ----------------------------

    st.header("📊 Technical")
    tech = safe(final_state.get("technical"))
    st.write(tech.get("summary", "No summary"))
    with st.expander("Full technical data"):
        st.json(tech)

    st.header("💬 Sentiment")
    sent = safe(final_state.get("sentiment"))
    st.write(sent.get("insight", "No insight"))
    with st.expander("Full sentiment data"):
        st.json(sent)

    st.header("📰 News")
    news = safe(final_state.get("news"))
    st.write(news.get("summary", "No summary"))
    with st.expander("Full news data"):
        st.json(news)

    st.header("📈 Fundamentals")
    fund = safe(final_state.get("fundamentals"))
    st.write(fund.get("summary", "No summary"))
    with st.expander("Full fundamentals data"):
        st.json(fund)

    # ----------------------------
    # BULL
    # ----------------------------
    st.header("🐂 Bull Case")
    bull = extract_bull(final_state.get("bull_argument"))
    st.write(bull.get("summary", "No summary"))
    with st.expander("Full bull data"):
        st.json(bull)

    # ----------------------------
    # BEAR
    # ----------------------------
    st.header("🐻 Bear Case")
    bear = extract_bear(final_state.get("bear_argument"))
    st.write(bear.get("summary", "No summary"))
    with st.expander("Full bear data"):
        st.json(bear)

    # ----------------------------
    # DECISION
    # ----------------------------
    st.header("⚖️ Final Decision")
    dec = safe(final_state.get("decision"))

    st.subheader(f"Decision: {dec.get('decision', 'N/A')}")
    st.write(f"Confidence: {dec.get('confidence', 0)}")

    st.write(dec.get("reasoning", "No reasoning"))

    with st.expander("Full decision data"):
        st.json(dec)

    # ----------------------------
    # DEBUG STATE (IMPORTANT)
    # ----------------------------
    st.divider()
    st.header("🧠 Full State Debug")
    st.json(final_state)