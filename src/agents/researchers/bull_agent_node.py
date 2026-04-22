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
    round_num = state.get("round", 1)

    last_opponent = next(
        (m for m in reversed(history) if m["speaker"] == "bear"),
        None
    )

    prompt = f"""
ROUND: {round_num}

TECHNICAL:
{json.dumps(state["technical"], indent=2)}

FUNDAMENTALS:
{json.dumps(state["fundamentals"], indent=2)}

NEWS:
{json.dumps(state["news"], indent=2)}

SENTIMENT:
{json.dumps(state["sentiment"], indent=2)}

OPPONENT LAST MESSAGE:
{json.dumps(last_opponent, indent=2)}

TASK:
- If ROUND 1: Build a strong bullish investment case
- If ROUND 2: Directly respond to the opponent and defend your position

CRITICAL INSTRUCTION:
You MUST directly attack specific claims from OPPONENT LAST MESSAGE.
- Quote or reference at least 2 concrete points from the opponent
- Explain why those points are incorrect, overstated, or misinterpreted
- Support your rebuttal using the provided data (technical, fundamentals, sentiment, news)
- Do NOT restate your previous argument
- Do NOT ignore the opponent’s claims

RESPONSE STRUCTURE:
For rebuttals, follow this structure:
1. Opponent claim
2. Why it is flawed
3. Evidence from data
4. Bullish interpretation

If no opponent message exists:
- Build a clear bullish thesis using:
  - growth drivers
  - valuation upside
  - sentiment tailwinds
  - catalysts

OUTPUT FORMAT (STRICT JSON ONLY):
{{
  "bull_argument": "structured bullish thesis or rebuttal",
  "key_catalysts": ["...", "..."],
  "risk_acknowledgement": ["...", "..."],
  "confidence": 0.0-1.0,
  "summary": "short investment thesis"
}}
"""

    response = llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ])

    result = json.loads(response.content)

    history.append({
        "speaker": "bull",
        "round": round_num,
        "content": result
    })

    return {
        "bull_argument": result,
        "debate_history": history,
        "round": round_num + 1
    }