import pickle

import tushare as ts
from tqdm import tqdm

if __name__ == '__main__':
    result = dict()

    with open('stock_basic.csv', encoding='utf-8') as file:
        lines = file.readlines()

    for line in tqdm(lines[1:]):
        code = line.split(',')[0].strip()
        df = ts.get_hist_data(code)
        result[code] = df

    with open('data/hist_data.pickle', 'wb') as file:
        pickle.dump(result, file)
