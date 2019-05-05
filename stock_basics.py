import tushare as ts

if __name__ == '__main__':
    df = ts.get_stock_basics()
    df.to_csv('data/stock_basic.csv')
