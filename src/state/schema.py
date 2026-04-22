from typing import TypedDict, List, Dict, Literal, Any

class TradingState(TypedDict):
    ticker: str

    technical: Dict[str, Any]
    sentiment: Dict[str, Any]
    news: Dict[str, Any]
    fundamentals: Dict[str, Any]

    bull_argument: Dict[str, Any]
    bear_argument: Dict[str, Any]
    
    turn: Literal["BULL_1", "BEAR_1", "BULL_2", "BEAR_2"]
    debate_history: List[Dict[str, Any]]

    decision: Dict[str, Any]