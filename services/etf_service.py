# services/etf_service.py
import requests
from config import TELEGRAM_CHAT_ID
from utils.cache import load_memory, save_memory

# ETF free source (CoinGecko + public filings)
ETF_DATA = {
    "BTC": "https://www.etf.com/bitcoin-etf-data",
    "ETH": "https://www.etf.com/ethereum-etf-data"
}

def fetch_etf_flows():
    # Dummy free implementation: fetch and parse publicly available HTML or JSON
    flows = {}
    for symbol, url in ETF_DATA.items():
        try:
            resp = requests.get(url).text
            # Parse inflow/outflow from HTML (simplified)
            flows[symbol] = {
                "inflow": round(1000000 * 0.5, 0),  # placeholder
                "outflow": round(1000000 * 0.3, 0)
            }
        except:
            flows[symbol] = {"inflow": 0, "outflow": 0}
    return flows

def post_etf_update(bot):
    mem = load_memory()
    flows = fetch_etf_flows()
    msg = "🏦 Weekly ETF Flow Update\n\n"
    for sym, data in flows.items():
        msg += f"{sym} ETF: Inflow: ${data['inflow']:,}, Outflow: ${data['outflow']:,}\n"

    msg += "\nETF movements affect market sentiment and liquidity.\n— ViralCryptoInsights"
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
