from finnhub import Client
import streamlit as st

FINNHUB_API_KEY = st.secrets["FINNHUB_API_KEY"]
client = Client(api_key=FINNHUB_API_KEY)

def get_fundamentals(ticker: str) -> dict:
    profile = client.company_profile2(symbol=ticker)
    metrics = client.company_basic_financials(ticker, "all")
    quote = client.quote(ticker)

    metric_data = metrics.get("metric", {})

    return {
        "ticker": ticker,

        "pe_ratio": metric_data.get("peBasicExclExtraTTM"),
        "forward_pe": metric_data.get("peInclExtraTTM"),

        "eps": metric_data.get("epsTTM"),
        "profit_margin": metric_data.get("netProfitMarginTTM"),
        "return_on_equity": metric_data.get("roeTTM"),

        "revenue_growth": metric_data.get("revenueGrowthTTMYoy"),
        "earnings_growth": metric_data.get("epsGrowthTTMYoy"),

        "debt_to_equity": metric_data.get("totalDebt/totalEquityAnnual"),
        "free_cashflow": metric_data.get("freeCashFlowTTM"),

        "market_cap": metric_data.get("marketCapitalization"),
        "52w_high": quote.get("h"),
        "52w_low": quote.get("l"),

        "analyst_target": metric_data.get("targetPrice"),
        "recommendation": metric_data.get("recommendationKey"),

        "name": profile.get("name"),
        "country": profile.get("country"),
        "industry": profile.get("finnhubIndustry"),
    }