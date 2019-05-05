import pandas as pd
from pandas import np


def volatility(filename):
    hist_data = pd.read_csv(filename)
    quotes = hist_data['close']
    logreturns = np.log(quotes / quotes.shift(1))
    vol = np.sqrt(252 * logreturns.var())
    return vol


if __name__ == '__main__':
    filename = 'data/000004.csv'
    vol = volatility(filename)
    print(vol)
