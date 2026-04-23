from src.agents.analyst.fundamental_agent import fundamental_agent

def fundamental_node(state):
    ticker = state["ticker"]

    result = fundamental_agent(ticker)

    return {
        "fundamentals": result
    }