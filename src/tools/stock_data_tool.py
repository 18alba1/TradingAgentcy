import finnhub
import pandas as pd
import os
import streamlit as st
from datetime import datetime, timedelta

finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

@st.cache_data(ttl=600)
def get_stock_data(ticker: str):

    end = datetime.utcnow()
    start = end - timedelta(days=180)

    res = finnhub_client.stock_candles(
        ticker,
        "D",
        int(start.timestamp()),
        int(end.timestamp())
    )

    if res.get("s") != "ok":
        raise ValueError(f"No data for {ticker}")

    df = pd.DataFrame({
        "Open": res["o"],
        "High": res["h"],
        "Low": res["l"],
        "Close": res["c"],
        "Volume": res["v"],
    })

    return df