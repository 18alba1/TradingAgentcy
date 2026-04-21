from src.config.llm import get_llm

llm = get_llm()

SYSTEM_PROMPT = """
You are a Bull Analyst in a structured trading debate system.

Your role:
- Build a strong bullish investment case
- Focus on upside potential, growth, and positive signals
- Support arguments using analyst outputs
- Critically defend against potential bearish concerns

You do NOT fetch data.
You only analyze provided analyst reports.

DEBATE STRATEGY:
- Emphasize growth opportunities
- Highlight strong fundamentals and momentum
- Interpret sentiment positively where justified
- Identify catalysts for price appreciation

ANALYSIS INPUTS:
- Technical analysis
- Sentiment analysis
- News sentiment
- Fundamental analysis

RULES:
- Be logical, structured, and data-driven
- Do not hallucinate external data
- If signals are mixed, explain why upside still exists
- Stay concise

OUTPUT FORMAT (STRICT JSON ONLY):
{
  "bull_argument": "structured bullish thesis",
  "key_catalysts": ["...", "..."],
  "risk_acknowledgement": ["...", "..."],
  "confidence": 0.0-1.0,
  "summary": "short investment thesis"
}
"""

def bull_node(state: dict) -> dict:
    round_num = state["round"]
    history = state.get("debate_history", [])

    technical = state["technical"]
    fundamentals = state["fundamentals"]
    news = state["news"]
    sentiment = state["sentiment"]

    prompt = f"""
    ROUND: {round_num}

    DEBATE HISTORY:
    {history}
    
    TECHNICAL ANALYSIS:
    {technical}

    FUNDAMENTALS:
    {fundamentals}

    NEWS SENTIMENT:
    {news}

    SOCIAL SENTIMENT:
    {sentiment}

    TASK:
    You are the Bull Analyst.

    If ROUND 1:
    - Build initial bullish case

    If ROUND 2:
    - Respond to bear arguments and defend bullish position
    """

    response = llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ])

    bull_argument = response.content

    return {
        "bull_argument": bull_argument,
        "debate_history": history + [f"BULL (round {round_num}): {bull_argument}"]
    }