# services/quotes_service.py
import requests
import os
from utils.cache import load_cache, save_cache

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def post_quote(bot):
    try:
        cache = load_cache()
        url = "https://api.quotable.io/random"
        data = requests.get(url).json()
        quote_id = data["_id"]

        if quote_id in cache.get("quotes_posted", []):
            return

        msg = f"💡 Quote:\n\"{data['content']}\" — {data['author']}\n\n— ViralCryptoInsights"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

        cache.setdefault("quotes_posted", []).append(quote_id)
        save_cache(cache)

    except Exception as e:
        print("Error in post_quote:", e)
