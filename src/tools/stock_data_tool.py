import yfinance as yf

def get_stock_data(ticker: str):
    stock = yf.Ticker(ticker)
    df = stock.history(period="6mo")

    return {
        "ticker": ticker,
        "data": df.tail(100)
    }