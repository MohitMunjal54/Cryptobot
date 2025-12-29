from telegram import Bot
from scheduler import start_scheduler
from config import TELEGRAM_BOT_TOKEN

bot = Bot(token=TELEGRAM_BOT_TOKEN)

if __name__ == "__main__":
    start_scheduler(bot)
