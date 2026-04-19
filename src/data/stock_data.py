'''Responsible for:

fetching stock prices (yfinance)
returning clean structured data

Output:

last price
historical dataframe
maybe indicators later'''
import yfinance as yf

def get_stock_data(ticker, period="3mo"):
    stock_data = yf.Ticker(ticker)
    stock_price_history = stock_data.history(period=period)

    return {
        "last_price": stock_price_history["Close"].iloc[-1],
        "periodic_data": stock_price_history.tail(20)
    }

