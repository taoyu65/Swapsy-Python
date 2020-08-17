import numpy as np
import datetime as dt
import pandas as pd

# 平均lifetime value

# variable
start_time = 1546326000     # 2019-01-01
end_time = 1597682736       # 2020-08-17

trade = pd.read_csv("db/trade 2020-07-03.csv", low_memory=False)
credit_trans = pd.read_csv("db/credit_transaction 2020-07-05.csv", low_memory=False)
part_trade = pd.read_csv("db/part trade 07-03 to 08-17.csv", low_memory=False)
part_credit_trans = pd.read_csv("db/part credit_transaction 07-05 to 08-17.csv", low_memory=False)
trade = trade.append(part_trade)
credit_trans = credit_trans.append(part_credit_trans)

trade = trade[(trade['create_time'] > start_time) & (trade['create_time'] < end_time)]
trade = trade[trade['status'] == 40]
trade = trade[['seller_id']]
trade = trade.drop_duplicates(subset='seller_id', keep='first')
trade['user_id'] = trade['seller_id']
# result: 有交易的用户 10870
print('有交易的用户', trade.count()[0])

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
print('有充值用户总数', have_recharged_person_count.count()[0])
# 有充值用户总数: 7954

have_recharged_amount = result['usd'].sum()
print('有交易用户得充值总额', have_recharged_amount)
# 有交易用户得充值总额: $622486

result.to_csv('csv/main3.csv')
