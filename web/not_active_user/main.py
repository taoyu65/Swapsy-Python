import pandas as pd
import time

# 计算不活跃用户 (发送coupon目的)

# variable
time_now = int(time.time())
stimulation_type_id = 5
user_group = 200801
duration_time = 5 * 24 * 3600

start1 = 1582675200     # 2020-02-26(半年前发500SC)
start1_credit = 500
start1_template_id_eng = 13
start1_template_id_chn = 12

start2 = 1590451200     # 2020-05-26(3个月到半年发50%)
start2_off = 50
start2_template_id_eng = 15
start2_template_id_chn = 14

user_identification = pd.read_csv("db/user_identification 2020-08-26.csv", low_memory=False)
user = pd.read_csv("db/user 2020-08-26.csv", low_memory=False)
trade = pd.read_csv("db/trade 2020-07-03.csv", low_memory=False)
trade_part = pd.read_csv("db/trade 07-03 to 08-26.csv", low_memory=False)
trade = trade.append(trade_part)

user_identification = user_identification[user_identification['create_time'] < start2]
user_identification = user_identification[user_identification['status'] == 40]
user_identification = user_identification[['user_id']]

user = user[user['create_time'] < start2]
user = user[['id', 'default_language', 'uuid']]

# ID已经验证并且带默认语言的用户
verified_user_with_language = user_identification.merge(user, left_on='user_id', right_on='id', how='left')

trade['user_id'] = trade['seller_id']
trade = trade[['user_id', 'status', 'update_time']]
trade = trade.drop_duplicates(subset='user_id', keep='last')   # 真正完成过交易的用户

result = verified_user_with_language.merge(trade, on='user_id', how='left')
result.fillna(0, inplace=True)

stimulation_1 = pd.DataFrame()
stimulation_2 = pd.DataFrame()

result_500_SC = result[(result['update_time'] == 0) | (result['update_time'] < start1)]
certificate_500_SC = pd.DataFrame()
certificate_500_SC['signed_user_id'] = result_500_SC['user_id']
certificate_500_SC['credit'] = start1_credit
certificate_500_SC['duration_time'] = duration_time
certificate_500_SC['create_time'] = time_now
certificate_500_SC['stimulation_type_id'] = stimulation_type_id
certificate_500_SC['user_group'] = user_group
certificate_500_SC.to_csv('csv/certificate_500_SC.csv', index=False)

stimulation_1['user_id'] = certificate_500_SC['signed_user_id']
stimulation_1['coupon_id'] = 0
stimulation_1['email_template_id'] = result_500_SC['default_language'].apply(lambda lan: start1_template_id_eng if lan == 'en-US' else start1_template_id_chn)
stimulation_1['type_id'] = stimulation_type_id
stimulation_1['create_time'] = time_now
stimulation_1['user_group'] = user_group

print(stimulation_1)

result_50_OFF = result[(result['update_time'] < start2) & (result['update_time'] > start1)]
certificate_50_OFF = pd.DataFrame()
certificate_50_OFF['signed_user_id'] = result_50_OFF['user_id']
certificate_50_OFF['credit'] = 0
certificate_50_OFF['credit_discount_rate'] = start2_off
certificate_50_OFF['duration_time'] = duration_time
certificate_50_OFF['create_time'] = time_now
certificate_50_OFF['stimulation_type_id'] = stimulation_type_id
certificate_50_OFF['user_group'] = user_group
certificate_50_OFF.to_csv('csv/certificate_50_OFF.csv', index=False)

stimulation_2['user_id'] = certificate_50_OFF['signed_user_id']
stimulation_2['coupon_id'] = 0
stimulation_2['email_template_id'] = result_50_OFF['default_language'].apply(lambda lan: start2_template_id_eng if lan == 'en-US' else start2_template_id_chn)
stimulation_2['type_id'] = stimulation_type_id
stimulation_2['create_time'] = time_now
stimulation_2['user_group'] = user_group


stimulation = pd.DataFrame()
stimulation = stimulation.append(stimulation_1)
stimulation = stimulation.append(stimulation_2)
stimulation.to_csv('csv/stimulation.csv', index=False)
