# community/polls_engine.py
from telegram import Poll
import random

# Simple crypto poll for weekends
POLL_QUESTIONS = [
    {"q": "BTC next week trend?", "options": ["Bullish", "Bearish", "Sideways"]},
    {"q": "ETH dominant layer?", "options": ["Layer1", "Layer2", "Both"]}
]

def weekend_poll(bot):
    poll = random.choice(POLL_QUESTIONS)
    bot.send_poll(chat_id=bot.chat_id, question=poll["q"], options=poll["options"], is_anonymous=True)
