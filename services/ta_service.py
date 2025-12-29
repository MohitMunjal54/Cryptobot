import requests
import json
import random
from telegram import Bot

POSTED_FILE = "ta_posted.json"

COINS = ["bitcoin", "ethereum", "solana", "ripple", "cardano"]
CRYPTO_EMOJI = "📊"

def load_posted():
    try:
        with open(POSTED_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_posted(posted):
    with open(POSTED_FILE, "w") as f:
        json.dump(posted, f)

def fetch_coin_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    try:
        r = requests.get(url, timeout=10).json()
        data = {
            "name": r['name'],
            "symbol": r['symbol'].upper(),
            "current_price_usd": r['market_data']['current_price']['usd'],
            "current_price_inr": r['market_data']['current_price']['inr'],
            "high_24h": r['market_data']['high_24h']['usd'],
            "low_24h": r['market_data']['low_24h']['usd']
        }
        return data
    except Exception as e:
        print("Error fetching coin data:", e)
        return None

def post_ta(bot: Bot):
    posted = load_posted()
    unposted = [coin for coin in COINS if coin not in posted]

    if not unposted:
        posted = []
        unposted = COINS

    coin_id = random.choice(unposted)
    data = fetch_coin_data(coin_id)
    if not data:
        return

    # Build Telegram message
    message = f"{CRYPTO_EMOJI} *TA Series*\n\n"
    message += f"1️⃣ Coin: {data['name']} ({data['symbol']})\n"
    message += f"💵 Price USD: ${data['current_price_usd']}\n"
    message += f"💵 Price INR: ₹{data['current_price_inr']}\n"
    message += f"📈 24h High: ${data['high_24h']}  📉 24h Low: ${data['low_24h']}\n"
    message += f"⚠️ DYOR: This is for educational purposes only!"

    # Post to Telegram
    try:
        bot.send_message(chat_id="@YourTelegramChannel", text=message, parse_mode="Markdown")
    except Exception as e:
        print("Error posting TA Series:", e)

    # Mark as posted
    posted.append(coin_id)
    save_posted(posted)
