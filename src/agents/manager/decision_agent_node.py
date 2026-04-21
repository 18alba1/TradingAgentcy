import json
from src.config.llm import get_llm

llm = get_llm()

SYSTEM_PROMPT = """
You are the final decision-maker in a quantitative trading system.

Your job:
- Evaluate all analyst outputs
- Evaluate bull vs bear arguments
- Resolve conflicting signals
- Produce a final trading decision

You do NOT fetch data.
You ONLY use provided analysis.

DECISION RULES:
- BUY: bullish dominance + acceptable risk
- SELL: bearish dominance + strong downside signals
- HOLD: unclear, conflicting, or low-confidence situation

Be conservative when signals conflict.

OUTPUT FORMAT (STRICT JSON ONLY):
{
  "decision": "BUY | SELL | HOLD",
  "confidence": 0.0-1.0,
  "reasoning": "clear explanation referencing key signals",
  "key_factors": ["...", "..."]
}
"""

def decision_agent_node(state):
    prompt = f"""
TECHNICAL ANALYSIS:
{state["technical"]}

SENTIMENT ANALYSIS:
{state["sentiment"]}

NEWS ANALYSIS:
{state["news"]}

FUNDAMENTALS:
{state["fundamentals"]}

DEBATE HISTORY:
{state.get("debate_history", [])}

TASK:
Make final trading decision based on all information above.
"""

    response = llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ])

    result = json.loads(response.content)

    return {"decision": result}