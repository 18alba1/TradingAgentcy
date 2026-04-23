from src.agents.analyst.sentiment_agent import sentiment_agent

def sentiment_node(state):
    ticker = state["ticker"]

    result = sentiment_agent(ticker)

    return {
        "sentiment": result
    }