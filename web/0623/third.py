import pandas as pd

# 生成新csv - recharge view
db = pd.read_csv("db/credit_transaction 2020-07-05.csv", low_memory=False)
db = db[(db['credit_rule_id'] == 14) | (db['credit_rule_id'] == 19)]
db = db[['user_id', 'create_time']]
db['create_time'] = pd.to_datetime(db['create_time'], unit='s')
db['create_time'] = db['create_time'].dt.strftime('%Y-%m')
db['count'] = 0

source = db.groupby(['create_time', 'user_id'])['count'].count().reset_index(name='recharge_count')

# merge
# todo : new records calculated and merge

source.to_csv('csv/third.csv')

