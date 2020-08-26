import pandas as pd

# 日期1 到 日期2 之前注册的用户 并且没有任何交易的.

user = pd.read_csv("db/user 08-01 to 08-15.csv", low_memory=False)
trade = pd.read_csv("db/trade 08-01 to 08-15.csv", low_memory=False)

trade['user_id'] = trade['seller_id']
trade = trade.groupby('user_id')['id'].count()

user['user_id'] = user['id']
user = user[['user_id', 'create_time']]

all_kind = user.merge(trade, on='user_id', how='left')

print(all_kind)
all_kind.to_csv('csv/all.csv')

all_kind['id'] = all_kind['id'].fillna(0)
no_trade = all_kind[all_kind['id'] == 0]

no_trade['user_id'].to_csv('csv/no_trade.csv')
