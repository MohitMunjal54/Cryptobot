# services/news_service.py
import feedparser
from gensim.summarization import summarize
import os
from utils.cache import load_cache, save_cache

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Free RSS news feeds
NEWS_FEEDS = [
    "https://cryptopanic.com/feed/cryptopanic.rss",
    "https://cointelegraph.com/rss",
    "https://academy.binance.com/en/feed/rss"
]

def fetch_news_articles():
    """Fetch latest news articles from RSS feeds"""
    articles = []
    for feed_url in NEWS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:  # top 5 latest
            content = getattr(entry, "summary", "") or entry.title
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "content": content
            })
    return articles

def summarize_text(text):
    """Summarize text using gensim (50 words)"""
    try:
        return summarize(text, word_count=50)
    except:
        return text  # fallback if summarization fails

def post_news(bot):
    """Post top 1 latest news in a friendly, human-like style"""
    try:
        cache = load_cache()
        posted_links = cache.get("news_posted", [])

        articles = fetch_news_articles()
        for article in articles:
            if article["link"] in posted_links:
                continue

            summary = summarize_text(article["content"])
            msg = (
                f"📰 Crypto News:\n"
                f"{article['title']}\n"
                f"{summary}\n"
                f"Read more: {article['link']}\n\n"
                f"— ViralCryptoInsights"
            )

            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

            # Save posted link to cache
            posted_links.append(article["link"])
            cache["news_posted"] = posted_links
            save_cache(cache)
            break  # Post only one news per scheduler run

    except Exception as e:
        print("Error in post_news:", e)
