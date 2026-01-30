# import aiohttp
# import asyncio
import requests
# import time
# import hmac
# import hashlib
# from urllib.parse import urlencode
from symbol import BINANCE_ORDER_BOOK, BINANCE_DATA, BYBIT_DATA, BITGET, MEXC, KUCOIN, KUCOIN_ORDER_BOOK, GATE
from filtered_funding import symbols_map
#
# API_KEY = 'OcirhzEKhIgPDd9wcV0fOTaMMoVBq3mLY8ESmEFZXcZ53doPfPIgsSZMZVz74bSy'
# API_SECRET = 'jvYQuPuM26KLvY3M67FlYtAZpCHLTf7Hc3qBhs7Ch5DPx6mxQ7mqDCwZnMywm1Sf'
#
# BINANCE_ORDER_BOOK = 'https://fapi.binance.com/fapi/v1/ticker/bookTicker'
# BINANCE_DATA = 'https://fapi.binance.com/fapi/v1/ticker/24hr'
# BINANCE_FUNDING = 'https://fapi.binance.com/fapi/v1/premiumIndex'
# BINANCE_FEES = 'https://fapi.binance.com/fapi/v1/commissionRate'
#
# BYBIT_DATA = 'https://api.bybit.com/v5/market/tickers'
#
# BITGET = 'https://api.bitget.com/api/v2/mix/market/tickers'
#
# MEXC = 'https://contract.mexc.com/api/v1/contract/ticker'
#
# KUCOIN = 'https://api-futures.kucoin.com/api/v1/contracts/active'
# KUCOIN_FUNDING = "https://api-futures.kucoin.com/api/v1/funding-rate/{symbol}/current"
#
# GATE = 'https://api.gateio.ws/api/v4/futures/usdt/tickers'
#
# FEES = {
#     'Binance': {
#         'maker:': 0.0002,
#         'taker:': 0.0005,
#     },
#     'Bybit': {
#         'maker:': 0.00036,
#         'taker:': 0.001,
#     },
#     'Bitget': {
#         'maker:': 0.0002,
#         'taker:': 0.0006,
#     },
#     'MEXC': {
#         'maker:': 0.0001,
#         'taker:': 0.0004,
#     },
#     'Gate': {
#         'maker:': 0.0002,
#         'taker:': 0.0005,
#     },
#     'Kucoin': {
#         'maker:': 0.0002,
#         'taker:': 0.0006,
#     },
# }
#
#
# # Function for getting only symbols from Binance
# def get_binance_symbol():
#     url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
#     data = requests.get(url).json()
#
#     result = []
#     for symbol in data['symbols']:
#         if symbol['contractType'] == 'PERPETUAL':
#             result.append({
#                 'symbol': symbol['symbol'],
#             })
#     return result
#
#
# # Function for getting only symbols from Bybit
# def get_bybit_symbol():
#     url = 'https://api.bybit.com/v5/market/instruments-info?category=linear&settleCoin=USDT'
#     params = {'category': 'linear'}
#     data = requests.get(url, params=params).json()
#
#     result = []
#     for symbol in data['result']['list']:
#         if symbol['status'] == 'Trading' and symbol['contractType'] == 'LinearPerpetual':
#             result.append({
#                 'symbol': symbol['symbol']
#             })
#     return result
#
#
# def get_bitget_symbol():
#     params = {"productType": "USDT-FUTURES"}
#     data = requests.get(BITGET, params=params).json()
#     result = []
#     for symbol in data['data']:
#         result.append({
#             'symbol': symbol['symbol']
#         })
#
#     return result
#
#
# def get_mexc_symbol():
#     result = []
#     data = requests.get(MEXC).json()
#     for key in data['data']:
#         symbol = key['symbol']
#         result.append({
#             'symbol': symbol.replace('_', '')
#         })
#     return result
#
#
# # def get_kucoin_symbol():
# #     result = []
# #     data = requests.get(KUCOIN).json()
# #     for key in data['data']:
# #         symbol = key['symbol']
# #         result.append({
# #             'symbol': symbol.replace('XBT', 'BTC').replace('USDTM', 'USDT'),
# #         })
# #
# #     return result
#
# async def get_kucoin_symbol():
#     async with aiohttp.ClientSession() as session:
#         async with session.get(KUCOIN) as kucoin:
#             data = await kucoin.json()
#
#     return [{'symbol': item['symbol']} for item in data['data']]
#
#
# def get_gate_symbol():
#     result = []
#     data = requests.get(GATE).json()
#     for key in data:
#         symbol = key['contract']
#         result.append({
#             'symbol': symbol.replace('_', ''),
#         })
#
#     return result
#
#
# binance = get_binance_symbol()  # [{'symbol': 'BTCUSDT'}, {'symbol': 'ETHUSDT'}, {'symbol': 'BCHUSDT'}, {'symbol': 'XRPUSDT'}, {'symbol': 'LTCUSDT'}]
# bybit = get_bybit_symbol()  # [{'symbol': '0GUSDT'}, {'symbol': '1000000BABYDOGEUSDT'}, {'symbol': '1000000CHEEMSUSDT'}, {'symbol': '1000000MOGUSDT'}]
# bitget = get_bitget_symbol()  #  [{'symbol': 'BTCUSDT'}, {'symbol': 'ETHUSDT'}, {'symbol': 'XRPUSDT'}, {'symbol': 'BCHUSDT'}, {'symbol': 'LTCUSDT'}]
# mexc = get_mexc_symbol()  # [{'symbol': 'BTCUSDT'}, {'symbol': 'ETHUSDT'}, {'symbol': 'SOLUSDT'}, {'symbol': 'RIVERUSDT'}, {'symbol': 'XAUTUSDT'}, {'symbol': 'BTCUSD'}, {'symbol': 'SILVERUSDT'}]
# kucoin = asyncio.run(get_kucoin_symbol())  # {'BTC': 'XBTUSDTM', 'ETH': 'ETHUSDTM', 'SOL': 'SOLUSDTM', 'WIF': 'WIFUSDTM', 'PEPE': 'PEPEUSDTM', 'DOGE': 'DOGEUSDTM', 'XRP': 'XRPUSDTM', '0G': '0GUSDTM'} [{'symbol': 'XBTUSDTM'}, {'symbol': 'ETHUSDTM'}, {'symbol': 'SOLUSDTM'}, {'symbol': 'WIFUSDTM'}, {'symbol': 'PEPEUSDTM'}, {'symbol': 'DOGEUSDTM'}, {'symbol': 'XRPUSDTM'}]
# gate = get_gate_symbol()  # [{'symbol': 'RAREUSDT'}, {'symbol': 'FILUSDT'}, {'symbol': 'GIGGLEUSDT'}, {'symbol': 'RECALLUSDT'}, {'symbol': 'LYNUSDT'}, {'symbol': 'SONICUSDT'}, {'symbol': 'TAUSDT'}]
# # print(kucoin)
#
#
# async def fetch_all_and_compare():
#     kucoin = await asyncio.gather(
#         get_kucoin_symbol(),
#     )
#
#     return kucoin
#
#
# def normalize(symbol: str) -> str:
#     return symbol.replace('USDTM', '').replace('USDT', '').replace('PERP', '').replace('USDC', '').replace('_USDT', '').replace('XBT', 'BTC').replace('USD', '').replace('_', '')
#
#
# def comparison_symbols(binance: list, bybit: list, bitget: list, mexc: list, kucoin: list, gate: list) -> list:
#     binance_symbol = {normalize(item['symbol']) for item in binance}
#     bybit_symbol = {normalize(item['symbol']) for item in bybit}
#     bitget_symbol = {normalize(item['symbol']) for item in bitget}
#     mexc_symbol = {normalize(item['symbol']) for item in mexc}
#     kucoin_symbol = {normalize(item['symbol']) for item in kucoin}
#     gate_symbols = {normalize(item['symbol']) for item in gate}
#     sets = [binance_symbol, bybit_symbol, bitget_symbol, mexc_symbol, kucoin_symbol, gate_symbols]
#
#     return list(set().union(*sets))
#
#
# kucoin = asyncio.run(fetch_all_and_compare())
# kucoin_list = kucoin[0]
# common_symbols = comparison_symbols(binance=binance, bybit=bybit, bitget=bitget, mexc=mexc, kucoin=kucoin_list, gate=gate)  # <class 'list'>
# # print(common_symbols, len(common_symbols))  # ['INJ', 'NIL', 'DEXE', 'PTB', 'REZ', 'CHZ', 'BANANA', 'ANIME', 'ANKR', 'FLUID', 'RENDER', 'C98', 'BLUAI', 'CTK', 'PIPPIN', 'GMX', 'LINEA', 'EVAA', 'COOKIE', 'MYX', 'ENJ']
#
#
# def get_funding_binance() -> dict:
#     symbols_set = set(common_symbols)
#     result = {}
#     # Get funding
#     v = requests.get(BINANCE_FUNDING).json()
#     for key in v:
#         symbol = key['symbol']
#         if symbol.endswith('USDC'):
#             continue
#         if symbol.endswith('USD'):
#             continue
#         if symbol in symbols_set:
#             continue
#         symbol = key['symbol']
#         result[symbol] = {
#             'funding': float(key['lastFundingRate']),
#         }
#     return result
#
#
# def get_funding_bybit():
#     symbols_set = set(common_symbols)
#     result = {}
#     # Get data
#     k = requests.get(BYBIT_DATA, params={'category': 'linear'}).json()
#     for t in k['result']['list']:
#         symbol = t['symbol']
#         funding_raw = t.get('fundingRate')  # Need for getting all symbols with and without funding
#         if symbol.endswith('PERP'):
#             continue
#         if symbol.endswith('USDC'):
#             continue
#         if symbol.endswith('USD'):
#             continue
#         if symbol in symbols_set:
#             continue
#
#         if funding_raw not in ('', None):
#             result[symbol] = {
#                 'funding': float(funding_raw)
#             }
#     return result
#
#
# def get_funding_bitget():
#     symbols_set = set(common_symbols)
#     params = {"productType": "USDT-FUTURES"}
#     result = {}
#     k = requests.get(BITGET, params=params).json()
#     for t in k['data']:
#         symbol = t['symbol']
#         if symbol.endswith('PERP'):
#             continue
#         if symbol.endswith('USDC'):
#             continue
#         if symbol.endswith('USD'):
#             continue
#         if symbol in symbols_set:
#             continue
#
#         result[symbol] = {
#             'funding': float(t['fundingRate'])
#         }
#     return result
#
#
# def get_funding_mexc():
#     symbols_set = set(common_symbols)
#     result = {}
#     k = requests.get(MEXC).json()
#     for t in k['data']:
#         symbol = t['symbol']
#         normalize_symbol = symbol.replace('_', '')
#         if symbol.endswith('USDC'):
#             continue
#         if symbol.endswith('USD'):
#             continue
#         if normalize_symbol in symbols_set:
#             continue
#         result[normalize_symbol] = {
#             'funding': float(t['fundingRate'])
#         }
#     return result
#
#
# # def get_funding_kucoin():
# #     symbols_set = set(common_symbols)
# #     result = {}
# #     symbols = get_kucoin_symbol()
# #     for item in symbols:
# #         symbol = item['symbol']
# #         url = f"https://api-futures.kucoin.com/api/v1/funding-rate/{symbol}/current"
# #         r = requests.get(url).json()
# #         data = r.get('data')
# #         normalize_symbol = symbol.replace('XBT', 'BTC')
# #         print(data)
# #         if not data:
# #             continue
# #         if normalize_symbol in symbols_set:
# #             continue
# #         print(normalize_symbol)
# #         result[normalize_symbol] = {
# #             'funding': float(data['value'])
# #         }
# #
# #         time.sleep(0.05)  # Rate limit
# #
# #     return result
#
# async def fetch_funding(session, symbol):
#     url = KUCOIN_FUNDING.format(symbol=symbol)
#     try:
#         async with session.get(url) as r:
#             data = await r.json()
#             if data.get('code') != "200000":
#                 print(f"Warning: funding not supported for {symbol} ({data.get('msg')})")
#                 return symbol, None
#             return symbol, {'funding': float(data['data']['value'])}
#     except Exception as e:
#         print(f"Error fetching {symbol}: {e}")
#         return symbol, None
#
#
# async def get_funding_kucoin(symbols):
#     async with aiohttp.ClientSession() as session:
#         tasks = [fetch_funding(session, s) for s in symbols]
#         results = await asyncio.gather(*tasks)
#         return dict(results)
#
#
# symbols = [item['symbol'] for item in kucoin_list]
#
#
# def get_funding_gate():
#     symbols_set = set(common_symbols)
#     result = {}
#     data = requests.get(GATE).json()
#     for key in data:
#         symbol = key['contract']
#         normalize_symbol = symbol.replace('_', '')
#         if normalize_symbol in symbols_set:
#             continue
#         result[normalize_symbol] = {
#             'funding': float(key['funding_rate'])
#         }
#
#     return result
#
#
# binance_funding = get_funding_binance()  # Example print {'USDCUSDT': {'funding': 5.301e-05}, 'GRIFFAINUSDT': {'funding': 5e-05}, 'GMXUSDT': {'funding': 6.258e-05}, 'BANUSDT': {'funding': 5e-05}}
# bybit_funding = get_funding_bybit()  # Example print {'0GUSDT': {'funding': -0.00062216}, '1000000BABYDOGEUSDT': {'funding': 5e-05}, '1000000CHEEMSUSDT': {'funding': 5e-05}, '1000000MOGUSDT': {'funding': -0.00065514}}
# bitget_funding = get_funding_bitget()   # Example print {'BTCUSDT': {'funding': 5.8e-05}, 'ETHUSDT': {'funding': 1.5e-05}, 'XRPUSDT': {'funding': 0.0001}, 'BCHUSDT': {'funding': -6.6e-05}, 'LTCUSDT': {'funding': 0.0001}}
# mexc_funding = get_funding_mexc()  # Example {'BTCUSDT': {'funding': 5e-05}, 'ETHUSDT': {'funding': -0.000117}, 'SOLUSDT': {'funding': -0.000196}, 'RIVERUSDT': {'funding': -0.001273}, 'XAUTUSDT': {'funding': 5e-05}}
# kucoin_funding = asyncio.run(get_funding_kucoin(symbols))  # Example {'BTCUSDT': {'funding': -7e-06}, 'ETHUSDT': {'funding': -5.5e-05}, 'SOLUSDT': {'funding': -2.8e-05}, 'WIFUSDT': {'funding': -3e-06}, 'PEPEUSDT': {'funding': -2.2e-05}}  {'XBTUSDTM': {'funding': -7e-06}, 'ETHUSDTM': {'funding': 1.3e-05}, 'SOLUSDTM': {'funding': -3e-06}, 'WIFUSDTM': {'funding': 0.000173}, 'PEPEUSDTM': {'funding': -0.000166}}
# gate_funding = get_funding_gate()  # Example {'DOTUSDT': {'funding': -0.00012}, '人生K线USDT': {'funding': 5e-05}, 'IMXUSDT': {'funding': 5e-05}, 'USUALUSDT': {'funding': 1.2e-05}, 'EPICUSDT': {'funding': -0.00166}, 'IPUSDT': {'funding': 1.2e-05}}
# no_kucoin_funding = {k.replace('USDTM', 'USDT').replace('XBT', 'BTC'): v for k, v in kucoin_funding.items()}  # Need for converting symbols ETHUSDTM to ETHUSDT
# # print(binance_funding)
# # print(bybit_funding)
# # print(bitget_funding)
# # print(mexc_funding)
# # print(kucoin_funding)
# # print(gate_funding)
# # print(no_kucoin_funding)
# set_all_symbols_funding = set().union(binance_funding, bybit_funding, bitget_funding, mexc_funding, no_kucoin_funding, gate_funding)
# # print(set_all_symbols_funding, len(set_all_symbols_funding))


# def get_data_binance(symbol):
#     print(symbol)
#
#
#
# symbols_map = extract_symbols_and_exchanges()
# print(symbols_map)
# def get_need_symbols():
#     for symbol, exchanges in symbols_map:
#         if 'binance' in exchanges:
#             get_data_binance(symbol)


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
    result = {}
    symbol_kucoin = symbol.replace('USDT', 'USDTM').replace('BTC', 'XBT')
    k = requests.get(KUCOIN_ORDER_BOOK, params={"symbol": symbol_kucoin}).json()
    d = requests.get(KUCOIN, params={"symbol": symbol_kucoin}).json()
    data = k['data']
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
print(collect_symbols_and_data)
#
#
#
#
# binance_data = get_data_binance(common_symbols)  # <class 'dict'>
# bybit_data = get_data_bybit(common_symbols)  # <class 'dict'>
# print(bybit_data)
# # bitget_data = get_data_bitget(common_symbols)  # <class 'dict'>
# coins_after_comparison = set(common_symbols) & binance_data.keys()  # Need for get real same symbols from Binance and Bybit <class 'set'>

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
