import pandas as pd
import numpy as np

# 生成新csv
trans = pd.read_csv("db/credit_transaction 2020-07-05.csv", low_memory=False)

# 1577862000 = 2020-01-01 PDT
trans = trans[(trans['create_time'] > 1577862000) & (trans['credit_rule_id'].isin([19, 37]))]

trans = trans[['user_id', 'credit_rule_id', 'credit_change', 'create_time']]

trans['create_time'] = pd.to_datetime(trans['create_time'], unit='s')
trans['create_time'] = trans['create_time'].dt.strftime('%Y-%m')    # 或者 dt.year / dt.month / dt.day / dt.data

trans['is_credit_card'] = np.where(trans['credit_rule_id'] == 37, 1, 0)

a = trans[trans['credit_change'] == 1000]
a['usd'] = 9.9
a['usd10'] = 9.9
b = trans[trans['credit_change'] == 2000]
b['usd'] = 18.9
b['usd20'] = 18.9
c = trans[trans['credit_change'] == 5000]
c['usd'] = 44.9
c['usd50'] = 44.9
d = trans[trans['credit_change'] == 20000]
d['usd'] = 169.9
d['usd200'] = 169.9

db = pd.concat([a, b, c, d])

db['usd10'].fillna(0, inplace=True)
db['usd20'].fillna(0, inplace=True)
db['usd50'].fillna(0, inplace=True)
db['usd200'].fillna(0, inplace=True)

db.to_csv('csv/main.csv')

