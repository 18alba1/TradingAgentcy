from langchain.agents import create_agent
from langchain_core.tools import StructuredTool

import json
from src.tools.stock_data_tool import get_stock_data
from src.config.llm import get_llm

llm = get_llm()

SYSTEM_PROMPT = """
You are a professional technical trading analyst.

Your job:
- Analyze stock price data using technical indicators
- Identify trend, momentum, and key signals
- Use concepts like RSI, MACD, support/resistance

Rules:
- Always fetch stock data first using tools
- Base reasoning ONLY on data provided
- Be precise and quantitative
- Do NOT guess missing values

Output format (STRICT JSON):
{
  "signal": "BUY | SELL | HOLD",
  "confidence": float between 0 and 1,
  "trend": "uptrend | downtrend | sideways",
  "momentum": "bullish | bearish | neutral",
  "rsi": float,
  "macd_signal": "bullish | bearish | neutral",
  "volatility": "low | moderate | high",
  "key_levels": {
    "support": float,
    "resistance": float
  },
  "summary": "short explanation"
}
"""

tools = [
    StructuredTool.from_function(
        func=get_stock_data,
        name="get_stock_data",
        description="Fetch historical stock price data for a ticker"
    )
]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)

def technical_agent(ticker: str):
    result = agent.invoke({
        "messages": [{"role": "user", "content": f"Analyze technical setup for {ticker}"}]
    })
    raw_output = result["messages"][-1].content
    clean = raw_output.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(clean)