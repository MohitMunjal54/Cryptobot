# content/formatter.py

def format_price_post(data):
    btc = data["bitcoin"]
    eth = data["ethereum"]
    sol = data["solana"]

    def format_coin(coin, symbol):
        change = coin.get("usd_24h_change", 0)
        emoji = "🟢" if change >= 0 else "🔴"
        return (
            f"{symbol}:\n"
            f"USD: ${coin['usd']:.2f} ({emoji}{change:.2f}%)\n"
            f"INR: ₹{coin['inr']:.2f}\n"
        )

    msg = "☕ Good Morning Family!\n\n"
    msg += "📊 Daily Crypto Prices\n\n"
    msg += format_coin(btc, "BTC")
    msg += format_coin(eth, "ETH")
    msg += format_coin(sol, "SOL")
    msg += "\nStay disciplined & informed.\n— ViralCryptoInsights"
    return msg


def format_learning(title, summary, url):
    return (
        f"📘 Learning Series\n\n"
        f"<b>{title}</b>\n"
        f"{summary}\n\n"
        f"<a href='{url}'>Read full article</a>\n\n"
        "🧠 Keep learning, stay disciplined.\n"
        "— ViralCryptoInsights"
    )


def format_ta(title, summary, url):
    return (
        f"📈 Technical Analysis Insight\n\n"
        f"<b>{title}</b>\n"
        f"{summary}\n\n"
        f"<a href='{url}'>Read full idea</a>\n\n"
        "🔍 Always combine structure with risk management.\n"
        "— ViralCryptoInsights"
    )


def format_quote(quote, author):
    return (
        f"💡 Daily Quote\n\n"
        f"\"{quote}\"\n"
        f"- {author}\n\n"
        "Stay disciplined & focused.\n— ViralCryptoInsights"
    )


def format_festival(name):
    return (
        f"🎉 Happy {name}!\n\n"
        "Wishing you joy, prosperity, and smart crypto moves.\n"
        "— ViralCryptoInsights"
    )
