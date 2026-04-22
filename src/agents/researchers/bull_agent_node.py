import json
from src.config.llm import get_llm

llm = get_llm()

SYSTEM_PROMPT = """
You are a Bull Analyst in a structured trading debate system.

Your role:
- Build a strong bullish investment case
- Focus on upside potential, growth, and positive catalysts
- Critically respond to bearish arguments when present
- Defend bullish thesis under attack

You only use provided data. No external knowledge.

OUTPUT FORMAT (STRICT JSON ONLY):
{
  "bull_argument": "structured bullish thesis",
  "key_catalysts": ["..."],
  "risk_acknowledgement": ["..."],
  "confidence": 0.0-1.0,
  "summary": "short thesis"
}
"""

def bull_node(state: dict) -> dict:
    history = state.get("debate_history", [])

    technical = state["technical"]
    fundamentals = state["fundamentals"]
    news = state["news"]
    sentiment = state["sentiment"]

    history = state.get("debate_history", [])
    last_message = next(
        (msg for msg in reversed(history)
        if msg["speaker"] != ("bull" if state["turn"].startswith("BULL") else "bear")),
        None
    )   
    
    turn = state.get("turn")

    prompt = f"""
TURN: {turn}

TECHNICAL ANALYSIS:
{json.dumps(technical, indent=2)}

FUNDAMENTALS:
{json.dumps(fundamentals, indent=2)}

NEWS:
{json.dumps(news, indent=2)}

SENTIMENT:
{json.dumps(sentiment, indent=2)}

DEBATE HISTORY:
{json.dumps(history, indent=2)}

RESPONSE TARGET (MOST IMPORTANT):
{json.dumps(last_message, indent=2)}

TASK:
- If BULL_1: build initial bullish case
- If BULL_2: directly respond to RESPONSE TARGET and defend bullish position
"""

    response = llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ])

    try:
        parsed = json.loads(response.content)
    except Exception:
        parsed = {
            "bull_argument": response.content,
            "key_catalysts": [],
            "risk_acknowledgement": [],
            "confidence": 0.5,
            "summary": "parsing error fallback"
        }

    return parsed