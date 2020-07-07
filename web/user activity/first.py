import pandas as pd
import numpy as np

# load
db_login_history = pd.read_csv("db/user_login_history 2020-07-04.csv", low_memory=False)
db_identification = pd.read_csv("db/user_identification 2020-07-04.csv", low_memory=False)

# regulation
db_login_history['login_time'] = pd.to_datetime(db_login_history['login_time'], unit='s')
db_login_history['login_time'] = db_login_history['login_time'].dt.strftime('%Y-%m')    # 或者 dt.year / dt.month / dt.day / dt.data
db_login_history = db_login_history[db_login_history['login_time'] >= '2019-01']  # calculate after 2019-1-1
db_login_history = db_login_history.drop(['login_ip'], axis=1)
# db_login_history['count'] = np.zeros(len(db_login_history))
# db_login_history.drop(['id'], axis=1)

db_identification['is_verified'] = np.where(db_identification['status'] == 40, 1, 0)
db_identification = db_identification[['user_id', 'is_verified']]

# group by
groupBy = db_login_history.groupby(['login_time', 'user_id'])['id'].count().reset_index(name='count')

# merge
# merged = groupBy.join(db_identification, on='user_id', how='left')    # only considered index
# merged = pd.merge(groupBy, db_identification, on='user_id', how='left')
merged = groupBy.merge(db_identification, on='user_id', how='left')

# out put
merged.to_csv('csv/first.csv')
