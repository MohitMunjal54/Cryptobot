from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import timezone
import random

from services.events_service import post_crypto_and_macro_events
from community.greetings import good_morning, good_night
from services.market_service import daily_prices
from services.sentiment_service import fear_greed
from services.news_service import top_news
from services.learning_service import post_learning
from services.ta_service import post_ta
from community.polls_engine import weekend_poll
from services.events_service import post_crypto_events
from services.whale_service import post_whale_alert
from services.etf_service import post_etf_update


tz = timezone("Asia/Kolkata")

def jitter(mins=20):
    return random.randint(-mins, mins)

def start_scheduler(bot):
    scheduler = BlockingScheduler(timezone=tz)

    scheduler.add_job(lambda: good_morning(bot), 'cron', hour=8, minute=30+jitter())
    scheduler.add_job(lambda: daily_prices(bot), 'cron', hour=9, minute=30+jitter())
    scheduler.add_job(lambda: fear_greed(bot), 'cron', hour=11, minute=30+jitter())
    scheduler.add_job(lambda: top_news(bot), 'cron', hour=13, minute=30+jitter())
    scheduler.add_job(lambda: post_learning(bot), 'cron', hour=16, minute=30+jitter())
    scheduler.add_job(lambda: post_ta(bot), 'cron', hour=18, minute=0+jitter())
    scheduler.add_job(lambda: weekend_poll(bot), 'cron', day_of_week='sat', hour=20)
    scheduler.add_job(lambda: good_night(bot), 'cron', hour=21, minutes=0)
    scheduler.add_job(lambda: post_crypto_and_macro_events(bot), 'cron', hour=10, minute=30)
    # Whale alerts: daily at 14:00 IST
    scheduler.add_job(lambda: post_whale_alert(bot), 'cron', hour=14, minute=0)

    # ETF updates: weekly Monday 12:30 IST
    scheduler.add_job(lambda: post_etf_update(bot), 'cron', day_of_week='mon', hour=12, minute=30)


    scheduler.start()
