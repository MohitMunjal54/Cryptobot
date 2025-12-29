# content/quotes_engine.py
import requests
import json
from utils.cache import load_memory, save_memory
from content.formatter import format_quote

QUOTE_API = "https://api.quotable.io/random"

def post_quote(bot):
    mem = load_memory()
    sent_quotes = mem.get("quotes", [])

    for _ in range(5):  # try multiple times to avoid repeats
        resp = requests.get(QUOTE_API).json()
        quote_id = resp["_id"]
        if quote_id not in sent_quotes:
            sent_quotes.append(quote_id)
            mem["quotes"] = sent_quotes
            save_memory(mem)

            msg = format_quote(resp["content"], resp["author"])
            bot.send_message(chat_id=bot.chat_id, text=msg, parse_mode="HTML")
            return
