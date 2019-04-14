import tushare as ts
from fbprophet import Prophet

# print(ts.get_hs300s())

hist_data = ts.get_hist_data('600848')

print(hist_data['close'])
print(hist_data)

m = Prophet()
m.fit(hist_data['close'])
