import requests


def get_binance_futures_usdt():
    base_url = "https://fapi.binance.com"

    # 1. Всі тікери (bid/ask + volume)
    tickers = requests.get(
        f"{base_url}/fapi/v1/ticker/24hr", timeout=5
    ).json()

    # 2. Funding
    funding = requests.get(
        f"{base_url}/fapi/v1/premiumIndex", timeout=5
    ).json()

    # Приводимо funding в словник
    funding_map = {
        f["symbol"]: float(f["lastFundingRate"])
        for f in funding
    }

    result = {}

    for t in tickers:
        symbol = t["symbol"]

        # Берем тільки USDT-фьючерси
        if not symbol.endswith("USDT"):
            continue

        result[symbol] = {
            "bid": float(t["bidPrice"]),
            "ask": float(t["askPrice"]),
            "volume_usdt_24h": float(t["quoteVolume"]),
            "funding": funding_map.get(symbol)
        }

    return result