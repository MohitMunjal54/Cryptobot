# services/whale_service.py
import requests
import os
from utils.cache import load_cache, save_cache

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def post_whale_alerts(bot):
    try:
        cache = load_cache("whale_alerts", default=[]) 
        url = "https://api.whale-alert.io/v1/transactions?api_key=demo&min_value=500000&currency=btc"  # free demo API
        data = requests.get(url).json()

        for tx in data.get("transactions", []):
            tx_id = tx["id"]
            if tx_id in cache.get("whale_tx", []):
                continue

            msg = f"🐋 Whale Alert:\n{tx['symbol']} transfer of ${tx['amount_usd']}\nFrom: {tx['from']['owner_type']}\nTo: {tx['to']['owner_type']}\n\n— ViralCryptoInsights"
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

            cache.setdefault("whale_tx", []).append(tx_id)

        save_cache(cache)

    except Exception as e:
        print("Error in post_whale_alerts:", e)
