# services/learning_service.py
from utils.summarizer import smart_summarize, analyst_wrap
from config import TELEGRAM_CHAT_ID
import requests
from bs4 import BeautifulSoup

LEARNING_SOURCES = [
    "https://www.coindesk.com/learn/",
    "https://www.cointelegraph.com/bitcoin-for-beginners"
]

def post_learning(bot):
    for article in LEARNING_SOURCES:
        try:
            r = requests.get(article, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            
            # Extract main article content
            paragraphs = soup.find_all("p")
            main_content = " ".join([p.get_text() for p in paragraphs])
            
            # Summarize
            summary = smart_summarize(main_content, sentences_count=3)
            if not summary:
                continue
            
            msg = f"📚 Learning Series\n\n{analyst_wrap(summary)}\nRead more: {article}\n— ViralCryptoInsights"
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
            break  # Only post one learning article per run
        except:
            continue
