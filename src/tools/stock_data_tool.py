import yfinance as yf
import streamlit as st

@st.cache_data(ttl=300)  # cache for 5 minutes
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="6mo")
    return df