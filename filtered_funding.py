from main import better_funding


def extract_symbols_and_exchanges(data: dict) -> dict:
    """
    Return:
    {
        'NAORISUSDT': ['binance', 'bybit', 'bitget', 'mexc', 'kucoin', 'gate'],
        'APRUSDT':    ['binance', 'bybit', 'bitget', 'mexc', 'kucoin', 'gate']
    }
    """
    result = {}

    for _, symbols in data.items():
        for symbol, exchanges in symbols.items():
            result[symbol] = list(exchanges.keys())

    return result


symbols_map = extract_symbols_and_exchanges(better_funding)
print(symbols_map)

for symbol, exchanges in symbols_map.items():
    print(symbol, exchanges)