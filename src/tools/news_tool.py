import finnhub
from newsdataapi import NewsDataApiClient
from datetime import date, timedelta
import streamlit as st

finnhub_api_key = st.secrets["FINNHUB_API_KEY"]
newsdata_api_key = st.secrets["NEWSDATA_API_KEY"]

finnhub_client = finnhub.Client(api_key=finnhub_api_key)
newsdata_client = NewsDataApiClient(apikey=newsdata_api_key)

def get_company_news(ticker):
    current_day = date.today()
    last_week = current_day - timedelta(weeks=1)

    news = finnhub_client.company_news(
        ticker,
        _from=last_week.isoformat(),
        to=current_day.isoformat()
    )

    if not news:
        return []

    sorted_news = sorted(
        news,
        key=lambda x: x.get("datetime") or 0,
        reverse=True
    )

    return [
        f"Headline: {item.get('headline', '')}. Summary: {item.get('summary', '')}"
        for item in sorted_news[:5]
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