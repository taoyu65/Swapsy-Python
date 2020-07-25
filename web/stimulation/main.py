import pandas as pd

trade = pd.read_csv("db/trade 2020-07-25.csv", low_memory=False)
st = pd.read_csv('db/stimulation 2020-07-25csv.csv', low_memory=False)

trade['user_id'] = trade['seller_id']
trade = trade[['user_id', 'create_time', 'status']]
trade['create_time'] = pd.to_datetime(trade['create_time'], unit='s')
trade['create_time'] = trade['create_time'].dt.strftime('%Y-%m')
trade = trade[(trade['create_time'] > '2020-06')]

st = st[(st['user_group'] == 2001) & (st['coupon_id'] == 0)]

re = pd.merge(trade, st, how='inner', on=['user_id'])

come_back = re.drop_duplicates(subset='user_id', keep='first')
print("总共回来: ", come_back.count()[0])

come_back_finish_trade = re[re['status'] == 40]
come_back_finish_trade = come_back_finish_trade.drop_duplicates(subset='user_id', keep='first')
print("回来并且交易成功: ", come_back_finish_trade.count()[0])

print(come_back_finish_trade)
# print(re)
