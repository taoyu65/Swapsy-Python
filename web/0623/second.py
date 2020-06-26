import pandas as pd
import numpy as np

df = pd.read_csv("csv/first.csv", low_memory=False)

df['greater_than_3'] = np.where(df['status'] <= 3, 0, df['status'])
df['less_than_3'] = np.where(df['status'] > 3, 0, df['status'])
print(df)

print(df[df['create_time'] == '2020-06'].sum())

# df = df.groupby('create_time')['greater_than_3', 'less_than_3'].count()
# print(df)
df.to_csv('csv/second.csv')
