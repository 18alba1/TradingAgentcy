import requests
import time

def get_reddit_sentiment(ticker: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    all_posts = []
    subreddits = ["stocks", "investing", "wallstreetbets"]

    for sub in subreddits:
        try:
            url = f"https://arctic-shift.photon-reddit.com/api/posts/search?subreddit={sub}&title={ticker}&limit=10&sort=desc"
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()

            for post in data.get("data", []):
                all_posts.append({
                    "subreddit": sub,
                    "title": post.get("title", ""),
                    "text": post.get("selftext", "")[:500],
                    "score": post.get("score", 0),
                    "comments": post.get("num_comments", 0)
                })

        except Exception as e:
            continue

        time.sleep(1)

    all_posts = [
        p for p in all_posts
        if p["text"] != "[removed]" and (p["score"] > 5 or p["comments"] > 5)
    ]

    if not all_posts:
        return {
            "ticker": ticker,
            "post_count": 0,
            "posts": [],
            "note": "No relevant posts found. Agent should base sentiment on other available data."
        }

    return {
        "ticker": ticker,
        "post_count": len(all_posts),
        "posts": all_posts
    }