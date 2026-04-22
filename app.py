import streamlit as st
import json
from src.graph.workflow import build_graph

# ----------------------------
# Helpers
# ----------------------------
def safe_json(data):
    if isinstance(data, str):
        try:
            return json.loads(data)
        except:
            return {"raw": data}
    return data or {}

def extract_bull(data):
    data = safe_json(data)
    if isinstance(data, dict) and "bull_argument" in data:
        return safe_json(data["bull_argument"])
    return data

def extract_bear(data):
    data = safe_json(data)
    if isinstance(data, dict) and "bear_argument" in data:
        return safe_json(data["bear_argument"])
    return data


# ----------------------------
# PAGE SETUP
# ----------------------------
st.set_page_config(layout="wide")
st.title("🏛️ AI Trading Debate System")

ticker = st.text_input("Ticker", "AAPL")
run = st.button("Run Analysis")


# ----------------------------
# RUN
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

    st.info("🚀 Running analysis...")

    # FIXED: proper stage tracking
    stages = [
        "Technical analysis",
        "Sentiment analysis",
        "News analysis",
        "Fundamentals analysis",
        "Bull debate",
        "Bear debate",
        "Final decision"
    ]

    progress = st.progress(0)
    current_stage = 0


    # ----------------------------
    # STREAM EXECUTION
    # ----------------------------
    for step in app.stream(initial_state):
        for node, update in step.items():

            final_state.update(update)

            # advance progress ONLY per meaningful stage
            if node in ["technical", "sentiment", "news", "fundamentals", "bull", "bear", "decision"]:
                progress.progress((current_stage + 1) / len(stages))
                current_stage += 1

            st.write(f"### {node}")
            st.success("Completed")


    st.success("✅ Analysis complete")


    # ----------------------------
    # ANALYST SECTION
    # ----------------------------
    st.header("📊 Market Analysis")

    col1, col2 = st.columns(2)

    with col1:
        tech = safe_json(final_state.get("technical"))
        st.subheader("Technical")
        st.write(tech.get("summary", "No summary available"))

        with st.expander("Full technical data"):
            st.json(tech)

    with col2:
        sent = safe_json(final_state.get("sentiment"))
        st.subheader("Sentiment")
        st.write(sent.get("insight", "No summary available"))

        with st.expander("Full sentiment data"):
            st.json(sent)


    news = safe_json(final_state.get("news"))
    fund = safe_json(final_state.get("fundamentals"))

    st.subheader("📰 News")
    st.write(news.get("summary", "No summary available"))

    with st.expander("Full news data"):
        st.json(news)

    st.subheader("📈 Fundamentals")
    st.write(fund.get("summary", "No summary available"))

    with st.expander("Full fundamentals data"):
        st.json(fund)


    # ----------------------------
    # DEBATE SECTION (FIXED STRUCTURE)
    # ----------------------------
    st.header("⚔️ Debate Breakdown")

    bull = extract_bull(final_state.get("bull_argument"))
    bear = extract_bear(final_state.get("bear_argument"))

    history = final_state.get("debate_history", [])

    # safely extract rounds
    def find_round(role, idx):
        for msg in history:
            if msg.get("speaker") == role:
                if idx == 0:
                    return msg.get("content")
                idx -= 1
        return None


    # ----------------------------
    # ROUND 1
    # ----------------------------
    st.subheader("🟢 Round 1")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🐂 Bull (Round 1)")
        st.write(find_round("bull", 0) or bull.get("summary", "No summary"))

    with col2:
        st.markdown("### 🐻 Bear (Round 1)")
        st.write(find_round("bear", 0) or bear.get("summary", "No summary"))


    # ----------------------------
    # ROUND 2
    # ----------------------------
    st.subheader("🔁 Round 2 (Rebuttals)")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 🐂 Bull Response")
        st.write(find_round("bull", 1) or "No rebuttal available")

    with col4:
        st.markdown("### 🐻 Bear Final Response")
        st.write(find_round("bear", 1) or "No rebuttal available")


    # ----------------------------
    # FINAL DECISION
    # ----------------------------
    st.header("⚖️ Final Decision")

    dec = safe_json(final_state.get("decision"))

    st.subheader(dec.get("decision", "N/A"))
    st.write("**Confidence:**", dec.get("confidence", 0))
    st.write(dec.get("reasoning", "No reasoning provided"))

    st.write("### Key Factors")
    st.write(dec.get("key_factors", []))


    # ----------------------------
    # CLEAN DROPDOWNS PER SECTION
    # ----------------------------

    st.subheader("📜 Bull Full Output")
    with st.expander("Show bull JSON"):
        st.json(bull)

    st.subheader("📜 Bear Full Output")
    with st.expander("Show bear JSON"):
        st.json(bear)

    st.subheader("🧠 Debate History (Raw)")
    with st.expander("Show full debate log"):
        st.json(history)

    st.subheader("🧾 System State (Debug)")
    with st.expander("Show full state"):
        st.json(final_state)