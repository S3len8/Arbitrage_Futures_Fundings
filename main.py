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