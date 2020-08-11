import pandas as pd

# 生成新csv - recharge view
trans = pd.read_csv("db/credit_transaction 2020-07-05.csv", low_memory=False)
trans_part1 = pd.read_csv("db/credit_transaction 2020-07-05 to 2020-08-11.csv", low_memory=False)
trans = trans.append(trans_part1)

trans = trans[(trans['credit_rule_id'] == 14) | (trans['credit_rule_id'] == 19)]
trans = trans[['user_id', 'create_time']]
trans['create_time'] = pd.to_datetime(trans['create_time'], unit='s')
trans['create_time'] = trans['create_time'].dt.strftime('%Y-%m')
trans['count'] = 0

source = trans.groupby(['create_time', 'user_id'])['count'].count().reset_index(name='recharge_count')

# merge
# todo : new records calculated and merge

source.to_csv('csv/third.csv')

