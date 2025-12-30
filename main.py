#from telegram import Bot
#from scheduler import start_scheduler
#from config import TELEGRAM_BOT_TOKEN

#bot = Bot(token=TELEGRAM_BOT_TOKEN)

#if __name__ == "__main__":
   #start_scheduler(bot)
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

bot = Bot(token=TELEGRAM_BOT_TOKEN)

if __name__ == "__main__":
    bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text="🚀 Bot is LIVE. Railway deployment successful."
    )
