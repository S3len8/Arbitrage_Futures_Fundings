from data import FEES, set_all_symbols_funding, binance_funding, bybit_funding, bitget_funding, mexc_funding, no_kucoin_funding, gate_funding


# Function get funding from binance and bybit in set coins_after_comparison
def get_funding(binance: dict, bybit: dict, bitget: dict, mexc: dict, kucoin: dict, gate: dict) -> dict:
    result = {
        6: {},  # Coin in 6
        5: {},  # Coin in 5
        4: {},  # Coin in 4
        3: {},  # Coin in 3
        2: {},  # Coin in 2
        1: {},  # Coin in 1
    }  # <class 'dict'>
    for symbol in set_all_symbols_funding:
        exchanges = {}
        if symbol in binance and binance[symbol].get('funding') is not None:  # Getting and calculation funding in percent from Binance
            funding = binance[symbol]['funding'] * 100
            exchanges['binance'] = funding

        if symbol in bybit and bybit[symbol].get('funding') is not None:  # Getting and calculation funding in percent from Bybit
            funding = bybit[symbol]['funding'] * 100
            exchanges['bybit'] = funding

        if symbol in bitget and bitget[symbol].get('funding') is not None:  # Getting and calculation funding in percent from Bitget
            funding = bitget[symbol]['funding'] * 100
            exchanges['bitget'] = funding

        if symbol in mexc and mexc[symbol].get('funding') is not None:  # Getting and calculation funding in percent from Mexc
            funding = mexc[symbol]['funding'] * 100
            exchanges['mexc'] = funding

        if symbol in kucoin and isinstance(kucoin[symbol], dict) and kucoin[symbol].get('funding') is not None:  # Getting and calculation funding in percent from Kucoin
            funding = kucoin[symbol]['funding'] * 100
            exchanges['kucoin'] = funding

        if symbol in gate and gate[symbol].get('funding') is not None:  # Getting and calculation funding in percent from Gate
            funding = gate[symbol]['funding'] * 100
            exchanges['gate'] = funding
        count = len(exchanges)

        if count == 0:
            continue

        result[count][symbol] = exchanges

    return result


funding = get_funding(binance_funding, bybit_funding, bitget_funding, mexc_funding, no_kucoin_funding, gate_funding)  # <class 'dict'>
print(funding)
for key in [6, 5, 4, 3, 2, 1]:
    print(f"{key} exchanges: {funding.get(key)}")


def get_better_funding():
    result = {}
    for count, symbols in funding.items():
        filtered_symbols = {}
        for symbol, exchanges in symbols.items():
            if any(abs(funding) >= 0.2 for funding in exchanges.values()):
                filtered_symbols[symbol] = exchanges

        if filtered_symbols:
            result[count] = filtered_symbols

    return result


better_funding = get_better_funding()  # <class 'dict'>
print(better_funding)


# def middle_price_exchanges(binance: dict, bybit: dict):
#     result = {}
#     exchanges_data = binance.keys() & bybit.keys()  # Unite keys from exchanges <class 'set'>
#     for symbol in exchanges_data:  # Get symbols from data
#         askBinance = binance[symbol]['ask']
#         bidBinance = binance[symbol]['bid']
#         askBybit = bybit[symbol]['ask']
#         bidBybit = bybit[symbol]['bid']
#         if symbol in funding:  # Checking availability symbols in funding
#             middle_price = (askBinance + bidBinance + askBybit + bidBybit) / 4
#             result[symbol] = {
#                 'symbol': symbol,
#                 'askBinance': float(askBinance),
#                 'bidBinance': float(bidBinance),
#                 'askBybit': float(askBybit),
#                 'bidBybit': float(bidBybit),
#                 'middle price': float(middle_price),
#             }
#     return result
#
#
# middle_price = middle_price_exchanges(binance_data, bybit_data)
# print(middle_price)
#
#
# def entry_spread():
#     result = {}
#     for symbol in funding:
#         funding_A = funding[symbol]['binance']
#         funding_B = funding[symbol]['bybit']
#         ask_A = float(middle_price[symbol]['askBinance'])
#         bid_A = float(middle_price[symbol]['bidBinance'])
#         ask_B = float(middle_price[symbol]['askBybit'])
#         bid_B = float(middle_price[symbol]['bidBybit'])
#         middle_price_A = middle_price[symbol]['middle price']
#         if funding_A > 0:
#             result[symbol] = ((ask_A - bid_B) / middle_price_A) * 100
#         elif funding_A < 0:
#             result[symbol] = ((ask_B - bid_A) / middle_price_A) * 100
#     return result
#
#
# def exit_spread():
#     result = {}
#     for symbol in funding:
#         funding_A = funding[symbol]['binance']
#         funding_B = funding[symbol]['bybit']
#         ask_A = float(middle_price[symbol]['askBinance'])
#         bid_A = float(middle_price[symbol]['bidBinance'])
#         ask_B = float(middle_price[symbol]['askBybit'])
#         bid_B = float(middle_price[symbol]['bidBybit'])
#         middle_price_A = middle_price[symbol]['middle price']
#         if funding_A > 0:
#             result[symbol] = ((bid_A - ask_B) / middle_price_A) * 100
#         elif funding_A < 0:
#             result[symbol] = ((bid_B - ask_A) / middle_price_A) * 100
#     return result
#
#
# print(entry_spread())
# print(exit_spread())
#
#
# # This function must calculation fees from two exchanges, like Binance/Bybit, MEXC/Bitget or something like this
# def get_fees():
#     result = {}
#     for exchange, key in FEES.items():  # Get exchange fees and after get maker/taker fee
#         result[exchange] = {
#             'maker fee': key['maker:'],
#             'taker fee': key['taker:'],
#         }
#     return result
#
#
# print(get_fees())