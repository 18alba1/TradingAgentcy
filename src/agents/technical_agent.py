'''
Purpose:

analyze price trends
use indicators (SMA, RSI)
output signal (BUY/SELL/HOLD)'''
'''
LLM receives:
- price data
- indicators
- context

LLM outputs:
- reasoning
- signal'''

#MAKE MORE COMPLICATED LATER AND MAYBE AGENTIC
from src.data.stock_data import get_stock_data

def technical_agent(data):
    close = data["periodic_data"]["Close"]

    sma = close.mean()

    if sma < close.iloc[-1]:
        signal = "BUY"
    else: 
        signal = "SELL"
    
    return {
        "signal": signal,
        "sma": sma,
        "reasoning": "Simple SMA strategy"
    }