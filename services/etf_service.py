# services/etf_service.py
import os

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def post_etf(bot):
    try:
        # Free sources may not have live data; placeholder
        msg = "🏦 ETF Update:\nBTC ETF inflow: $XXM\nETH ETF inflow: $YYM\nWhy it matters: ETF flows indicate institutional interest.\n\n— ViralCryptoInsights"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
    except Exception as e:
        print("Error in post_etf:", e)
