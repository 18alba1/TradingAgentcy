import requests
import pandas as pd
import streamlit as st

API_KEY = st.secrets["TWELVEDATA_API_KEY"]

@st.cache_data(ttl=600)
def get_stock_data(ticker: str):

    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": ticker,
        "interval": "1day",
        "outputsize": 180,
        "apikey": API_KEY
    }

    res = requests.get(url, params=params).json()

    if "values" not in res:
        raise ValueError(res)

    df = pd.DataFrame(res["values"])
    df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": float})
    df = df.iloc[::-1] 
    df.rename(columns={"close": "Close"}, inplace=True)

    return df