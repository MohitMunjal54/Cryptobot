# services/events_service.py
import feedparser
from datetime import datetime, timedelta
from config import TELEGRAM_CHAT_ID
from utils.cache import load_memory, save_memory

# Crypto events (CoinGecko)
COINGECKO_EVENTS = "https://api.coingecko.com/api/v3/events"

# Free macro events RSS (Investing.com)
MACRO_RSS_URL = "https://www.investing.com/rss/financial-calendar.rss"

def fetch_crypto_events():
    """Fetch upcoming crypto events from CoinGecko"""
    import requests
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
    """Fetch macro events from Investing.com RSS feed"""
    today = datetime.utcnow().date()
    end = today + timedelta(days=7)
    feed = feedparser.parse(MACRO_RSS_URL)
    events = []
    for entry in feed.entries:
        try:
            # Convert RSS date string to date
            event_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z").date()
            if today <= event_date <= end:
                events.append({
                    "title": entry.title,
                    "date": event_date.strftime("%Y-%m-%d"),
                    "link": entry.link
                })
        except:
            continue
    return events

def post_crypto_and_macro_events(bot):
    """Post crypto and macro events to Telegram"""
    mem = load_memory()
    posted_events = mem.get("events_ids", [])

    # Crypto events
    crypto_events = fetch_crypto_events()
    for ev in crypto_events:
        if ev["id"] not in posted_events:
            msg = (
                f"📅 Upcoming Crypto Event\n\n"
                f"Name: {ev['title']}\n"
                f"Date: {ev['start_date']}\n"
                f"Type: {ev['type']}\n"
                f"More info: {ev.get('website','N/A')}\n\n"
                "Stay informed & plan wisely.\n— ViralCryptoInsights"
            )
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
            posted_events.append(ev["id"])

    # Macro events
    macro_events = fetch_macro_events()
    for ev in macro_events:
        macro_id = f"macro_{ev['title']}_{ev['date']}"
        if macro_id not in posted_events:
            msg = (
                f"📢 Upcoming Macro-Economic Event\n\n"
                f"Event: {ev['title']}\n"
                f"Date: {ev['date']}\n"
                f"More info: {ev['link']}\n\n"
                "This event may impact crypto markets.\n— ViralCryptoInsights"
            )
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
            posted_events.append(macro_id)

    mem["events_ids"] = posted_events
    save_memory(mem)
