from langchain.agents import create_agent
from langchain_core.tools import StructuredTool

import json
from src.config.llm import get_llm
from src.tools.sentiment_tool import get_reddit_sentiment

llm = get_llm()

SYSTEM_PROMPT = """You are a social sentiment analyst.

Your job:
- Analyze retail investor sentiment from Reddit posts
- Detect hype, fear, uncertainty, or strong conviction
- Identify if sentiment is driven by fundamentals or speculation

Rules:
- Always use tools to fetch social data first
- Do not hallucinate or guess without data
- Be critical of hype and exaggerated claims
- If no data is available, return neutral sentiment with confidence 0

Output format (STRICT JSON, no markdown, no backticks):
{
  "sentiment": "bullish | bearish | neutral",
  "confidence": 0-1,
  "hype_driven": true | false,
  "risk": "low | medium | high",
  "insight": "what retail investors believe and why"
}"""

tools = [
    StructuredTool.from_function(
        func=get_reddit_sentiment,
        name="get_reddit_sentiment",
        description="Search Reddit posts about a stock ticker across r/stocks, r/investing, and r/wallstreetbets. Returns post titles, text, scores, and comment counts to assess retail investor sentiment."
    )
]

agent = create_agent(model=llm, tools=tools, system_prompt=SYSTEM_PROMPT)

def sentiment_agent(ticker: str):
    result = agent.invoke({
        "messages": [{"role": "user", "content": f"Analyze social media sentiment for ticker: {ticker}"}]
    })
    raw_output = result["messages"][-1].content
    clean = raw_output.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(clean)