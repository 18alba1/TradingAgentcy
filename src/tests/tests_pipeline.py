from tools.stock_data_tool import get_stock_data
from src.data.news_data import get_company_news, get_global_news

from src.agents.technical_agent import technical_agent
from src.agents.sentiment_agent import (
    analyze_company_sentiment,
    analyze_global_sentiment
)
from src.agents.decision_agent import decision_agent


ticker = "MSFT"

# 1. Get data
stock_data = get_stock_data(ticker)

# 2. Technical analysis
technical = technical_agent(stock_data)

# 3. Sentiment
company_news = get_company_news(ticker)
company_sentiment = analyze_company_sentiment(company_news)

global_news = get_global_news()
global_sentiment = analyze_global_sentiment(global_news)

# 4. Decision
decision = decision_agent(
    technical,
    company_sentiment,
    global_sentiment,
    price=stock_data["last_price"]
)

print(decision)