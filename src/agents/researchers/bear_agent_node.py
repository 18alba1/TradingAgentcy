import json
from src.config.llm import get_llm

llm = get_llm()

SYSTEM_PROMPT = """
You are a Bear Analyst in a structured trading debate system.

Your role:
- Build a strong bearish investment case
- Focus on downside risk, valuation concerns, and failure scenarios
- Critically respond to bullish arguments
- Challenge assumptions directly using provided data

You only use provided data. No external knowledge.

OUTPUT FORMAT (STRICT JSON ONLY):
{
  "bear_argument": "structured bearish thesis",
  "key_risks": ["..."],
  "counter_to_bull": ["..."],
  "risk_drivers": ["..."],
  "confidence": 0.0-1.0,
  "summary": "short bearish thesis"
}
"""

def bear_node(state: dict) -> dict:
    history = state.get("debate_history", [])
    round_num = state.get("round", 1)

    last_opponent = next(
        (m for m in reversed(history) if m["speaker"] == "bull"),
        None
    )

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

OPPONENT LAST MESSAGE:
{json.dumps(last_opponent, indent=2)}

TASK:
- If BEAR_1: build initial bearish case
- If BEAR_2: directly respond to opponent and refute their claims

CRITICAL INSTRUCTION:
You MUST directly attack specific claims from OPPONENT LAST MESSAGE.
Quote or reference at least 2 concrete points and refute them.
Do NOT restate your previous argument.
If you repeat yourself, your response is invalid.
"""

    response = llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ])

    result = json.loads(response.content)

    history.append({
        "speaker": "bear",
        "round": round_num,
        "content": result
    })

    return {
        "bear_argument": result,
        "debate_history": history,
        "round": round_num + 1
    }