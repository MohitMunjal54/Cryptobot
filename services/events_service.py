# services/events_service.py
import requests
from datetime import datetime, timedelta
from config import TELEGRAM_CHAT_ID
from content.formatter import format_ta  # reuse formatting
from utils.cache import load_memory, save_memory

# Sample free events API (CoinGecko)
COINGECKO_EVENTS = "https://api.coingecko.com/api/v3/events"

def fetch_events():
    today = datetime.utcnow().date()
    end = today + timedelta(days=7)  # next 7 days
    params = {"upcoming_events_only": True}
    data = requests.get(COINGECKO_EVENTS, params=params).json()
    events = []
    for ev in data.get("data", []):
        start_date = datetime.strptime(ev["start_date"], "%Y-%m-%d").date()
        if today <= start_date <= end:
            events.append(ev)
    return events

def post_crypto_events(bot):
    mem = load_memory()
    posted_events = mem.get("events_ids", [])

    events = fetch_events()
    for ev in events:
        if ev["id"] not in posted_events:
            msg = (
                f"📅 Upcoming Crypto Event\n\n"
                f"Name: {ev['title']}\n"
                f"Date: {ev['start_date']}\n"
                f"Type: {ev['type']}\n"
                f"Platform: {ev.get('platform', 'N/A')}\n"
                f"More info: {ev.get('website', 'N/A')}\n\n"
                "Stay informed & plan wisely.\n— ViralCryptoInsights"
            )
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
            posted_events.append(ev["id"])
            mem["events_ids"] = posted_events
            save_memory(mem)
