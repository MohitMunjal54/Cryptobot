from utils.rss_helpers import fetch_rss_entries
from utils.cache import load_memory, save_memory
from content.formatter import format_learning
from utils.summarizer import ai_summarize
from config import LEARNING_FEEDS

def post_learning(bot):
    mem = load_memory()
    learning_ids = mem.get("learning_ids", [])

    for feed_url in LEARNING_FEEDS:
        entries = fetch_rss_entries(feed_url)
        for entry in entries:
            if entry.id not in learning_ids:
                summary = ai_summarize(entry.summary, ratio=0.25)
                msg = format_learning(entry.title, summary, entry.link)
                bot.send_message(chat_id=bot.chat_id, text=msg, parse_mode="HTML")
                learning_ids.append(entry.id)
                mem["learning_ids"] = learning_ids
                save_memory(mem)
                return
