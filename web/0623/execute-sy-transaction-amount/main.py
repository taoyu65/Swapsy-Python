import pandas as pd
import numpy as np

# sy: 计算按笔数 5~10 / 10~20 的用户总数

df = pd.read_csv("../csv/first.csv", low_memory=False)

month_07_5_10 = df[(df['create_time'] == '2020-07') & (df['status'] >= 5) & (df['status'] < 10)]
month_08_5_10 = df[(df['create_time'] == '2020-08') & (df['status'] >= 5) & (df['status'] < 10)]
month_09_5_10 = df[(df['create_time'] == '2020-09') & (df['status'] >= 5) & (df['status'] < 10)]

month_07_10_20 = df[(df['create_time'] == '2020-07') & (df['status'] >= 10) & (df['status'] < 20)]
month_08_10_20 = df[(df['create_time'] == '2020-08') & (df['status'] >= 10) & (df['status'] < 20)]
month_09_10_20 = df[(df['create_time'] == '2020-09') & (df['status'] >= 10) & (df['status'] < 20)]

print('07月: 5~10笔总共', month_07_5_10.count()[0], '人')
print('07月: 10~20笔总共', month_07_10_20.count()[0], '人')
print('08月: 5~10笔总共', month_08_5_10.count()[0], '人')
print('07月: 10~20笔总共', month_08_10_20.count()[0], '人')
print('09月: 5~10笔总共', month_09_5_10.count()[0], '人')
print('07月: 10~20笔总共', month_09_10_20.count()[0], '人')
