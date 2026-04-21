from src.agents.analyst.technical_agent import technical_agent

def technical_node(state):
    ticker = state["ticker"]

    result = technical_agent(ticker)

    return {
        "technical": result
    }