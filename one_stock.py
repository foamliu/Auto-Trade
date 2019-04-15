import datetime
import os

import pandas as pd
import tushare as ts
from fbprophet import Prophet
from pandas.plotting import register_matplotlib_converters

formatter = lambda x: "%.2f" % x

register_matplotlib_converters()
from utils import suppress_stdout_stderr

threshold = 0.05


def workdays(d, end, excluded=(6, 7)):
    days = []
    while d.date() <= end.date():
        if d.isoweekday() not in excluded:
            days.append(d.strftime('%Y-%m-%d'))
        d += datetime.timedelta(days=1)
    return days


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

    date_range = workdays(datetime.datetime(2017, 4, 15), datetime.datetime(2019, 4, 15))
    prev_date = '2017-04-14'
    row = df[df['ds'] == prev_date]
    prev_y = row.iloc[0]['y']

    net_profit = 0

    print('date\tratio\tprev_y\tyhat\ty\tprofit\tnet_profit')
    for d in date_range:
        if d in df['ds'].unique():
            data = df[df['ds'] < d]
            count = data['ds'].count()
            row = df[df['ds'] == d]
            if row['ds'].count() > 0:
                y = row.iloc[0]['y']

                with suppress_stdout_stderr():
                    m = Prophet()
                    m.fit(data)
                    future = m.make_future_dataframe(periods=10)
                    forecast = m.predict(future)

                row = forecast[forecast['ds'] == d]
                yhat = row.iloc[0]['yhat']

                ratio = (yhat - prev_y) / prev_y
                if ratio > threshold:
                    profit = 10000 * (y / prev_y - 1)
                    net_profit += profit
                    print('{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(d, ratio, prev_y, formatter(yhat), y, formatter(profit),
                                                              formatter(net_profit)))

                prev_y = y
