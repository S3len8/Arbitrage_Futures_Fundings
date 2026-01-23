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
                'binance': funding_A,
                'bybit': funding_B,
            }
    return result


funding = get_better_funding(binance_data, bybit_data)  # <class 'dict'>
print(funding)
for symbol, data in funding.items():
    print(symbol, data['binance'], data['bybit'])


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


middle_price = middle_price_exchanges(binance_data, bybit_data)
print(middle_price)


def entry_spread():
    result = {}
    for symbol in funding:
        funding_A = funding[symbol]['binance']
        funding_B = funding[symbol]['bybit']
        ask_A = float(middle_price[symbol]['askBinance'])
        bid_A = float(middle_price[symbol]['bidBinance'])
        ask_B = float(middle_price[symbol]['askBybit'])
        bid_B = float(middle_price[symbol]['bidBybit'])
        middle_price_A = middle_price[symbol]['middle price']
        if funding_A > 0:
            result[symbol] = ((ask_A - bid_B) / middle_price_A) * 100
        elif funding_A < 0:
            result[symbol] = ((ask_B - bid_A) / middle_price_A) * 100
    return result


def exit_spread():
    result = {}
    for symbol in funding:
        funding_A = funding[symbol]['binance']
        funding_B = funding[symbol]['bybit']
        ask_A = float(middle_price[symbol]['askBinance'])
        bid_A = float(middle_price[symbol]['bidBinance'])
        ask_B = float(middle_price[symbol]['askBybit'])
        bid_B = float(middle_price[symbol]['bidBybit'])
        middle_price_A = middle_price[symbol]['middle price']
        if funding_A > 0:
            result[symbol] = ((bid_A - ask_B) / middle_price_A) * 100
        elif funding_A < 0:
            result[symbol] = ((bid_B - ask_A) / middle_price_A) * 100
    return result


print(entry_spread())
print(exit_spread())
# def get_fees():
#     result = {}
#     for symbol in FEES:
#         if symbol in funding['exchanges']:
#             feeA = symbol['']
#             feeB = symbol['']
#             result = {
#                 'exchange:': symbol,
#                 'fee': symbol['']
#             }
#     return result
