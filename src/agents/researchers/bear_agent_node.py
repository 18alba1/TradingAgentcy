from src.config.llm import get_llm

llm = get_llm()

SYSTEM_PROMPT = """
You are a Bear Analyst in a structured trading debate system.

Your role:
- Build a strong bearish investment case
- Focus on downside risk, valuation concerns, and failure scenarios
- Critically challenge the bullish argument using provided analyst outputs
- Protect the system from over-optimistic decision making

You do NOT fetch data.
You only analyze provided analyst reports.

DEBATE STRATEGY:
- Emphasize risks, uncertainty, and downside catalysts
- Identify weaknesses in fundamentals and valuation
- Interpret sentiment cautiously or negatively when justified
- Challenge bullish assumptions directly with evidence from inputs

ANALYSIS INPUTS:
- Technical analysis
- Sentiment analysis
- News sentiment
- Fundamental analysis
- Bull argument (VERY IMPORTANT)

RULES:
- Be logical, structured, and data-driven
- Do not hallucinate external data
- If signals are mixed, explain why downside risk dominates or remains significant
- Directly respond to and critique the bull argument
- Stay concise but equally detailed as bull output

OUTPUT FORMAT (STRICT JSON ONLY):
{
  "bear_argument": "structured bearish thesis",
  "key_risks": ["...", "..."],
  "counter_to_bull": ["...", "..."],
  "risk_drivers": ["...", "..."],
  "confidence": 0.0-1.0,
  "summary": "short risk-focused investment thesis"
}
"""

def bear_node(state: dict) -> dict:
    round_num = state["round"]
    history = state.get("debate_history", [])

    bull_argument = state["bull_argument"]
    
    technical = state["technical"]
    sentiment = state["sentiment"]
    news = state["news"]
    fundamentals = state["fundamentals"]

    prompt = f"""
    ROUND: {round_num}

    DEBATE HISTORY:
    {history}
    
    LAST BULL ARGUMENT:
    {bull_argument}

    TECHNICAL ANALYSIS:
    {technical}

    FUNDAMENTALS:
    {fundamentals}

    NEWS SENTIMENT:
    {news}

    SOCIAL SENTIMENT:
    {sentiment}

    TASK:
    You are the Bear Analyst.

    If ROUND 1:
    - Build initial bearish case

    If ROUND 2:
    - Criticize bull AND respond to its rebuttal
    """ 

    response = llm.invoke((
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ))

    bear_argument = response.content

    return {
        "bear_argument": bear_argument,
        "debate_history": history + [f"BEAR (round {round_num}): {bear_argument}"]
    }