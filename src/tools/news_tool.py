#import finnhub
from newsdataapi import NewsDataApiClient
#from datetime import date, timedelta
import streamlit as st
import requests

#finnhub_api_key = st.secrets["FINNHUB_API_KEY"]
newsdata_api_key = st.secrets["NEWSDATA_API_KEY"]
API_KEY = st.secrets["FMP_API_KEY"]

#finnhub_client = finnhub.Client(api_key=finnhub_api_key)
newsdata_client = NewsDataApiClient(apikey=newsdata_api_key)


def get_company_news(ticker: str):

    url = f"https://financialmodelingprep.com/api/v3/stock_news"

    params = {
        "tickers": ticker,
        "limit": 10,
        "apikey": API_KEY
    }

    res = requests.get(url, params=params).json()

    if not isinstance(res, list):
        return []

    return [
        f"Headline: {item.get('title','')}. Summary: {item.get('text','')}"
        for item in res[:5]
    ]

def get_global_news():
    response = newsdata_client.news_api(
        q="economy OR inflation OR interest rates OR war OR stock market OR AI",
        language="en",
        category="business,politics"
    )

    articles = response.get("results", [])

    return [
        f"Title: {a.get('title', '')} | Description: {a.get('description', '')}"
        for a in articles[:5]
    ]