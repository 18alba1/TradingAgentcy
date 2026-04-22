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
# UI
# ----------------------------
st.set_page_config(layout="wide")
st.title("🏛️ AI Trading Debate System (DEBUG MODE)")

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
    # DEBUG PANEL
    # ----------------------------
    debug_box = st.empty()
    progress_box = st.progress(0)

    seen_nodes = []   # preserves order (important for debugging)
    total_expected_stages = 7


    # ----------------------------
    # STREAM EXECUTION
    # ----------------------------
    for step in app.stream(state):

        for node, update in step.items():

            # update state
            final_state.update(update)

            # ----------------------------
            # DEBUG OUTPUT (REAL TRUTH)
            # ----------------------------
            seen_nodes.append(node)

            debug_box.markdown(
                f"""
                ### 🔄 Executing Node
                **Current:** `{node}`

                **Full trace so far:**
                {seen_nodes}
                """
            )

            # ----------------------------
            # SAFE PROGRESS (NEVER BREAKS)
            # ----------------------------
            progress_value = min(len(set(seen_nodes)) / total_expected_stages, 1.0)
            progress_box.progress(progress_value)


    st.success("✅ Analysis complete")


    # ----------------------------
    # ANALYST SECTION
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

    st.subheader("📈 Fundamentals")
    st.write(fund.get("summary", "No summary"))


    # ----------------------------
    # DEBATE SECTION (ROBUST ROUND DISPLAY)
    # ----------------------------
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
    st.subheader("🟢 Round 1")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🐂 Bull")
        b1 = get_msg("bull", 1)
        st.write(b1.get("summary") if b1 else "No data")

        with st.expander("Full bull R1"):
            st.json(b1 or {})

    with col2:
        st.markdown("### 🐻 Bear")
        r1 = get_msg("bear", 1)
        st.write(r1.get("summary") if r1 else "No data")

        with st.expander("Full bear R1"):
            st.json(r1 or {})


    # ----------------------------
    # ROUND 2
    # ----------------------------
    st.subheader("🔁 Round 2")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 🐂 Bull Response")
        b2 = get_msg("bull", 2)
        st.write(b2.get("summary") if b2 else "No response")

        with st.expander("Full bull R2"):
            st.json(b2 or {})

    with col4:
        st.markdown("### 🐻 Bear Response")
        r2 = get_msg("bear", 2)
        st.write(r2.get("summary") if r2 else "No response")

        with st.expander("Full bear R2"):
            st.json(r2 or {})


    # ----------------------------
    # FINAL DECISION
    # ----------------------------
    st.header("⚖️ Final Decision")

    dec = safe_json(final_state.get("decision", {}))

    st.subheader(dec.get("decision", "N/A"))
    st.write("Confidence:", dec.get("confidence", 0))
    st.write(dec.get("reasoning", "No reasoning"))

    st.write("Key Factors:")
    st.write(dec.get("key_factors", []))


    # ----------------------------
    # DEBUG SECTION
    # ----------------------------
    st.divider()

    st.subheader("🧠 Execution Trace (Debug)")
    st.write(seen_nodes)

    with st.expander("Full state"):
        st.json(final_state)

    with st.expander("Raw debate history"):
        st.json(history)