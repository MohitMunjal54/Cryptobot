import requests
from config import COINGECKO_BASE, TELEGRAM_CHAT_ID
from content.formatter import format_price_post

def daily_prices(bot):
    url = f"{COINGECKO_BASE}/simple/price"
    params = {
        "ids": "bitcoin,ethereum,solana",
        "vs_currencies": "usd,inr",
        "include_24hr_change": "true"
    }

    data = requests.get(url, params=params).json()
    msg = format_price_post(data)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
