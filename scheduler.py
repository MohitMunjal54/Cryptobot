from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import timezone
import os
from services import (
    crypto_service,
    news_service,
    whale_service,
    etf_service,
    events_service,
    quotes_service,
    learning_service,
    festival_service
)

from config import TIMEZONE

tz = timezone(TIMEZONE)
scheduler = BlockingScheduler(timezone=tz)

def start_scheduler(bot):
    # Morning BTC/ETH prices
    scheduler.add_job(lambda: crypto_service.post_prices(bot), 'cron', hour=8, minute=30)
    
    # Market snapshot
    scheduler.add_job(lambda: crypto_service.post_market_snapshot(bot), 'cron', hour=10, minute=30)
    
    # Crypto news & ETF updates
    scheduler.add_job(lambda: news_service.post_news(bot), 'cron', hour=12, minute=30)
    scheduler.add_job(lambda: etf_service.post_etf(bot), 'cron', hour=13, minute=0)
    
    # Whale alerts
    scheduler.add_job(lambda: whale_service.post_whale_alerts(bot), 'interval', minutes=30)
    
    # Crypto + Macro events
    scheduler.add_job(lambda: events_service.post_crypto_and_macro_events(bot), 'cron', hour=10, minute=30)
    
    # Motivational quotes
    scheduler.add_job(lambda: quotes_service.post_quote(bot), 'cron', hour=18, minute=30)
    
    # Learning / TA series
    scheduler.add_job(lambda: learning_service.post_learning(bot), 'cron', hour=17, minute=0)
    
    # Festival greetings
    scheduler.add_job(lambda: festival_service.post_festival_greeting(bot), 'cron', hour=9, minute=0)
    
    scheduler.start()
