# services/news_service.py
import feedparser
import requests
from utils.summarizer import summarize_text
from config import TELEGRAM_CHAT_ID
from telegram import Bot

bot = Bot(token="YOUR_TELEGRAM_BOT_TOKEN")  # Use env variable in production

# List of free RSS or JSON sources
NEWS_SOURCES = [
    "https://cryptopanic.com/newsfeed/",            # CryptoPanic RSS
    "https://cointelegraph.com/rss",                # CoinTelegraph RSS
    "https://www.coindesk.com/arc/outboundfeeds/rss/"  # CoinDesk RSS
]

def fetch_news_from_source(url, max_items=5):
    try:
        feed = feedparser.parse(url)
        news_items = []
        for entry in feed.entries[:max_items]:
            title = entry.title
            link = entry.link
            summary_text = entry.summary if hasattr(entry, 'summary') else entry.description
            summary = summarize_text(summary_text, sentences_count=3)
            news_items.append({
                "title": title,
                "link": link,
                "summary": summary
            })
        return news_items
    except Exception as e:
        print(f"Error fetching news from {url}: {e}")
        return []

def fetch_all_news():
    all_news = []
    seen_titles = set()  # Avoid duplicates
    for source in NEWS_SOURCES:
        news_items = fetch_news_from_source(source)
        for news in news_items:
            if news["title"] not in seen_titles:
                seen_titles.add(news["title"])
                all_news.append(news)
    # Sort by latest (if feed has published date)
    return all_news[:10]  # Limit to top 10 combined

def post_news(bot_instance):
    news_items = fetch_all_news()
    for news in news_items:
        message = f"📰 {news['title']}\n{news['summary']}\nRead more: {news['link']}"
        bot_instance.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
