from data import binance_data, bybit_data, coins_after_comparison


def get_better_funding(binance: dict, bybit: dict) -> dict:
    result = {}
    for key in coins_after_comparison:
        funding_A = (binance[key]['funding']) * 100
        funding_B = (bybit[key]['funding']) * 100
        if not funding_A or not funding_B:
            print(f'{key} ❌ нет данных')
            continue

        if (0.1 >= funding_A and -0.1 >= funding_A) or (0.1 >= funding_B and -0.1 >= funding_B):
            result[key] = {
                'binance': binance[key],
                'bybit': bybit[key],
                'funding Binance:': funding_A,
                'funding Bybit:': funding_B,
            }
    return result
    # print(common_symbols)
    # print(type(common_symbols))
    # print(len(common_symbols))


print(-0.02 < -0.01)
funding = get_better_funding(binance_data, bybit_data)
print(funding)
for symbol, data in funding.items():
    print(symbol, data['funding Binance:'], data['funding Bybit:'])