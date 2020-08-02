import pandas as pd

trade = pd.read_csv("db/trade part_2020-07.csv", low_memory=False)

trade['user_id'] = trade['seller_id']
trade = trade[['user_id', 'create_time', 'status', 'buying_currency', 'buying_amount']]
trade['create_time'] = pd.to_datetime(trade['create_time'], unit='s')
trade['create_time'] = trade['create_time'].dt.strftime('%Y-%m')
trade = trade[(trade['create_time'] >= '2020-07')]
trade = trade[trade['status'] == 40]

print('2020-07 已经成功交易')
# CNY -> USD
trade1 = trade[trade['buying_currency'] == 'USD']
print("CNY换USD 笔数: ", trade1.count()[0], '笔')
print("CNY换USD 总量: $", trade1.sum()['buying_amount'])

# USD -> CNY
trade2 = trade[trade['buying_currency'] == 'CNY']
cny_amount = trade2.sum()['buying_amount']
print("USD换CNY 笔数: ", trade2.count()[0], '笔')
print("USD换CNY 总量: ¥", cny_amount, '($', int(cny_amount/7), ')')

# print(re)
