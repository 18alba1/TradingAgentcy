import os
import json
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import StructuredTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.tools.news_tool import get_company_news, get_global_news

load_dotenv()
openai_api_key=os.environ.get("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    api_key=openai_api_key
)

SYSTEM_PROMPT = """
You are a financial sentiment analyst in a trading system.

Your job:
- Analyze company news sentiment
- Analyze global market sentiment
- Detect risk, optimism, or uncertainty
- Output structured sentiment insight for a trading system

You MUST use tools to fetch news before making conclusions.

Rules:
- Always retrieve company news first if ticker is given
- Always retrieve global news
- Do not guess without data
- Be concise but accurate

Output format (STRICT JSON):
{
  "company_sentiment": "...",
  "global_sentiment": "...",
  "risk_level": "low | medium | high",
  "summary": "short explanation"
}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

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

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

def sentiment_agent(ticker: str):
    result = agent_executor.invoke({
        "input": f"Analyze sentiment for ticker: {ticker}"
    })

    return json.loads(result["output"])