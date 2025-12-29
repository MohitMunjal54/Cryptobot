import requests
from config import FEAR_GREED_API, TELEGRAM_CHAT_ID

def fear_greed(bot):
    data = requests.get(FEAR_GREED_API).json()["data"][0]
    value = data["value"]
    classification = data["value_classification"]

    msg = (
        f"📊 Market Sentiment Update\n\n"
        f"Fear & Greed Index: {value}\n"
        f"Sentiment: {classification}\n\n"
        "Markets often move opposite to extreme emotions.\n"
        "— ViralCryptoInsights"
    )

    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
