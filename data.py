import requests
from symbol import BINANCE_ORDER_BOOK, BINANCE_DATA, BYBIT_DATA, BITGET, MEXC, KUCOIN, KUCOIN_ORDER_BOOK, GATE
from filtered_funding import symbols_map


# Function for data binance
def get_data_binance(symbol: str) -> dict:
    result = {}
    # Get volume
    k = requests.get(BINANCE_DATA).json()
    # Get orderbook
    q = requests.get(BINANCE_ORDER_BOOK).json()
    volume = {vol['symbol']: float(vol['quoteVolume']) for vol in k}
    for t in q:
        if t['symbol'] == symbol:
            result[symbol] = {
                'bid': float(t['bidPrice']),
                'ask': float(t['askPrice']),
                'volume 24H': volume.get(symbol, 0.0),
            }
    return result


def get_data_bybit(symbol: str) -> dict:
    result = {}
    # Get data
    k = requests.get(BYBIT_DATA, params={'category': 'linear'}).json()

    for t in k['result']['list']:
        if t['symbol'] == symbol:
            result[symbol] = {
                'bid': float(t['bid1Price']),
                'ask': float(t['ask1Price']),
                'volume 24H': float(t['turnover24h']),
            }
    return result


def get_data_bitget(symbol: str) -> dict:
    result = {}
    params = {"productType": "USDT-FUTURES"}
    k = requests.get(BITGET, params=params).json()
    for t in k['data']:
        if t['symbol'] == symbol:
            result[symbol] = {
                'bid': float(t['bidPr']),
                'ask': float(t['askPr']),
                'volume 24H': float(t['usdtVolume']),
            }
    return result


def get_data_mexc(symbol: str) -> dict:
    result = {}
    k = requests.get(MEXC).json()
    for t in k['data']:
        if t['symbol'] == symbol.replace('USDT', '_USDT'):
            result[symbol] = {
                'bid': float(t['bid1']),
                'ask': float(t['ask1']),
                'volume 24H': float(t['volume24']),
            }
    return result


def get_data_kucoin(symbol: str) -> dict:
    try:
        result = {}
        symbol_kucoin = symbol.replace('USDT', 'USDTM').replace('BTC', 'XBT')
        k = requests.get(KUCOIN_ORDER_BOOK, params={"symbol": symbol_kucoin}).json()
        d = requests.get(KUCOIN, params={"symbol": symbol_kucoin}).json()
    except Exception as e:
        print(f"KuCoin request error for {symbol}: {e}")
        return None

        # Проверяем code
    if k.get("code") != "200000":
        return None

    if d.get("code") != "200000":
        return None

    data = k.get("data")
    if not data:
        return None

    for c in d["data"]:
        if c["symbol"] == symbol_kucoin:
            volume = float(c.get("turnoverOf24h", 0))
    result[symbol] = {
        'bid': float(data['bestBidPrice']),
        'ask': float(data['bestAskPrice']),
        'volume 24H': volume,
    }
    return result


def get_data_gate(symbol: str) -> dict:
    result = {}
    k = requests.get(GATE).json()
    for t in k:
        if t['contract'] == symbol.replace('USDT', '_USDT'):
            result[symbol] = {
                'bid': float(t['highest_bid']),
                'ask': float(t['lowest_ask']),
                'volume 24H': float(t['volume_24h_base']),
            }
    return result


def collect_symbols_and_data():
    result = {}
    for symbol, exchanges in symbols_map.items():
        result[symbol] = {}
        if 'binance' in exchanges:
            if data := get_data_binance(symbol):  # Need for get only coins with data
                result[symbol]['binance'] = data
            else:
                print(None)
        if 'bybit' in exchanges:
            if data := get_data_bybit(symbol):  # Need for get only coins with data
                result[symbol]['bybit'] = data
            else:
                print(None)
        if 'bitget' in exchanges:
            if data := get_data_bitget(symbol):  # Need for get only coins with data
                result[symbol]['bitget'] = data
            else:
                print(None)
        if 'mexc' in exchanges:
            if data := get_data_mexc(symbol):  # Need for get only coins with data
                result[symbol]['mexc'] = data
            else:
                print(None)
        if 'kucoin' in exchanges:
            if data := get_data_kucoin(symbol):  # Need for get only coins with data
                result[symbol]['kucoin'] = data
            else:
                print(None)
        if 'gate' in exchanges:
            if data := get_data_gate(symbol):  # Need for get only coins with data
                result[symbol]['gate'] = data
            else:
                print(None)
    return result


collect_symbols_and_data = collect_symbols_and_data()