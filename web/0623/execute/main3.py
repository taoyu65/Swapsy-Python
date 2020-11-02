import pandas as pd
import numpy as np

# 处理 trade 表. 拿到2020-01月用户买入币种
trade = pd.read_csv("../db/trade 2020-11-02.csv", low_memory=False)
# trade_part1 = pd.read_csv("../db/trade 2020-07-03 to 2020-09-07.csv", low_memory=False)
# trade = trade.append(trade_part1)

# variable
target_month = '2020-05'

trade['create_time'] = pd.to_datetime(trade['create_time'], unit='s')
trade['create_time'] = trade['create_time'].dt.strftime('%Y-%m')    #
trade['user_id'] = trade['seller_id']

trade = trade[trade['create_time'] == target_month]

trade = trade[['user_id', 'create_time', 'buying_currency']]
trade = trade.drop_duplicates(subset='user_id', keep='first')
print(trade)
# count: 2308

trade.to_csv('csv/main3.csv')
