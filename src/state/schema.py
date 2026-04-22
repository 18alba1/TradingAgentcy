from typing import TypedDict, List, Dict, Any


class DebateMessage(TypedDict):
    speaker: str
    round: int
    content: Dict[str, Any]


class TradingState(TypedDict):
    ticker: str

    technical: Dict[str, Any]
    sentiment: Dict[str, Any]
    news: Dict[str, Any]
    fundamentals: Dict[str, Any]

    bull_argument: Dict[str, Any]
    bear_argument: Dict[str, Any]

    round: int
    debate_history: List[DebateMessage]

    decision: Dict[str, Any]