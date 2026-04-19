"""
Sentiment Agent (FinBERT-based)

Responsible for:
- Company news sentiment
- Global news sentiment

Output:
- structured sentiment score + label
"""

from transformers import pipeline

sentiment_pipeline = pipeline(
    "text-classification",
    model="ProsusAI/finbert",
    return_all_scores=True
)

def _analyze_text(text: str):
    output = sentiment_pipeline(text)

    if isinstance(output, list) and len(output) > 0:

        if isinstance(output[0], list):
            results = output[0]

        elif isinstance(output[0], dict):
            results = output

        else:
            raise ValueError(f"Unexpected output format: {output}")

    else:
        raise ValueError(f"Unexpected pipeline output: {output}")

    best_result = max(results, key=lambda x: x["score"])

    return {
        "label": best_result["label"],
        "score": float(best_result["score"])
    }

def _extract_text(article):
    if isinstance(article, dict):
        return (
            article.get("headline")
            or article.get("title")
            or article.get("description")
            or ""
        )
    return str(article)

def analyze_company_sentiment(news_list):
    scores = []

    for article in news_list:
        text = _extract_text(article)
        res = _analyze_text(text)
        scores.append(res)

    return _aggregate(scores)

def analyze_global_sentiment(news_list):
    scores = []

    for article in news_list:
        text = _extract_text(article)
        res = _analyze_text(text)
        scores.append(res)
    
    return _aggregate(scores)

def _aggregate(results):
    if not results:
        return {"sentiment": "neutral", "confidence": 0.0, "reasoning": "No data"}

    label_score = {"positive": 0.0, "negative": 0.0, "neutral": 0.0}

    for r in results:
        label_score[r["label"]] += r["score"]

    final_label = max(label_score, key=label_score.get)

    confidence = label_score[final_label] / len(results)

    return {
        "sentiment": final_label,
        "confidence": round(confidence, 3),
        "reasoning": f"Aggregated from {len(results)} articles"
    }

from src.data.news_data import get_company_news

news = get_company_news("MSFT")

result = analyze_company_sentiment(news)

print(result)