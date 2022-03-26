import pandas as pd

# 仅仅有wechat收款的人
trans = pd.read_csv("../db/user_wallet 2022-02-23.csv", low_memory=False)

trans = trans[(trans['name'] == 'wxpay')]
# trans = trans[['user_id', 'create_time']]
# trans['create_time'] = pd.to_datetime(trans['create_time'], unit='s')
# trans['create_time'] = trans['create_time'].dt.strftime('%Y-%m')
# trans['count'] = 0
#
# source = trans.groupby(['create_time', 'user_id'])['count'].count().reset_index(name='recharge_count')
#
# # merge
# # todo : new records calculated and merge
#
# source.to_csv('csv/third.csv')
#

print(trans)