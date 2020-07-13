import pandas as pd
import numpy as np

# 处理 trade 表. 拿到2020-01月用户买入币种
trade = pd.read_csv("../db/trade 2020-07-03.csv", low_memory=False)
trade['create_time'] = pd.to_datetime(trade['create_time'], unit='s')
trade['create_time'] = trade['create_time'].dt.strftime('%Y-%m')    #
trade['user_id'] = trade['seller_id']

trade = trade[trade['create_time'] == '2020-01']

trade = trade[['user_id', 'create_time', 'buying_currency']]
trade = trade.drop_duplicates(subset='user_id', keep='first')

trade.to_csv('csv/main3.csv')
