from newsdataapi import NewsDataApiClient
import streamlit as st
import requests
import requests
from datetime import date, timedelta

newsdata_api_key = st.secrets["NEWSDATA_API_KEY"]
newsdata_client = NewsDataApiClient(apikey=newsdata_api_key)

MARKETAUX_API_KEY = st.secrets["MARKETAUX_API_KEY"]

def get_company_news(ticker):
    current_day = date.today()
    last_week = current_day - timedelta(weeks=1)
    
    url = "https://api.marketaux.com/v1/news/all"
    
    params = {
        "symbols": ticker,
        "filter_entities": "true",
        "published_after": last_week.isoformat(),
        "api_token": MARKETAUX_API_KEY,
        "language": "en"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        news = data.get("data", [])
        
        if not news:
            return []

        # Marketaux results are typically already sorted by date
        combined = [
            f"Headline: {item.get('title', '')}. Summary: {item.get('description', '')}"
            for item in news[:5]
        ]
        return combined
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

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