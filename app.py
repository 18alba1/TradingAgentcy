import streamlit as st
import json
import os
from dotenv import load_dotenv
from src.graph.workflow import build_graph
import yfinance as yf

# ----------------------------
# LOAD ENV
# ----------------------------
load_dotenv()
APP_PASSWORD = st.secrets["APP_PASSWORD"]

# ----------------------------
# AUTH SYSTEM
# ----------------------------
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.title("🔐 Trading Agentcy Login")

    password = st.text_input("Enter password", type="password")

    if st.button("Login"):
        if password == APP_PASSWORD:
            st.session_state.authenticated = True
            st.success("Logged in successfully")
            st.rerun()
        else:
            st.error("Incorrect password")

    return False


if not check_password():
    st.stop()

# ----------------------------
# HELPERS
# ----------------------------
def safe_json(data):
    if isinstance(data, str):
        try:
            return json.loads(data)
        except:
            return {"raw": data}
    return data or {}

# ----------------------------
# PAGE SETUP
# ----------------------------
st.set_page_config(layout="wide")
st.title("🏛️ Trading Agentcy")
st.write("VERSION 2")
# ----------------------------
# SYSTEM EXPLANATION
# ----------------------------
with st.expander("ℹ️ How the system works", expanded=True):
    st.markdown("""
This system simulates a **multi-agent trading decision process**:

### 📊 Analyst Team
- **Technical Analyst** → price trends, RSI, MACD  
- **Fundamental Analyst** → financial health & valuation  
- **News Analyst** → macro & company news impact  
- **Sentiment Analyst** → retail & market sentiment  

### ⚔️ Investment Debate Engine
- 🐂 **Bull Agent** → argues for upside  
- 🐻 **Bear Agent** → argues for downside  
- They debate over **2 rounds**:
  1. Initial arguments  
  2. Rebuttals  

### ⚖️ Decision Manager
- Aggregates everything  
- Outputs: **BUY / SELL / HOLD**
""")

ticker = st.text_input("Ticker", "AAPL")
run = st.button("Run Analysis")

# ----------------------------
# RUN
# ----------------------------
if run:
    app = build_graph()

    state = {
        "ticker": ticker,
        "technical": {},
        "sentiment": {},
        "news": {},
        "fundamentals": {},
        "bull_argument": {},
        "bear_argument": {},
        "round": 1,
        "debate_history": [],
    }

    final_state = state.copy()

    st.info("🚀 Running analysis...")

    # ----------------------------
    # STEP TRACKER
    # ----------------------------
    STEPS = [
        ("technical", "Technical Analysis"),
        ("sentiment", "Sentiment Analysis"),
        ("news", "News Analysis"),
        ("fundamentals", "Fundamental Analysis"),
        ("bull", "Bull Argument (Round 1)"),
        ("bear", "Bear Response (Round 1)"),
        ("bull", "Bull Rebuttal (Round 2)"),
        ("bear", "Bear Final (Round 2)"),
        ("decision", "Final Decision"),
    ]

    progress_bar = st.progress(0)
    step_box = st.empty()

    completed = []
    current = None

    # ----------------------------
    # STREAM EXECUTION
    # ----------------------------
    for step in app.stream(state):
        for node, update in step.items():
            final_state.update(update)

            current = node
            completed.append(node)

            # UI Steps
            step_ui = "### ⚙️ Execution Status\n"
            for i, (step_key, label) in enumerate(STEPS):
                if i < len(completed):
                    step_ui += f"✅ {label}\n"
                elif step_key == current:
                    step_ui += f"⏳ **{label} (running...)**\n"
                else:
                    step_ui += f"⬜ {label}\n"

            step_box.markdown(step_ui)

            progress_value = min(len(completed) / len(STEPS), 1.0)
            progress_bar.progress(progress_value)

            st.toast(f"{node} complete ✅")

    st.success("✅ Analysis complete")

    # ----------------------------
    # 📌 TOP DECISION DASHBOARD
    # ----------------------------
    st.header("📌 Investment Decision")

    dec = safe_json(final_state.get("decision", {}))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Decision", dec.get("decision", "N/A"))

    with col2:
        st.metric("Confidence", f"{round(dec.get('confidence', 0)*100)}%")

    with col3:
        st.metric("Risk Level", "Medium")

    st.write(dec.get("reasoning", "No reasoning"))
    st.divider()

    # ----------------------------
    # 📊 ANALYST SIGNALS
    # ----------------------------
    st.header("📊 Analyst Signals")

    col1, col2 = st.columns(2)

    with col1:
        tech = safe_json(final_state.get("technical"))
        st.subheader("Technical")
        st.write(tech.get("summary", "No summary"))

        with st.expander("Full technical"):
            st.json(tech)

    with col2:
        sent = safe_json(final_state.get("sentiment"))
        st.subheader("Sentiment")
        st.write(sent.get("insight", "No insight available"))

        with st.expander("Full sentiment"):
            st.json(sent)

    news = safe_json(final_state.get("news"))
    fund = safe_json(final_state.get("fundamentals"))

    st.subheader("📰 News")
    st.write(news.get("summary", "No summary"))

    with st.expander("Full news"):
        st.json(news)

    st.subheader("📈 Fundamentals")
    st.write(fund.get("summary", "No summary"))

    with st.expander("Full fundamentals"):
        st.json(fund)

    st.divider()

    # ----------------------------
    # ⚖️ BULL VS BEAR STRENGTH
    # ----------------------------
    st.header("⚖️ Bull vs Bear Strength")

    history = final_state.get("debate_history", [])

    def get_msg(role, round_num):
        for msg in history:
            if msg.get("speaker") == role and msg.get("round") == round_num:
                return msg.get("content")
        return None

    bull = get_msg("bull", 2) or get_msg("bull", 1)
    bear = get_msg("bear", 2) or get_msg("bear", 1)

    bull_conf = bull.get("confidence", 0) if bull else 0
    bear_conf = bear.get("confidence", 0) if bear else 0

    total = bull_conf + bear_conf + 1e-6
    st.progress(bull_conf / total)
    st.caption(f"Bull: {bull_conf:.2f} vs Bear: {bear_conf:.2f}")

    st.divider()

    # ----------------------------
    # ⚔️ DEBATE ENGINE
    # ----------------------------
    st.header("⚔️ Investment Debate Engine")

    # ROUND 1
    st.subheader("🟢 Round 1 — Initial Positions")

    col1, col2 = st.columns(2)

    with col1:
        b1 = get_msg("bull", 1)
        st.markdown("### 🐂 Bull")

        if b1:
            st.markdown("**Thesis**")
            st.write(b1.get("bull_argument"))

            st.markdown("**Key Catalysts**")
            st.write(b1.get("key_catalysts", []))

            st.caption(b1.get("summary", ""))

            with st.expander("Full Bull Data"):
                st.json(b1)

    with col2:
        r1 = get_msg("bear", 1)
        st.markdown("### 🐻 Bear")

        if r1:
            st.markdown("**Thesis**")
            st.write(r1.get("bear_argument"))

            st.markdown("**Key Risks**")
            st.write(r1.get("key_risks", []))

            st.caption(r1.get("summary", ""))

            with st.expander("Full Bear Data"):
                st.json(r1)

    # ROUND 2
    st.subheader("🔁 Round 2 — Rebuttals")

    col3, col4 = st.columns(2)

    with col3:
        b2 = get_msg("bull", 2)
        st.markdown("### 🐂 Bull Rebuttal")

        if b2:
            st.write(b2.get("bull_argument"))
            st.caption(b2.get("summary", ""))

            with st.expander("Full Bull R2"):
                st.json(b2)

    with col4:
        r2 = get_msg("bear", 2)
        st.markdown("### 🐻 Bear Final")

        if r2:
            st.write(r2.get("bear_argument"))
            st.caption(r2.get("summary", ""))

            with st.expander("Full Bear R2"):
                st.json(r2)

    st.divider()

    # ----------------------------
    # 🧠 SIDEBAR DEBUG
    # ----------------------------
    with st.sidebar:
        st.header("🧠 Debug")

        with st.expander("Execution Trace"):
            st.write(completed)

        with st.expander("Full state"):
            st.json(final_state)

        with st.expander("Debate history"):
            st.json(history)

    # ----------------------------
    # 🧠 WHAT THIS SHOWS
    # ----------------------------
    st.header("🧠 What this shows")

    st.markdown("""
- Multi-agent reasoning system  
- Structured bull vs bear debate  
- Decision-making under uncertainty  
- Explainable AI for financial analysis  
""")