import pandas as pd
# 换人民币超过5万 10万 20万 50万的用户数

trade = pd.read_csv("../../db/new/trade 3-8.csv", low_memory=False)

trade['user_id'] = trade['seller_id']
trade = trade[['user_id', 'create_time', 'status', 'buying_currency', 'buying_amount']]
# trade['create_time'] = pd.to_datetime(trade['create_time'], unit='s')
# trade['create_time'] = trade['create_time'].dt.strftime('%Y-%m')
# trade = trade[(trade['create_time'] >= '2020-07')]
trade = trade[trade['status'] == 40]

# 需求人民币的
trade1 = trade[trade['buying_currency'] == 'CNY']
trade1 = trade1.groupby(['user_id'])['buying_amount'].sum()
trade1.to_csv('csv/need_cny.csv')
print("f")

# 需求美元的
trade2 = trade[trade['buying_currency'] == 'USD']
trade2 = trade2.groupby(['user_id'])['buying_amount'].sum()
trade2.to_csv('csv/need_usd.csv')
print(trade2)


# 第二步 main2
