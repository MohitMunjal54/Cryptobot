# services/learning_service.py
import requests
import feedparser
import random
import os
from utils.cache import load_cache, save_cache

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Example curated TA & learning feeds (free RSS)
LEARNING_FEEDS = [
    "https://www.investopedia.com/feedbuilder/feed/getrssfeed/?feedName=bitcoin",
    "https://academy.binance.com/en/feed/rss",
    "https://cointelegraph.com/rss/tag/technical-analysis"
]

def fetch_learning_content():
    """Fetch latest articles or tips from free RSS feeds"""
    articles = []
    for feed_url in LEARNING_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:  # top 5 latest
            title = entry.title
            summary = getattr(entry, "summary", "")
            content = f"{title}\n{summary}"
            articles.append(content)
    return articles

def post_learning(bot):
    """Post one learning / TA tip per run"""
    try:
        cache = load_cache()
        posted = cache.get("learning_posted", [])

        articles = fetch_learning_content()
        random.shuffle(articles)  # randomize for variety

        for article in articles:
            if article in posted:
                continue
            msg = f"📚 Learning / TA Series:\n{article}\n\n— ViralCryptoInsights"
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

            # Save to cache
            posted.append(article)
            cache["learning_posted"] = posted
            save_cache(cache)
            break  # Post only one per run

    except Exception as e:
        print("Error in post_learning:", e)
