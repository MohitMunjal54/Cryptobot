from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import timezone
from datetime import datetime
from services import (
    crypto_service,
    news_service,
    whale_service,
    etf_service,
    events_service,
    quotes_service,
    learning_service,
    ta_service,
    festival_service
)
from config import TIMEZONE

tz = timezone(TIMEZONE)
scheduler = BlockingScheduler(timezone=tz)

def start_scheduler(bot):
    # Morning BTC/ETH prices (daily)
    scheduler.add_job(lambda: crypto_service.post_prices(bot), 'cron', hour=8, minute=30)

    # Market snapshot (daily)
    scheduler.add_job(lambda: crypto_service.post_market_snapshot(bot), 'cron', hour=10, minute=30)

    # Crypto news & ETF updates (daily)
    scheduler.add_job(lambda: news_service.post_news(bot), 'cron', hour=12, minute=30)
    scheduler.add_job(lambda: etf_service.post_etf(bot), 'cron', hour=13, minute=0)

    # Whale alerts (every 30 mins)
    scheduler.add_job(lambda: whale_service.post_whale_alerts(bot), 'interval', minutes=30)

    # Crypto + Macro events (daily)
    scheduler.add_job(lambda: events_service.post_crypto_and_macro_events(bot), 'cron', hour=10, minute=30)

    # Motivational quotes (daily)
    scheduler.add_job(lambda: quotes_service.post_quote(bot), 'cron', hour=18, minute=30)

    # Festival greetings (daily)
    scheduler.add_job(lambda: festival_service.post_festival_greeting(bot), 'cron', hour=9, minute=0)

    # 🌙 Good night reminder (daily)
    scheduler.add_job(lambda: quotes_service.post_good_night(bot), 'cron', hour=21, minute=30)

    # 💡 Learning & TA Series – Weekends only (Sat & Sun)
    scheduler.add_job(lambda: learning_service.post_learning(bot), 'cron', day_of_week='sat,sun', hour=17, minute=0)
    scheduler.add_job(lambda: ta_service.post_ta(bot), 'cron', day_of_week='sat,sun', hour=18, minute=0)

    scheduler.start()
