import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode

API_KEY = 'OcirhzEKhIgPDd9wcV0fOTaMMoVBq3mLY8ESmEFZXcZ53doPfPIgsSZMZVz74bSy'
API_SECRET = 'jvYQuPuM26KLvY3M67FlYtAZpCHLTf7Hc3qBhs7Ch5DPx6mxQ7mqDCwZnMywm1Sf'

BINANCE_ORDER_BOOK = 'https://fapi.binance.com/fapi/v1/ticker/bookTicker'
BINANCE_DATA = 'https://fapi.binance.com/fapi/v1/ticker/24hr'
BINANCE_FUNDING = 'https://fapi.binance.com/fapi/v1/premiumIndex'
BINANCE_FEES = 'https://fapi.binance.com/fapi/v1/commissionRate'

BYBIT_DATA = 'https://api.bybit.com/v5/market/tickers'

FEES = {
    'Binance maker:': 0.0002,
    'Binance taker:': 0.0005,
    'Bybit maker:': 0.00036,
    'Bybit taker:': 0.001,
    'Bitget maker:': 0.0002,
    'Bitget taker:': 0.0006,
    'MEXC maker:': 0.0001,
    'MEXC taker:': 0.0004,
    'Gate maker:': 0.0002,
    'Gate taker:': 0.0005,
    'Kucoin maker:': 0.0002,
    'Kucoin taker:': 0.0006,
}


# Function for getting only symbols from Binance
def get_binance_symbol():
    url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
    data = requests.get(url).json()

    result = []
    for symbol in data['symbols']:
        if symbol['contractType'] == 'PERPETUAL':
            result.append({
                'symbol': symbol['symbol'],
            })
    return result


# Function for getting only symbols from Bybit
def get_bybit_symbol():
    url = 'https://api.bybit.com/v5/market/instruments-info?category=linear&settleCoin=USDT'
    params = {'category': 'linear'}
    data = requests.get(url, params=params).json()

    result = []
    for symbol in data['result']['list']:
        if symbol['status'] == 'Trading' and symbol['contractType'] == 'LinearPerpetual':
            result.append({
                'symbol': symbol['symbol']
            })
    return result


binance = get_binance_symbol()
bybit = get_bybit_symbol()


# Function for comparison symbols
def comparison_symbols(binance: list, bybit: list) -> list:
    binance_symbol = {item['symbol'] for item in binance}
    bybit_symbol = {item['symbol'] for item in bybit}
    return list(binance_symbol & bybit_symbol)


common_symbols = comparison_symbols(binance=binance, bybit=bybit)  # <class 'list'>


# Function for data binance
def get_data_binance(common_symbols: list[str]) -> dict:
    symbols_set = set(common_symbols)
    result = {}
    # Get volume
    k = requests.get(BINANCE_DATA).json()
    # Get funding
    v = requests.get(BINANCE_FUNDING).json()
    # Get orderbook
    q = requests.get(BINANCE_ORDER_BOOK).json()
    funding = {
        f['symbol']: float(f['lastFundingRate'])
        for f in v
        if f['symbol'] in symbols_set
    }
    volume = {
        vol['symbol']: float(vol['quoteVolume'])
        for vol in k
        if vol['symbol'] in symbols_set
    }
    for t in q:
        symbol = t['symbol']
        if symbol not in symbols_set:
            continue

        result[symbol] = {
            'bid': float(t['bidPrice']),
            'ask': float(t['askPrice']),
            'volume 24H': volume.get(symbol, 0.0),
            'funding': funding.get(symbol, 0.0)
        }
    return result


def get_data_bybit(common_symbols: list[str]) -> dict:
    symbols_set = set(common_symbols)
    result = {}
    # Get data
    k = requests.get(BYBIT_DATA, params={'category': 'linear'}).json()

    for t in k['result']['list']:
        symbol = t['symbol']
        if symbol not in symbols_set:
            continue

        result[symbol] = {
            'bid': float(t['bid1Price']),
            'ask': float(t['ask1Price']),
            'volume 24H': float(t['turnover24h']),
            'funding': float(t['fundingRate'])
        }
    return result


binance_data = get_data_binance(common_symbols)  # <class 'dict'>
bybit_data = get_data_bybit(common_symbols)  # <class 'dict'>
coins_after_comparison = set(common_symbols) & binance_data.keys()  # Need for get real same symbols from Binance and Bybit <class 'set'>
# def get_fees_binance(symbol):  # {'symbol': 'BTCUSDT', 'makerCommissionRate': '0.000200', 'takerCommissionRate': '0.000500', 'rpiCommissionRate': '0'}
#     params = {
#         'symbol': symbol,
#         'timestamp': int(time.time() * 1000)
#     }
#
#     query = urlencode(params)
#     signature = hmac.new(
#         API_SECRET.encode(),
#         query.encode(),
#         hashlib.sha256
#     ).hexdigest()
#
#     params['signature'] = signature
#
#     headers = {
#         'X-MBX-APIKEY': API_KEY
#     }
#
#     r = requests.get(
#         BINANCE_FEES,
#         headers=headers,
#         params=params
#     )
#
#     return r.json()
#
#
# print(get_fees_binance('BTCUSDT'))
# print(coins_after_comparison, len(coins_after_comparison))
# print(get_binance_symbol(), len(get_binance_symbol()))
# print(get_bybit_symbol(), len(get_bybit_symbol()))
# print(common_symbols, len(comparison_symbols(binance, bybit)))
# print(binance_data, len(binance_data))
# print(bybit_data, len(bybit_data))
# print(bybit_data.keys() - binance_data.keys())
# try:
#     def get_binance_futures_usdt():
#         # Bid / Ask - берем для порівняння ф'ючерсів
#         book = requests.get(
#             f"https://fapi.binance.com/fapi/v1/ticker/bookTicker"
#         ).json()
#
#         # 24h volume - об'єм монети за 24 години
#         tickers = requests.get(
#             f"https://fapi.binance.com/fapi/v1/ticker/24hr"
#         ).json()
#
#         # Funding
#         funding = requests.get(
#             f"https://fapi.binance.com/fapi/v1/premiumIndex"
#         ).json()
#
#         # Книга ордерів
#         book_map = {
#             b["symbol"]: {
#                 "bid": float(b["bidPrice"]),
#                 "ask": float(b["askPrice"])
#             }
#             for b in book
#         }
#
#         # Книга фандінгу
#         funding_map = {
#             f["symbol"]: float(f["lastFundingRate"])
#             for f in funding
#         }
#
#         result = {}
#
#         # Цикл для перевірки ф'ючерса, щоб брати саме USDT і символ має мати книгу ордерів
#         for t in tickers:
#             symbol = t.get("symbol")
#
#             if not symbol or not symbol.endswith("USDT"):
#                 continue
#
#             if symbol not in book_map:
#                 continue
#
#             # Систематизація інформації
#             result[symbol] = {
#                 **book_map[symbol],
#                 "volume_usdt_24h": float(t["quoteVolume"]),
#                 "funding": funding_map.get(symbol)
#             }
#
#         return result
#
#
#     def get_bybit_futures_usdt():
#         # Getting tickers from Bybit
#         tickers = requests.get(
#             f"https://api.bybit.com/v5/market/tickers",
#             params={'category': 'linear'}
#         ).json()['result']['list']
#
#         # Adding symbols to dict
#         result = {}
#
#         # Cycle for searching symbols with USDT and orderbook in all tickers
#         for t in tickers:
#             symbol = t['symbol']
#
#             if not symbol.endswith('USDT'):
#                 continue
#
#             order_book = requests.get(
#                 f"https://api.bybit.com/v5/market/orderbook",
#                 params={
#                     'category': 'linear',
#                     'symbol': symbol,
#                     'limit': 1,
#                 }
#             ).json()['result']
#
#             if not order_book['a'] or not order_book['b']:
#                 continue
#
#             result[symbol] = {
#                 'ask': float(order_book['a'][0][0]),
#                 'bid': float(order_book['b'][0][0]),
#                 'volume': float(t['turnover24h']),
#                 'funding': float(t['fundingRate'])
#             }
#
#         return result
#
#
#     binance = get_binance_futures_usdt()
#     bybit = get_bybit_futures_usdt()
#
#
#     def comparison_symbols(binance: dict, bybit: dict):
#         binance_symbols = set(binance.keys())
#         bybit_symbols = set(bybit.keys())
#
#         common_symbols = binance_symbols & bybit_symbols
#
#         result = {}
#
#         for symbol in common_symbols:
#             result[symbol] = {
#                 "binance": binance[symbol],
#                 "bybit": bybit[symbol]
#             }
#
#         return result
#
#
#     common = comparison_symbols(binance, bybit)
#     print(type(common))
#     print("COMMON:", len(common))
#     print(list(common.items())[:3])
# except KeyboardInterrupt as e:
#     print("Program ended!")
