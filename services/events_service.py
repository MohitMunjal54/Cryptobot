# services/events_service.py
import requests
from datetime import datetime, timedelta
from config import TELEGRAM_CHAT_ID
from utils.cache import load_memory, save_memory

# CoinGecko events (crypto protocol)
COINGECKO_EVENTS = "https://api.coingecko.com/api/v3/events"

# Macro & Economic Events
FOMC_EVENTS_URL = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
# For simplicity, we can parse manually or store key dates in JSON

IND_EVENTS = [
    {"name": "RBI Policy Meeting", "date": "2025-01-05", "type": "Indian Macro"},
    {"name": "Finance Budget 2025", "date": "2025-02-01", "type": "Indian Macro"}
]

def fetch_crypto_events():
    today = datetime.utcnow().date()
    end = today + timedelta(days=7)
    params = {"upcoming_events_only": True}
    data = requests.get(COINGECKO_EVENTS, params=params).json()
    events = []
    for ev in data.get("data", []):
        start_date = datetime.strptime(ev["start_date"], "%Y-%m-%d").date()
        if today <= start_date <= end:
            events.append(ev)
    return events

def fetch_macro_events():
    today = datetime.utcnow().date()
    end = today + timedelta(days=7)
    events = []
    for ev in IND_EVENTS:
        ev_date = datetime.strptime(ev["date"], "%Y-%m-%d").date()
        if today <= ev_date <= end:
            events.append(ev)
    return events

def post_crypto_events(bot):
    mem = load_memory()
    posted_events = mem.get("events_ids", [])

    # Crypto protocol events
    events = fetch_crypto_events()
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

    # Macro events
    macro_events = fetch_macro_events()
    for ev in macro_events:
        macro_id = f"macro_{ev['name']}_{ev['date']}"
        if macro_id not in posted_events:
            msg = (
                f"📢 Upcoming Macro-Economic Event\n\n"
                f"Event: {ev['name']}\n"
                f"Date: {ev['date']}\n"
                f"Type: {ev['type']}\n\n"
                "This may impact crypto markets.\n— ViralCryptoInsights"
            )
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
            posted_events.append(macro_id)

    mem["events_ids"] = posted_events
    save_memory(mem)
