# community/greetings.py
from content.formatter import format_price_post
from services.market_service import daily_prices

def good_morning(bot):
    daily_prices(bot)  # Morning prices + greetings

def good_night(bot):
    msg = "🌙 Good Night Family!\n\nReflect on today, plan tomorrow, and stay disciplined.\n— ViralCryptoInsights"
    bot.send_message(chat_id=bot.chat_id, text=msg)
