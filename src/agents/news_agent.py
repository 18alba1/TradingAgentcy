from langchain.agents import create_agent
from langchain_core.tools import StructuredTool

import json
from src.tools.news_tool import get_company_news, get_global_news
from src.config.llm import get_llm

llm = get_llm()

SYSTEM_PROMPT = """
You are a financial news analyst in a trading system.

Your job:
- Analyze company-specific news sentiment
- Analyze global macroeconomic news sentiment
- Detect risk factors, optimism, or uncertainty in the news
- Identify key events or drivers moving the market

You MUST use tools to fetch news before making conclusions.

Rules:
- Always retrieve company news first if ticker is given
- Always retrieve global news
- Do not guess without data
- Be concise and objective — report what the news says, not what to trade
- If no relevant news is found, reflect that in a low confidence score

Output format (STRICT JSON, no markdown, no backticks):
{
  "company_sentiment": "positive | neutral | negative",
  "company_score": 0-1,
  "global_sentiment": "positive | neutral | negative | mixed",
  "global_score": 0-1,
  "risk_level": "low | medium | high",
  "confidence": 0-1,
  "key_drivers": ["...", "..."],
  "summary": "short explanation of what the news says"
}
"""

tools = [
    StructuredTool.from_function(
        func=get_company_news,
        name="get_company_news",
        description="Fetch latest company-specific financial news using ticker symbol."
    ),
    StructuredTool.from_function(
        func=get_global_news,
        name="get_global_news",
        description="Fetch latest global macroeconomic and market news."
    )
]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)

def news_agent(ticker: str):
    result = agent.invoke({
        "messages": [{"role": "user", "content": f"Analyze news sentiment for ticker: {ticker}"}]
    })
    raw_output = result["messages"][-1].content
    clean = raw_output.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(clean)