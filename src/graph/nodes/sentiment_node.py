from src.agents.analyst.sentiment_agent import sentiment_agent

def technical_node(state):
    ticker = state["ticker"]

    result = sentiment_agent(ticker)

    return {
        "technical": result
    }