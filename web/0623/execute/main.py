import pandas as pd
import numpy as np

# 生成新csv
db1 = pd.read_csv("../csv/second.csv", low_memory=False)
db2 = pd.read_csv("../csv/third.csv", low_memory=False)

db1['user_id'] = db1['seller_id']
db = pd.merge(db1, db2, on=['create_time', 'user_id'], how='left')
db['recharge_count'].fillna(0, inplace=True)
db['recharge_count'] = db['recharge_count'].astype(int)

db = db[db['create_time'] == '2020-01']
db = db[db['less_than_3'] > 0]
db = db[db['recharge_count'] == 0]
db = db[['user_id']]
db['user_id'] = db['user_id'].astype(int)

db1 = db1[db1['create_time'] > '2020-01']
# 计算 2020-01以后 有几个整月 有交易. eg: 2代表 2020-01后 有2个月 有交易
db['count'] = 0

for index, row in db.iterrows():
    row['count'] = db1[db1['user_id'] == row['user_id']].count()[0]

print(db)
db.to_csv('csv/main.csv')
# trade = trade[trade['is_chain_version'] == 1]
# trade['create_time'] = pd.to_datetime(trade['create_time'], unit='s')
# trade['create_time'] = trade['create_time'].dt.strftime('%Y-%m')    # 或者 dt.year / dt.month / dt.day / dt.data
# trade = trade.drop(['id', 'uuid', 'uuid_old', 'expire_time', 'update_time', 'is_from_old', 'is_puppet', 'rate_up', 'rate_down'], axis=1)
#
# source = trade[['seller_id', 'create_time', 'status']]
# source = source[source['status'] == 40]
#
# source = source.groupby(['create_time', 'seller_id']).count()
# # source['less3'] = source[source['status'] < 3]
# # print(source.head())
# #
# source.to_csv('csv/first.csv')
# print(source)
