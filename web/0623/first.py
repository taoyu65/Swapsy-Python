import pandas as pd

# 生成新csv
trade = pd.read_csv("../../db/new/trade.csv", low_memory=False)
# trade_part1 = pd.read_csv("db/trade 2020-07-03 to 2020-09-07.csv", low_memory=False)
# trade = trade.append(trade_part1)

trade = trade[trade['is_chain_version'] == 1]
trade['create_time'] = pd.to_datetime(trade['create_time'], unit='s')
trade['create_time'] = trade['create_time'].dt.strftime('%Y-%m')    # 或者 dt.year / dt.month / dt.day / dt.data
trade = trade.drop(['id', 'uuid', 'uuid_old', 'expire_time', 'update_time', 'is_from_old', 'is_puppet', 'rate_up', 'rate_down'], axis=1)
trade = trade[trade['create_time'] >= '2019-06']
source = trade[['seller_id', 'create_time', 'status']]
source = source[source['status'] == 40]

source = source.groupby(['create_time', 'seller_id']).count()
# source['less3'] = source[source['status'] < 3]
# print(source.head())
#
source.to_csv('csv/first.csv')
# print(source)
