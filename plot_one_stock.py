import datetime
import os
import matplotlib.pyplot as plt
import pandas as pd
import tushare as ts
from utils import workdays


if __name__ == '__main__':
    pickle_file = '600848_daily.pickle'
    if os.path.isfile(pickle_file):
        df = pd.read_pickle(pickle_file)
    else:
        hist_data = ts.get_hist_data('600848')

        ds = hist_data.index.values[::-1]
        y = hist_data['close'].values[::-1]
        df = pd.DataFrame(list(zip(ds, y)), columns=['ds', 'y'])
        df.to_pickle(pickle_file)
        print(df.head())

    date_range = workdays(datetime.datetime(2018, 4, 15), datetime.datetime(2019, 4, 15))
    df = df[df['ds'] > '2018-04-15']
    lines = df.plot(kind='line', x='ds', y='y')
    plt.show()