import pandas as pd
# 换人民币超过5万 10万 20万 50万的用户数

trade_need_cny = pd.read_csv("csv/need_cny.csv", low_memory=False)
trade_need_usd = pd.read_csv("csv/need_usd.csv", low_memory=False)

# 超过5万人们币
trade1 = trade_need_cny[trade_need_cny['buying_amount'] > 50000]
print("超过5万人们币的总数: ", trade1.count()['user_id'], " 平均值: ", trade1['buying_amount'].mean().round())
trade1.to_csv('csv/result_need_cny_1.csv')

# 超过10万人们币
trade2 = trade_need_cny[trade_need_cny['buying_amount'] > 100000]
print("超过10万人们币的总数: ", trade2.count()['user_id'], " 平均值: ", trade2['buying_amount'].mean().round())
trade2.to_csv('csv/result_need_cny_2.csv')

# 超过20万人们币
trade3 = trade_need_cny[trade_need_cny['buying_amount'] > 200000]
print("超过20万人们币的总数: ", trade3.count()['user_id'], " 平均值: ", trade3['buying_amount'].mean().round())
trade3.to_csv('csv/result_need_cny_3.csv')

# 超过50万人们币
trade4 = trade_need_cny[trade_need_cny['buying_amount'] > 500000]
print("超过50万人们币的总数: ", trade4.count()['user_id'], " 平均值: ", trade4['buying_amount'].mean().round())
trade4.to_csv('csv/result_need_cny_4.csv')


# 超过1万美金
trade1 = trade_need_usd[trade_need_usd['buying_amount'] > 10000]
print("超过1万美金的总数: ", trade1.count()['user_id'], " 平均值: ", trade1['buying_amount'].mean().round())
trade1.to_csv('csv/result_need_usd_1.csv')

# 超过2万美金
trade2 = trade_need_usd[trade_need_usd['buying_amount'] > 20000]
print("超过2万美金的总数: ", trade2.count()['user_id'], " 平均值: ", trade2['buying_amount'].mean().round())
trade2.to_csv('csv/result_need_usd_2.csv')

# 超过5万美金
trade3 = trade_need_usd[trade_need_usd['buying_amount'] > 50000]
print("超过5万美金的总数: ", trade3.count()['user_id'], " 平均值: ", trade3['buying_amount'].mean().round())
trade3.to_csv('csv/result_need_usd_3.csv')

# 超过10万美金
trade4 = trade_need_usd[trade_need_usd['buying_amount'] > 100000]
print("超过10万美金的总数: ", trade4.count()['user_id'], " 平均值: ", trade4['buying_amount'].mean().round())
trade4.to_csv('csv/result_need_usd_4.csv')

