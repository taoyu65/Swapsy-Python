import pandas as pd

trade = pd.read_csv("db/trade part_2020-07.csv", low_memory=False)
permission = pd.read_csv("db/administrator_operation_log 2020-08-02.csv", low_memory=False)

trade['user_id'] = trade['seller_id']
trade = trade[['user_id', 'create_time', 'status', 'buying_currency', 'buying_amount']]
trade['create_time'] = pd.to_datetime(trade['create_time'], unit='s')
trade['create_time'] = trade['create_time'].dt.strftime('%Y-%m')
trade = trade[(trade['create_time'] >= '2020-07')]

trade1 = trade[trade['status'] == 60].count()[0]
print("自动cancel总条数: ", trade1, '-80=', trade1-80)

trade2 = trade[trade['status'] == 60]
trade2 = trade2.drop_duplicates(subset='user_id', keep='first').count()[0]
permission = permission[permission['logged_user_id'] > 0]
permission['create_time'] = pd.to_datetime(permission['create_time'], unit='s')
permission['create_time'] = permission['create_time'].dt.strftime('%Y-%m')
permission = permission[permission['create_time'] >= '2020-07']
permission = permission[permission['index'] == 'mark-expire']
permission = permission.drop_duplicates(subset='logged_user_id', keep='first')
permission = permission.count()[0]
print("后台手动mark to expire人数: ", permission)
print("自动cancel人数: ", trade2, '-', permission, '=', trade2-permission)

print("自动cancel总条数: ", trade1-80)
print("自动cancel人数: ", trade2-permission)



