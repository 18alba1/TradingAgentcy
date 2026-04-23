import streamlit as st
from finnhub import Client

# assume you set this in st.secrets or env
FINNHUB_API_KEY = st.secrets["FINNHUB_API_KEY"]
client = Client(api_key=FINNHUB_API_KEY)


@st.cache_data(ttl=3600)
def get_fundamentals(ticker: str) -> dict:
    # Finnhub endpoints
    profile = client.company_profile2(symbol=ticker)
    metrics = client.company_basic_financials(ticker, "all")
    quote = client.quote(ticker)

    metric_data = metrics.get("metric", {})

    return {
        "ticker": ticker,

        # valuation
        "pe_ratio": metric_data.get("peBasicExclExtraTTM"),
        "forward_pe": metric_data.get("peInclExtraTTM"),

        # profitability
        "eps": metric_data.get("epsTTM"),
        "profit_margin": metric_data.get("netProfitMarginTTM"),
        "return_on_equity": metric_data.get("roeTTM"),

        # growth
        "revenue_growth": metric_data.get("revenueGrowthTTMYoy"),
        "earnings_growth": metric_data.get("epsGrowthTTMYoy"),

        # financial health
        "debt_to_equity": metric_data.get("totalDebt/totalEquityAnnual"),
        "free_cashflow": metric_data.get("freeCashFlowTTM"),

        # valuation context
        "market_cap": metric_data.get("marketCapitalization"),
        "52w_high": quote.get("h"),
        "52w_low": quote.get("l"),

        # analyst
        "analyst_target": metric_data.get("targetPrice"),
        "recommendation": metric_data.get("recommendationKey"),

        # extra useful context
        "name": profile.get("name"),
        "country": profile.get("country"),
        "industry": profile.get("finnhubIndustry"),
    }