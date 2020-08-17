import pandas as pd

# 发送过后 用户回来以及充值情况

variable = 1594921024   # 发送邮件的时间戳

trans = pd.read_csv("../db/credit_transaction 2020-07-05.csv", low_memory=False)
trans_part = pd.read_csv("../db/credit_transaction 2020-07-05 to 2020-08-11.csv", low_memory=False)
trans = trans.append(trans_part)
user = pd.read_csv("db/stimulation 2001 users.csv", low_memory=False)

user = user[['user_id', 'coupon_id']]

credit_user = user[user['coupon_id'] == 0]
coupon_user = user[user['coupon_id'] > 0]

db = pd.merge(credit_user, trans, on='user_id')
db = db[['user_id', 'credit_rule_id', 'credit_change', 'coupon_id', 'create_time']]
db = db[(db['credit_rule_id'] == 19) | (db['credit_rule_id'] == 37)]

db = db[db['create_time'] > variable]
print(db)
print('总共回来充值笔数', db.count()[0])

db = db.drop_duplicates(subset='user_id', keep='first')
print('总共回来充值人数', db.count()[0])

print('赠送credit的人的充值数', db[db['coupon_id'] == 0].count()[0])


