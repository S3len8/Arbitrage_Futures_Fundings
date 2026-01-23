from data import binance_data, bybit_data, coins_after_comparison, FEES


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


funding = get_better_funding(binance_data, bybit_data)  # <class 'dict'>
for symbol, data in funding.items():
    print(symbol, data['funding Binance:'], data['funding Bybit:'])


def middle_price_exchanges(binance: dict, bybit: dict):
    result = {}
    exchanges_data = binance.keys() & bybit.keys()
    for symbol in exchanges_data:
        askBinance = binance[symbol]['ask']
        bidBinance = binance[symbol]['bid']
        askBybit = bybit[symbol]['ask']
        bidBybit = bybit[symbol]['bid']
        if symbol in funding:
            middle_price = (askBinance + bidBinance + askBybit + bidBybit) / 4
            result[symbol] = {
                'symbol': symbol,
                'askBinance': float(askBinance),
                'bidBinance': float(bidBinance),
                'askBybit': float(askBybit),
                'bidBybit': float(bidBybit),
                'middle price': float(middle_price),
            }
    return result


def get_fees():
    result = {}
    for symbol in FEES:
        if symbol in funding['exchanges']:
            feeA = symbol['']
            feeB = symbol['']
            result = {
                'exchange:': symbol,
                'fee': symbol['']
            }
    return result


print(middle_price_exchanges(binance_data, bybit_data))