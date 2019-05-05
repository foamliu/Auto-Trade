import pickle

from pandas import np


def volatility(df):
    quotes = df['close']
    logreturns = np.log(quotes / quotes.shift(1))
    vol = np.sqrt(252 * logreturns.var())
    return vol


if __name__ == '__main__':
    with open('data/hist_data.pickle', 'rb') as file:
        data = pickle.load(file)

    code_vol_list = []

    for code in data.keys():
        df = data[code]
        if df is None:
            print(code)
            continue
        vol = volatility(df)
        code_vol_list.append((code, vol))

    sorted_by_vol = sorted(code_vol_list, key=lambda tup: tup[1], reverse=True)

    lines = []
    for tup in sorted_by_vol:
        lines.append('{}\t{}\n'.format(tup[0], tup[1]))

    with open('data/volatility.txt', 'w') as file:
        file.writelines(lines)
