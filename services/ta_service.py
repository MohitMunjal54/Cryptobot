from utils.rss_helpers import fetch_rss_entries
from utils.cache import load_memory, save_memory
from content.formatter import format_ta
from utils.summarizer import ai_summarize
from config import TA_FEEDS

def post_ta(bot):
    mem = load_memory()
    ta_ids = mem.get("ta_ids", [])

    for feed_url in TA_FEEDS:
        entries = fetch_rss_entries(feed_url)
        for entry in entries:
            if entry.id not in ta_ids:
                summary = ai_summarize(entry.summary, ratio=0.25)
                msg = format_ta(entry.title, summary, entry.link)
                bot.send_message(chat_id=bot.chat_id, text=msg, parse_mode="HTML")
                ta_ids.append(entry.id)
                mem["ta_ids"] = ta_ids
                save_memory(mem)
                return
