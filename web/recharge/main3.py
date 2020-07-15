import numpy as np
import datetime as dt
import pandas as pd

# 平均lifetime value

trade = pd.read_csv("db/trade 2020-07-03.csv", low_memory=False)
credit_trans = pd.read_csv("db/credit_transaction 2020-07-05.csv", low_memory=False)

start_time = 1577862000     # 2020-01-01
end_time = 1593586800       # 2020-07-01

trade = trade[(trade['create_time'] > start_time) & (trade['create_time'] < end_time)]
trade = trade[trade['status'] == 40]
trade = trade[['seller_id']]
trade = trade.drop_duplicates(subset='seller_id', keep='first')
trade['user_id'] = trade['seller_id']
# result: 有交易的用户 5553
# print(trade)

credit_trans = credit_trans[(credit_trans['create_time'] < end_time)]

credit_trans = credit_trans[credit_trans['credit_rule_id'].isin([14, 19, 37])]
credit_trans = credit_trans[['user_id', 'credit_change']]
tem_index = credit_trans['user_id']
tem = pd.DataFrame({'credit_change': credit_trans['credit_change'].to_list()}, index=tem_index)
e = tem[tem['credit_change'] == 500]
e['usd'] = 5
a = tem[tem['credit_change'] == 1000]
a['usd'] = 9.9
b = tem[tem['credit_change'] == 2000]
b['usd'] = 18.9
c = tem[tem['credit_change'] == 5000]
c['usd'] = 44.9
d = tem[tem['credit_change'] == 20000]
d['usd'] = 169.9
tem = pd.concat([a, b, c, d, e])
# tem.to_csv('m.csv')
# print(tem)
# exit()
result = trade.merge(tem, on='user_id', how='left')

result = result.groupby('user_id')[['credit_change', 'usd']].sum()
# print(result)
# exit()
have_recharged_person_count = result[result['usd'] > 0]
print(have_recharged_person_count.count())
# 有充值用户总数: 4994

have_recharged_amount = result['usd'].sum()
print(have_recharged_amount)
# 有交易用户得充值总额: $497676

result.to_csv('csv/main3.csv')
