# services/crypto_service.py
import requests
import os

TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

def post_prices(bot):
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd,inr"
        data = requests.get(url).json()

        btc_usd = data['bitcoin']['usd']
        eth_usd = data['ethereum']['usd']
        sol_usd = data['solana']['usd']

        btc_inr = data['bitcoin']['inr']
        eth_inr = data['ethereum']['inr']
        sol_inr = data['solana']['inr']

        msg = f"☕ Good morning family!\n\n📈 Prices:\nBTC: ${btc_usd} / ₹{btc_inr}\nETH: ${eth_usd} / ₹{eth_inr}\nSOL: ${sol_usd} / ₹{sol_inr}\n\n— ViralCryptoInsights"
        bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=msg)

    except Exception as e:
        print("Error in post_prices:", e)

def post_market_snapshot(bot):
    try:
        url = "https://api.coingecko.com/api/v3/global"
        data = requests.get(url).json()

        btc_dom = data['data']['market_cap_percentage']['btc']
        eth_dom = data['data']['market_cap_percentage']['eth']
        altcap = 100 - btc_dom - eth_dom

        msg = f"📊 Market Snapshot:\nBTC Dominance: {btc_dom:.2f}%\nETH Dominance: {eth_dom:.2f}%\nAltcoins: {altcap:.2f}% of market\n\n— ViralCryptoInsights"
        bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=msg)

    except Exception as e:
        print("Error in post_market_snapshot:", e)
