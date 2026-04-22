from langgraph.graph import StateGraph, START, END
from src.state.schema import TradingState

from src.agents.analyst.technical_agent import technical_agent
from src.agents.analyst.sentiment_agent import sentiment_agent
from src.agents.analyst.news_agent import news_agent
from src.agents.analyst.fundamental_agent import fundamental_agent

from src.agents.researchers.bull_agent_node import bull_node
from src.agents.researchers.bear_agent_node import bear_node
from src.agents.manager.decision_agent_node import decision_agent_node

def technical_node(state: TradingState):
    result = technical_agent(state["ticker"])
    return {"technical": result}

def news_node(state: TradingState):
    result = news_agent(state["ticker"])
    return {"news": result}

def sentiment_node(state: TradingState):
    result = sentiment_agent(state["ticker"])
    return {"sentiment": result}

def fundamental_node(state: TradingState):
    result = fundamental_agent(state["ticker"])
    return {"fundamentals": result}

def bull_wrapper(state: TradingState):
    result = bull_node(state)

    if state["turn"] == "BULL_1":
        next_turn = "BEAR_1"
    else:
        next_turn = state["turn"]

    return {
        "bull_argument": result,
        "debate_history": state["debate_history"] + [{
            "speaker": "bull",
            "content": result
        }],
        "turn": next_turn
    }

def bear_wrapper(state: TradingState):
    result = bear_node(state)

    if state["turn"] == "BEAR_1":
        next_turn = "BULL_2"
    else:
        next_turn = "BEAR_2"

    return {
        "bear_argument": result,
        "debate_history": state["debate_history"] + [{
            "speaker": "bear",
            "content": result
        }],
        "turn": next_turn
    }

def route_after_bear(state: TradingState):
    if state["turn"] == "BEAR_1":
        return "bull"
    return "decision"

def decision_node(state):
    result = decision_agent_node(state)
    return result

    return {"decision": result}

def build_graph():
    graph = StateGraph(TradingState)

    graph.add_node("technical", technical_node)
    graph.add_node("sentiment", sentiment_node)
    graph.add_node("news", news_node)
    graph.add_node("fundamentals", fundamental_node)

    graph.add_node("bull", bull_wrapper)
    graph.add_node("bear", bear_wrapper)

    graph.add_node("decision", decision_node)

    graph.add_edge(START, "technical")
    graph.add_edge(START, "fundamentals")
    graph.add_edge(START, "news")
    graph.add_edge(START, "sentiment")

    graph.add_edge(["technical", "fundamentals", "news", "sentiment"], "bull")

    graph.add_edge("bull", "bear")

    graph.add_conditional_edges(
        "bear",
        route_after_bear,
        {
            "bull": "bull",
            "decision": "decision"
        }
    )

    graph.add_edge("decision", END)

    return graph.compile()