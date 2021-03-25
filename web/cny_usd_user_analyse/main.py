import pandas as pd
import numpy as np

# 分析人民币换美金 用户的 属性

id = pd.read_csv("../../db/new/user_identification_detail_03-25.csv", low_memory=False)
trade = pd.read_csv("../../db/new/trade 3-8.csv", low_memory=False)
trade = trade[(trade['buying_currency'] == 'USD') & (trade['is_chain_version'] == 1)]
trade = trade.drop_duplicates(subset=['seller_id'], keep=False)
# add age
now = pd.Timestamp('now')
# id['birth_date'] = id['birth_date'].where(id['birth_date'] < now, id['birth_date'] - np.timedelta64(100, 'Y'))
id = id.dropna(subset=['birth_date'])
id['birth_date'] = pd.to_datetime(id['birth_date'], errors='coerce')
id['age'] = (now - id['birth_date']).astype('<m8[Y]')

dealer = [80, 84, 1148, 957]
trade = trade.query('seller_id not in @dealer')

data = pd.merge(trade, id, how='inner', left_on='seller_id', right_on='user_id')
data.to_csv('test.csv')
# 性别
gender_male = data[data['gender'] == 'M'].count()['gender']
print('gender male: ', gender_male)
gender_female = data[data['gender'] == 'F'].count()['gender']
print('gender female: ', gender_female)

# 年龄
data_age = data.groupby(['age']).size()
age_json = ''
for item in data_age.items():
    age = str(item[0])
    count = str(item[1])
    age_json += '{value: '+count+', name: \''+age+'\'},'
print(age_json)

# 国家
CN = data[data['nationality'] == 'CN'].count()['nationality']
print('CN: ', CN)
US = data[data['nationality'] == 'US'].count()['nationality']
print('US: ', US)

# 地区
data_region = data.groupby(['region_name']).size()
region_json = ''
for item in data_region.items():
    region = str(item[0])
    count = str(item[1])
    region_json += '{value: '+count+', name: \''+region+'\'},'
print(region_json)
