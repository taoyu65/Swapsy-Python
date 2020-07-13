import pandas as pd
import numpy as np

user = pd.read_csv("csv/main2.csv", low_memory=False)
trade = pd.read_csv("csv/main3.csv", low_memory=False)

# 2020-01 月以后在也没回来的用户 (user_id 和 最后的buying_currency)

# db = pd.merge(user, trade, on='user_id', how='inner')
# user.set_index('user_id').join(trade, on='user_id')
db = user.merge(trade, how='left')
db = db[['user_id', 'buying_currency']]

cny_amount = db[db['buying_currency'] == 'CNY'].count()[0]
usd_amount = db[db['buying_currency'] == 'USD'].count()[0]
print(cny_amount)   # count: 238
print(usd_amount)   # count: 193

db.to_csv('csv/main4.csv')
