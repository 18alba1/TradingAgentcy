import streamlit as st
import os
import json
from dotenv import load_dotenv

# 1. LADDA DOTENV DET FÖRSTA VI GÖR
# Detta ser till att alla efterföljande importer kan läsa API-nyckeln
load_dotenv()

# Kontrollera API-nyckeln direkt
if not os.getenv("OPENAI_API_KEY"):
    st.error("🚨 API-nyckel saknas! Se till att du har en .env-fil med OPENAI_API_KEY i projektets rotmapp.")
    st.stop()

# 2. IMPORTERA DINA GRAF-MODULER
# Dessa importeras efter load_dotenv så att de får tillgång till miljön
try:
    from src.graph.workflow import build_graph
except ImportError as e:
    st.error(f"❌ Kunde inte importera graf-modulen. Kontrollera dina sökvägar. Fel: {e}")
    st.stop()

# --- SIDSINSTÄLLNINGAR ---
st.set_page_config(page_title="AI Trading Agency", layout="wide", page_icon="📈")

st.title("📈 AI Trading Agency: Multi-Agent Analysis")
st.markdown("Detta system orkestrerar agenter för teknisk, fundamental och sentiment-analys.")

# --- SIDEBAR FÖR INPUT ---
with st.sidebar:
    st.header("Inställningar")
    ticker = st.text_input("Aktieticker (t.ex. NVDA, TSLA, MSFT)", value="AAPL").upper()
    
    st.info("""
    **Arbetsflöde:**
    1. Analytiker körs parallellt.
    2. Bull/Bear-researchers debatterar.
    3. Manager tar ett beslut.
    """)
    
    run_button = st.button("🚀 Starta Analys", use_container_width=True)

# --- HUVUDFÖNSTER ---
if run_button:
    # Initialisera grafen
    with st.spinner("Initierar agenter..."):
        app = build_graph()
    
    # Skapa det initiala tillståndet (måste matcha din TradingState)
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

    # Logg för att se vad som händer i realtid
    st.subheader("Processlogg")
    log_placeholder = st.empty()
    status_log = []

    # Kör grafen med streaming
    # Vi skapar en kopia av state för att lagra resultaten lokalt i appen
    current_state = initial_state.copy()

    try:
        for output in app.stream(initial_state):
            for node_name, state_update in output.items():
                # Uppdatera loggen i UI
                status_log.append(f"✅ Nod **{node_name}** klar.")
                log_placeholder.markdown("\n".join(status_log))
                
                # Uppdatera vårt lokala state med datan från noden
                current_state.update(state_update)

        st.success("Analys genomförd!")

        # --- VISA RESULTAT I TABS ---
        tabs = st.tabs(["📊 Analytiker", "🗣️ Debatt", "🎯 Slutgiltigt Beslut"])

        with tabs[0]:
            st.subheader("Data från Analyst Team")
            c1, c2 = st.columns(2)
            with c1:
                st.write("### Teknisk Analys")
                st.json(current_state.get("technical", {}))
                st.write("### Fundamental Analys")
                st.json(current_state.get("fundamentals", {}))
            with c2:
                st.write("### Sentiment & Nyheter")
                st.json(current_state.get("sentiment", {}))
                st.json(current_state.get("news", {}))

        with tabs[1]:
            st.subheader("Researcher Team: Debatt")
            
            st.markdown("#### 🐂 Bull Argument")
            st.info(current_state.get("bull_argument", "Ingen data."))
            
            st.markdown("#### 🐻 Bear Argument")
            st.warning(current_state.get("bear_argument", "Ingen data."))
            
            with st.expander("Visa debatthistorik"):
                for entry in current_state.get("debate_history", []):
                    st.write(entry)

        with tabs[2]:
            st.subheader("Manager: Beslutsunderlag")
            decision = current_state.get("decision", {})
            if decision:
                st.metric("Beslut", str(decision.get('action', 'N/A')).upper())
                st.write(f"**Sannolikhet/Confidence:** {decision.get('confidence', 'N/A')}")
                st.write(f"**Motivering:** {decision.get('reasoning', 'N/A')}")
            else:
                st.error("Inget beslut kunde fattas.")

    except Exception as e:
        st.error(f"Ett fel uppstod under körningen: {e}")
        st.exception(e)

else:
    st.info("Skriv in en ticker i sidomenyn och klicka på 'Starta Analys' för att börja.")