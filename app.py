import streamlit as st
import json
from src.graph.workflow import build_graph

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

### ⚔️ Debate System
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

            # ----------------------------
            # STEP UI
            # ----------------------------
            step_ui = "### ⚙️ Execution Status\n"

            for i, (step_key, label) in enumerate(STEPS):
                if i < len(completed):
                    step_ui += f"✅ {label}\n"
                elif step_key == current:
                    step_ui += f"⏳ **{label} (running...)**\n"
                else:
                    step_ui += f"⬜ {label}\n"

            step_box.markdown(step_ui)

            # ----------------------------
            # PROGRESS BAR
            # ----------------------------
            progress_value = min(len(completed) / len(STEPS), 1.0)
            progress_bar.progress(progress_value)

    st.success("✅ Analysis complete")


    # ----------------------------
    # ANALYST RESULTS
    # ----------------------------
    st.header("📊 Market Analysis")

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


    # ==========================================================
    # 🔥 NEW DEBATE SECTION (FULL ARGUMENTS)
    # ==========================================================
    st.header("⚔️ Debate System")

    history = final_state.get("debate_history", [])

    def get_msg(role, round_num):
        for msg in history:
            if msg.get("speaker") == role and msg.get("round") == round_num:
                return msg.get("content")
        return None


    # ----------------------------
    # ROUND 1
    # ----------------------------
    st.subheader("🟢 Round 1 — Initial Positions")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🐂 Bull Case")

        b1 = get_msg("bull", 1)

        if b1:
            st.write(b1.get("bull_argument", "No argument"))
            st.caption(f"Summary: {b1.get('summary', '')}")

            with st.expander("📜 Full Bull Data"):
                st.json(b1)
        else:
            st.write("No data")

    with col2:
        st.markdown("### 🐻 Bear Case")

        r1 = get_msg("bear", 1)

        if r1:
            st.write(r1.get("bear_argument", "No argument"))
            st.caption(f"Summary: {r1.get('summary', '')}")

            with st.expander("📜 Full Bear Data"):
                st.json(r1)
        else:
            st.write("No data")


    # ----------------------------
    # ROUND 2
    # ----------------------------
    st.subheader("🔁 Round 2 — Rebuttals")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 🐂 Bull Rebuttal")

        b2 = get_msg("bull", 2)

        if b2:
            st.write(b2.get("bull_argument", "No rebuttal"))
            st.caption(f"Summary: {b2.get('summary', '')}")

            with st.expander("📜 Full Bull R2 Data"):
                st.json(b2)
        else:
            st.write("No response")

    with col4:
        st.markdown("### 🐻 Bear Final Response")

        r2 = get_msg("bear", 2)

        if r2:
            st.write(r2.get("bear_argument", "No rebuttal"))
            st.caption(f"Summary: {r2.get('summary', '')}")

            with st.expander("📜 Full Bear R2 Data"):
                st.json(r2)
        else:
            st.write("No response")


    # ----------------------------
    # FINAL DECISION
    # ----------------------------
    st.header("⚖️ Final Decision")

    dec = safe_json(final_state.get("decision", {}))

    st.subheader(dec.get("decision", "N/A"))
    st.write("Confidence:", dec.get("confidence", 0))
    st.write(dec.get("reasoning", "No reasoning"))

    st.write("### Key Factors")
    st.write(dec.get("key_factors", []))


    # ----------------------------
    # DEBUG
    # ----------------------------
    with st.expander("🧠 Execution Trace"):
        st.write(completed)

    with st.expander("Full state"):
        st.json(final_state)

    with st.expander("Raw debate history"):
        st.json(history)