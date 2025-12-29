import feedparser
from config import CRYPTO_NEWS_RSS, TELEGRAM_CHAT_ID

def top_news(bot):
    feed = feedparser.parse(CRYPTO_NEWS_RSS)
    posts = feed.entries[:5]

    text = "📰 Today’s Key Crypto Developments\n\n"
    for i, post in enumerate(posts, 1):
        text += f"{i}. {post.title}\n"

    text += "\nWhy it matters:\nMarket narratives shape capital flow.\n— ViralCryptoInsights"

    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
