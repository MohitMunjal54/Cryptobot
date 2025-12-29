# services/events_service.py
import feedparser
import os
from utils.cache import load_cache, save_cache

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def post_crypto_and_macro_events(bot):
    try:
        cache = load_cache()
        url = "https://www.forexfactory.com/ffcal_week_this.xml"  # Free economic calendar
        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:
            event_id = entry.id if 'id' in entry else entry.link
            if event_id in cache.get("events_ids", []):
                continue

            msg = f"🌍 Event Alert:\n{entry.title}\nTime: {entry.published}\n\n— ViralCryptoInsights"
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

            cache.setdefault("events_ids", []).append(event_id)

        save_cache(cache)

    except Exception as e:
        print("Error in post_crypto_and_macro_events:", e)
