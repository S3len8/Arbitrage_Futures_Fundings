from data import binance_data, bybit_data, coins_after_comparison


# Function get funding from binance and bybit in set coins_after_comparison
def get_better_funding(binance: dict, bybit: dict) -> dict:
    result = {}  # <class 'dict'>
    for key in coins_after_comparison:
        funding_A = (binance[key]['funding']) * 100  # Getting and calculation funding in percent from Binance
        funding_B = (bybit[key]['funding']) * 100  # Getting and calculation funding in percent from Bybit
        if not funding_A or not funding_B:
            print(f'{key} ❌ нет данных')
            continue
        # Filter for getting necessary funding percent from exchanges
        if (0.1 >= funding_A and -0.1 >= funding_A) or (0.1 >= funding_B and -0.1 >= funding_B):
            result[key] = {
                'binance': binance[key],
                'bybit': bybit[key],
                'funding Binance:': funding_A,
                'funding Bybit:': funding_B,
            }
    return result


funding = get_better_funding(binance_data, bybit_data)
for symbol, data in funding.items():
    print(symbol, data['funding Binance:'], data['funding Bybit:'])


print(type(binance_data))
print(binance_data)


def middle_price_binance(binance: dict):
    result = {}
    for symbol in binance:
        ask = binance[symbol]['ask']
        bid = binance[symbol]['bid']
        if symbol in funding:
            result = {
                'binance: ': 'Binance',
                'symbol': symbol,
                'ask': float(ask),
                'bid': float(bid),
            }
    return result


def middle_price_bybit(bybit: dict):
    result = {}
    for symbol in bybit:
        ask = bybit[symbol]['ask']
        bid = bybit[symbol]['bid']
        if symbol in funding:
            result = {
                'binance: ': 'Bybit',
                'symbol': symbol,
                'ask': float(ask),
                'bid': float(bid),
            }
    return result


print(middle_price_binance(binance_data))
print(middle_price_bybit(bybit_data))