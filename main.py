from data import common


def funding_filter():
    result = {}
    for symbol, v in common.items():
        binance_funding = common
        # Getting funding only better than 1 or -1
        if not -0.01 < v['funding'] < 0.01:
            result[symbol] = {
                'ask': v['ask'],
                'bid': v['bid'],
                'funding': v['funding'],
            }

    return result


funding_filter()