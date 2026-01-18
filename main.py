from data import common


def funding_filter():
    result = {}
    for symbol, v in common:
        # Getting funding only better than 1 or -1
        if not -1 < v['funding'] < 1:
            result[symbol] = {
                'ask': v['ask'],
                'bid': v['bid'],
                'funding': v['funding'],
            }

    return result


funding_filter()