import pandas as pd
import numpy as np
import random

# 2020-05 (target_month) 月以后在也没回来的用户 (user_id 和 最后的buying_currency)

user = pd.read_csv("csv/main2.csv", low_memory=False)
trade = pd.read_csv("csv/main3.csv", low_memory=False)

# variable 需要计算
group_a_split = 133
group_b_split = 44

# db = pd.merge(user, trade, on='user_id', how='inner')
# user.set_index('user_id').join(trade, on='user_id')
db = user.merge(trade, how='left', on='user_id')
db = db[['user_id', 'buying_currency']]
cny = db[db['buying_currency'] == 'CNY']
usd = db[db['buying_currency'] == 'USD']
print(cny.count()[0])   # count: 115
print(usd.count()[0])   # count: 193
print('total: ', cny.count()[0] + usd.count()[0])
# getting final result
# Group A: (238 / 2 = 119 cny) + (193 / 2 = 96 usd) = 215
# Group B: (238 / 2 = 119 cny) + (193 / 2 = 97 usd) = 216

cny_list = list(cny['user_id'])
random.shuffle(cny_list)

usd_list = list(usd['user_id'])
random.shuffle(usd_list)

group_a = cny_list[:group_a_split] + usd_list[:group_b_split]
group_b = cny_list[group_a_split:] + usd_list[group_b_split:]

print(group_a)
print(group_b)

# print(cny)

# cny.to_csv('csv/main4_cny.csv')
# usd.to_csv('csv/main4_usd.csv')
