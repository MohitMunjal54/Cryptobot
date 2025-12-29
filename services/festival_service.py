# services/festival_service.py
import holidays
import datetime
import os

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

indian_holidays = holidays.India()

def post_festival_greeting(bot):
    today = datetime.date.today()
    if today in indian_holidays:
        festival_name = indian_holidays.get(today)
        msg = f"🎉 Happy {festival_name}!\nWishing you joy and peace.\n\n— ViralCryptoInsights"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
