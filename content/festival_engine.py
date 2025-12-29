# content/festival_engine.py
import holidays
from datetime import date
from content.formatter import format_festival

IND_HOLIDAYS = holidays.India(years=date.today().year)

def check_festival(bot):
    today = date.today()
    if today in IND_HOLIDAYS:
        festival_name = IND_HOLIDAYS.get(today)
        msg = format_festival(festival_name)
        bot.send_message(chat_id=bot.chat_id, text=msg)
