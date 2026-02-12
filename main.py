from data import collect_symbols_and_data
from funding import better_funding
from symbol import FEES


def better_funding_symbols():
    result = {}

    for _, symbols in better_funding.items():
        for symbol, exchanges in symbols.items():

            # 1. funding
            fundings = {
                ex: f for ex, f in exchanges.items()
                if f is not None
            }

            if len(fundings) < 2:
                continue

            # Sorting funding in abs
            sorted_fundings = sorted(fundings.items(), key=lambda x: abs(x[1]))

            small_ex, small_f = sorted_fundings[0]
            big_ex, big_f = sorted_fundings[-1]

            abs_small = abs(small_f)
            abs_big = abs(big_f)

            # Spread between small funding and big funding
            if (small_f > 0 and big_f < 0) or (small_f < 0 and big_f > 0):
                spread = abs_big + abs_small
            else:
                spread = abs_big - abs_small

            # Collect all data from dict
            symbol_data = collect_symbols_and_data.get(symbol)
            if not symbol_data:
                continue

            def get_market(exchange):
                ex_data = symbol_data.get(exchange)
                if not ex_data:
                    return None
                market = ex_data.get(symbol)
                return market

            small_market = get_market(small_ex)
            big_market = get_market(big_ex)

            # If one coin haven`t orderbook
            if not small_market or not big_market:
                continue

            # Result
            result[symbol] = {
                'small_exchange': small_ex,
                'small_funding': small_f,
                'small_bid': small_market['bid'],
                'small_ask': small_market['ask'],
                'small_volume_24H': small_market['volume 24H'],

                'big_exchange': big_ex,
                'big_funding': big_f,
                'big_bid': big_market['bid'],
                'big_ask': big_market['ask'],
                'big_volume_24H': big_market['volume 24H'],

                'funding_spread': spread,
            }

    return result


better_funding_symbols = better_funding_symbols()
# print(better_funding_symbols)


def middle_price_exchanges():
    result = {}
    for symbol, value in better_funding_symbols.items():  # Get symbols from data
        small_bid = value['small_bid']
        small_ask = value['small_ask']
        big_bid = value['big_bid']
        big_ask = value['big_ask']
        middle_price = (small_bid + small_ask + big_bid + big_ask) / 4
        result[symbol] = {
            'symbol': symbol,
            'middle price': float(middle_price),
        }
    return result


middle_price = middle_price_exchanges()
# print(middle_price)


def entry_spread():
    result = {}
    for symbol, value in better_funding_symbols.items():
        smallFunding = value['small_funding']
        bigFunding = value['big_funding']
        small_bid = value['small_bid']
        small_ask = value['small_ask']
        big_bid = value['big_bid']
        big_ask = value['big_ask']
        middle_price_EntrySpread = (big_ask + big_bid + small_ask + small_bid) / 4
        if bigFunding > 0:
            result[symbol] = ((small_ask - big_bid) / middle_price_EntrySpread) * 100
        elif bigFunding < 0:
            result[symbol] = ((big_ask - small_bid) / middle_price_EntrySpread) * 100
    return result


def exit_spread():
    result = {}
    for symbol, value in better_funding_symbols.items():
        smallFunding = value['small_funding']
        bigFunding = value['big_funding']
        small_bid = value['small_bid']
        small_ask = value['small_ask']
        big_bid = value['big_bid']
        big_ask = value['big_ask']
        middle_price_EntrySpread = (big_ask + big_bid + small_ask + small_bid) / 4
        if bigFunding > 0:
            result[symbol] = ((small_bid - big_ask) / middle_price_EntrySpread) * 100
        elif bigFunding < 0:
            result[symbol] = ((big_bid - small_ask) / middle_price_EntrySpread) * 100
    return result


entry_Spread = entry_spread()
exit_Spread = exit_spread()
# print(entry_Spread)
# print(exit_Spread)


# This function must calculation fees from two exchanges, like Binance/Bybit, MEXC/Bitget or something like this
def get_fees():
    result = {}
    fees_lower = {exchange.lower(): fees for exchange, fees in FEES.items()}
    for symbol, v in better_funding_symbols.items():
        exchangeSmall = v['small_exchange'].lower()
        exchangeBig = v['big_exchange'].lower()
        for exchange in (exchangeSmall, exchangeBig):  # Get exchange fees and after get maker/taker fee
            if exchange in fees_lower:
                result[symbol] = {
                    f'maker fee small_exchange': fees_lower[exchange]['maker:'],
                    f'taker fee small_exchange': fees_lower[exchange]['taker:'],
                    f'maker fee big_exchange': fees_lower[exchange]['maker:'],
                    f'taker fee big_exchange': fees_lower[exchange]['taker:'],
                }
    return result


get_fees = get_fees()
# print(get_fees)


def pnl():
    result = {}
    for (kEnrty, vEntry), (kExit, vExit) in zip(entry_Spread.items(), exit_Spread.items()):
        result[kEnrty] = vExit - vEntry
    return result


pnl_exit_entry = pnl()
print(pnl_exit_entry)


def funding_profit():
    result = {}
    for k, v in better_funding_symbols.items():
        pnl = pnl_exit_entry.get(k, {})
        dict_fees = get_fees.get(k, {})
        fees_small_exchange = dict_fees['taker fee small_exchange']
        fees_big_exchange = dict_fees['taker fee big_exchange']
        fees = fees_small_exchange + fees_big_exchange
        spread = v['funding_spread']
        funding_profit = spread - 2*fees + pnl
        result[k] = {
            'Profit': funding_profit,
        }
    return result


funding_profit = funding_profit()
print(funding_profit)


def print_function():
    result = {}
    for k, v in better_funding_symbols.items():
        profitFunding = funding_profit.get(k, {})['Profit']
        if profitFunding > 0.6:
            result[k] = {
                'Small_exchange': v['small_exchange'],
                'Small_ask': v['small_ask'],
                'Small_bid': v['small_bid'],
                'Small_volume_24H': v['small_volume_24H'],
                'Big_exchange': v['big_exchange'],
                'Big_ask': v['big_ask'],
                'Big_bid': v['big_bid'],
                'Big_volume_24H': v['big_volume_24H'],
                'Funding_spread': v['funding_spread'],
                'Profit': profitFunding,
            }
    return result


print_function = print_function()
print(print_function)