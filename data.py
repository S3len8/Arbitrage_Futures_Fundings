import requests


def get_binance_futures_usdt():
    # Bid / Ask - берем для порівняння ф'ючерсів
    book = requests.get(
        f"https://fapi.binance.com/fapi/v1/ticker/bookTicker"
    ).json()

    # 24h volume - об'єм монети за 24 години
    tickers = requests.get(
        f"https://fapi.binance.com/fapi/v1/ticker/24hr"
    ).json()

    # Funding
    funding = requests.get(
        f"https://fapi.binance.com/fapi/v1/premiumIndex"
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


def get_bybit_futures_usdt():
    # Getting tickers from Bybit
    tickers = requests.get(
        f"https://api.bybit.com/v5/market/tickers",
        params={'category': 'linear'}
    ).json()['result']['list']

    # Adding symbols to dict
    result = {}

    # Cycle for searching symbols with USDT and orderbook in all tickers
    for t in tickers:
        symbol = t['symbol']

        if not symbol.endswith('USDT'):
            continue

        order_book = requests.get(
            f"https://api.bybit.com/v5/market/orderbook",
            params={
                'category': 'linear',
                'symbol': symbol,
                'limit': 1,
            }
        ).json()['result']

        if not order_book['a'] or not order_book['b']:
            continue

        result[symbol] = {
            'ask': float(order_book['a'][0][0]),
            'bid': float(order_book['b'][0][0]),
            'volume': float(t['turnover24h']),
            'funding': float(t['fundingRate'])
        }

    return result


binance = get_binance_futures_usdt()
print("BINANCE:", len(binance))
print(list(binance.items())[:3])
print("BTCUSDT:", binance.get("BTCUSDT"))

bybit = get_bybit_futures_usdt()
print("BYBIT:", len(bybit))
print(list(bybit.items())[:3])