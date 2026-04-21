from typing import TypedDict, List, Dict, Any

class TradingState(TypedDict):
    ticker: str

    technical: Dict[str, Any]
    sentiment: Dict[str, Any]
    news: Dict[str, Any]
    fundamentals: Dict[str, Any]

    bull_argument: Dict[str, Any]
    bear_argument: Dict[str, Any]
    
    round: int
    debate_history: List[str]

    decision: Dict[str, Any]