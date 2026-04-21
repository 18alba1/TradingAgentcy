from src.agents.analyst.fundamental_agent import fundamental_agent

def technical_node(state):
    ticker = state["ticker"]

    result = fundamental_agent(ticker)

    return {
        "technical": result
    }