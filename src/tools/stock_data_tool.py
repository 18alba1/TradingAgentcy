import yfinance as yf
import streamlit as st

@st.cache_data(ttl=600) 
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="6mo")
    return df