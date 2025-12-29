import os

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# CoinGecko API
COINGECKO_BASE = "https://api.coingecko.com/api/v3"

# Fear & Greed Index
FEAR_GREED_API = "https://api.alternative.me/fng/"

# Crypto news RSS
CRYPTO_NEWS_RSS = "https://cryptopanic.com/feed/rss/"

# Learning / TA RSS
LEARNING_FEEDS = [
    "https://academy.binance.com/en/feed",
    "https://www.coingecko.com/learn/rss"
]

TA_FEEDS = [
    "https://www.tradingview.com/crypto/ideas/rss/",
    "https://cointelegraph.com/tags/technical-analysis/rss"
]

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")
# Timezone
TIMEZONE = "Asia/Kolkata"

# Volatility / Price Alert
PRICE_ALERT_PERCENT = 1.2

# Max posts/day
MAX_POSTS_PER_DAY = 10
