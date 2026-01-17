import requests


def get_binance_futures_usdt():
    base = "https://fapi.binance.com"

    # Bid / Ask - берем для порівняння ф'ючерсів
    book = requests.get(
        f"{base}/fapi/v1/ticker/bookTicker", timeout=5
    ).json()

    # 24h volume - об'єм монети за 24 години
    tickers = requests.get(
        f"{base}/fapi/v1/ticker/24hr", timeout=5
    ).json()

    # Funding
    funding = requests.get(
        f"{base}/fapi/v1/premiumIndex", timeout=5
    ).json()

    # Книга ордерів
    book_map = {
        b["symbol"]: {
            "bid": float(b["bidPrice"]),
            "ask": float(b["askPrice"])
        }
        for b in book
    }

    # Книга фандінгу
    funding_map = {
        f["symbol"]: float(f["lastFundingRate"])
        for f in funding
    }

    result = {}

    # Цикл для перевірки ф'ючерса, щоб брати саме USDT і символ має мати книгу ордерів
    for t in tickers:
        symbol = t.get("symbol")

        if not symbol or not symbol.endswith("USDT"):
            continue

        if symbol not in book_map:
            continue

        # Систематизація інформації
        result[symbol] = {
            **book_map[symbol],
            "volume_usdt_24h": float(t["quoteVolume"]),
            "funding": funding_map.get(symbol)
        }

    return result


print(get_binance_futures_usdt()['BTCUSDT'])


def get_bybit_futures_usdt():
    pass