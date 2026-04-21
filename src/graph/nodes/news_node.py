from src.agents.analyst.news_agent import news_agent

def technical_node(state):
    ticker = state["ticker"]

    result = news_agent(ticker)

    return {
        "technical": result
    }