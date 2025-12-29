import feedparser
import json
import random
from datetime import datetime
from telegram import Bot

# JSON file to track already posted topics
POSTED_FILE = "learning_posted.json"

# RSS feeds from free online learning sources
LEARNING_FEEDS = [
    "https://academy.binance.com/en/feed",          # Binance Academy
    "https://cointelegraph.com/rss/tag/education",  # CoinTelegraph Learn
    "https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml"  # Coindesk Learn
]

CRYPTO_EMOJI = "📘"

def load_posted():
    try:
        with open(POSTED_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_posted(posted):
    with open(POSTED_FILE, "w") as f:
        json.dump(posted, f)

def fetch_learning_articles():
    articles = []
    for feed in LEARNING_FEEDS:
        d = feedparser.parse(feed)
        for entry in d.entries:
            articles.append({
                "title": entry.title,
                "link": entry.link
            })
    return articles

def post_learning(bot: Bot):
    posted = load_posted()
    articles = fetch_learning_articles()

    # Filter unposted
    unposted = [a for a in articles if a['title'] not in posted]
    if not unposted:
        # Reset posted to avoid repetition
        posted = []
        unposted = articles

    article = random.choice(unposted)

    # Telegram-friendly formatting
    message = f"{CRYPTO_EMOJI} *Crypto Learning Series*\n\n"
    message += f"1️⃣ {article['title']}\n"
    message += f"Read & Learn! 🚀"

    # Post on Telegram
    try:
        bot.send_message(chat_id="@YourTelegramChannel", text=message, parse_mode="Markdown")
    except Exception as e:
        print("Error posting Learning Series:", e)

    # Mark as posted
    posted.append(article['title'])
    save_posted(posted)
