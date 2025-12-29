# services/news_service.py

import requests
import feedparser
import random
from config import TELEGRAM_CHANNEL_ID

# Free RSS / news sources
NEWS_SOURCES = [
    "https://cointelegraph.com/rss",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cryptopanic.com/newsfeed/"
]

# Random calm insight lines
INSIGHT_LINES = [
    "Market reaction remains measured.",
    "Traders remain cautious amid mixed signals.",
    "Price action shows stability with subtle shifts.",
    "Liquidity remains moderate, not aggressive.",
    "Participants watching broader macro context."
]

# Fetch headlines
def fetch_headlines():
    headlines = []
    for url in NEWS_SOURCES:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:  # top 3 from each
                title = entry.title.strip()
                if title and title not in headlines:
                    headlines.append(title)
        except Exception:
            continue
    return headlines

# Send news to Telegram
def post_news(bot):
    headlines = fetch_headlines()
    if not headlines:
        headlines = ["Market data available, headlines not found."]

    message = "📰 *Crypto Pulse – News Update*\n\n"
    for idx, headline in enumerate(headlines[:5], start=1):
        message += f"{idx}️⃣ {headline}\n"

    insight = random.choice(INSIGHT_LINES)
    message += f"\n{insight}\n\n— ViralCryptoInsights"

    bot.send_message(
        chat_id=TELEGRAM_CHANNEL_ID,
        text=message,
        parse_mode="Markdown"
    )
