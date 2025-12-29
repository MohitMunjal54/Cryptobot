# services/news_service.py
from config import TELEGRAM_CHAT_ID
from utils.summarizer import smart_summarize, analyst_wrap
import feedparser

RSS_FEEDS = [
    "https://cryptopanic.com/news.rss",
    "https://www.coindesk.com/arc/outboundfeeds/rss/"
]

def post_news(bot):
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:1]:  # Only top 1 article
            title = entry.title
            link = entry.link
            content = entry.get("summary", title)
            summary = smart_summarize(content, sentences_count=2)
            if not summary:
                continue
            msg = f"📰 {title}\n\n{analyst_wrap(summary)}\nRead more: {link}\n— ViralCryptoInsights"
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
            break  # Post only 1 article per feed
