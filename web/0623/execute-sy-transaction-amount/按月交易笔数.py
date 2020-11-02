import pandas as pd
import numpy as np

# gz: 计算按笔数 5~10 / 10~20 的用户总数

df = pd.read_csv("../csv/first.csv", low_memory=False)

# month_07_5_10 = df[(df['create_time'] == '2020-07') & (df['status'] >= 5) & (df['status'] < 10)]
# month_08_5_10 = df[(df['create_time'] == '2020-08') & (df['status'] >= 5) & (df['status'] < 10)]
# month_09_5_10 = df[(df['create_time'] == '2020-09') & (df['status'] >= 5) & (df['status'] < 10)]
#
# month_07_10_20 = df[(df['create_time'] == '2020-07') & (df['status'] >= 10) & (df['status'] < 20)]
# month_08_10_20 = df[(df['create_time'] == '2020-08') & (df['status'] >= 10) & (df['status'] < 20)]
# month_09_10_20 = df[(df['create_time'] == '2020-09') & (df['status'] >= 10) & (df['status'] < 20)]
#
# month_07_20_max = df[(df['create_time'] == '2020-07') & (df['status'] >= 20)]
# month_08_20_max = df[(df['create_time'] == '2020-08') & (df['status'] >= 20)]
# month_09_20_max = df[(df['create_time'] == '2020-09') & (df['status'] >= 20)]

#
# print('07月: 5~10笔总共', month_07_5_10.count()[0], '人')
# month_07_5_10['seller_id'].to_csv('csv/07_05_10.csv')
#
# print('07月: 10~20笔总共', month_07_10_20.count()[0], '人')
# month_07_10_20['seller_id'].to_csv('csv/07_10_20.csv')
#
# print('07月: 20+笔总共', month_07_20_max.count()[0], '人')
# month_07_20_max['seller_id'].to_csv('csv/07_20_max.csv')
#
#
# print('08月: 5~10笔总共', month_08_5_10.count()[0], '人')
# month_08_5_10['seller_id'].to_csv('csv/08_05_10.csv')
#
# print('08月: 10~20笔总共', month_08_10_20.count()[0], '人')
# month_08_10_20['seller_id'].to_csv('csv/08_10_20.csv')
#
# print('08月: 20+笔总共', month_08_20_max.count()[0], '人')
# month_08_20_max['seller_id'].to_csv('csv/08_20_max.csv')
#
#
# print('09月: 5~10笔总共', month_09_5_10.count()[0], '人')
# month_09_5_10['seller_id'].to_csv('csv/09_05_10.csv')
#
# print('09月: 10~20笔总共', month_09_10_20.count()[0], '人')
# month_09_10_20['seller_id'].to_csv('csv/09_10_20.csv')
#
# print('09月: 20+笔总共', month_09_20_max.count()[0], '人')
# month_09_20_max['seller_id'].to_csv('csv/09_20_max.csv')

# month 10
print('start...')
month_10_5_10 = df[(df['create_time'] == '2020-10') & (df['status'] >= 5) & (df['status'] < 10)]
month_10_10_20 = df[(df['create_time'] == '2020-10') & (df['status'] >= 10) & (df['status'] < 20)]
month_10_20_max = df[(df['create_time'] == '2020-10') & (df['status'] >= 20)]

print('10月: 5~10笔总共', month_10_5_10.count()[0], '人')
month_10_5_10['seller_id'].to_csv('csv/10_05_10.csv')

print('10月: 10~20笔总共', month_10_10_20.count()[0], '人')
month_10_10_20['seller_id'].to_csv('csv/10_10_20.csv')

print('10月: 20+笔总共', month_10_20_max.count()[0], '人')
month_10_20_max['seller_id'].to_csv('csv/10_20_max.csv')
