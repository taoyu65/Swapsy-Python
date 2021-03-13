import pandas as pd
import numpy as np
import swifter

# 交易时间金额分布图 用户A确认打款到用户C给A确认打款

proof = pd.read_csv("../../db/new/trade transaction proof 2021-03-09.csv", low_memory=False)
trade = pd.read_csv("../../db/new/trade.csv", low_memory=False)
trade = trade[['id', 'buying_currency', 'selling_amount']]
# 仅仅需要 美金换人民币
trade = trade[trade['buying_currency'] == 'CNY']

proof['date'] = pd.to_datetime(proof['create_time'], unit='s')
proof['date'] = proof['date'].dt.strftime('%y/%m')  # 或者 dt.year / dt.month / dt.day / dt.data
proof = proof[proof['date'] >= '21/02']  # calculate after 2019-1-1

dealer = [80, 84, 1148, 957]
proof = proof.query('user_id not in @dealer')

copy = proof.copy(deep=True)

step1 = pd.merge(proof, copy, how='inner', left_on='trade_id', right_on='receiver_trade_id')
step1 = pd.merge(step1, trade, how='inner', left_on='trade_id_x', right_on='id')

step1['step1'] = (step1['create_time_y'] - step1['create_time_x']).div(3600).round().astype(int)
step1['selling_amount'] = step1['selling_amount'].astype(int)

step1_output = step1[['selling_amount', 'step1']]
step1_output = step1_output[step1_output['step1'] < 48]


# interval function
def calculation(x):
    if 0 < x < 450:
        return 0            # $300
    elif 450 <= x < 750:
        return 1            # $600
    elif 750 <= x < 1050:
        return 2            # $900
    elif 1050 <= x < 1350:
        return 3            # $1200
    elif 1350 <= x < 1650:
        return 4            # $1500
    elif 1650 <= x < 1950:
        return 5            # $1800
    elif 1950 <= x < 2100:
        return 6            # $2100
    else:
        return 0


print(step1)
step1_output['step1'] = step1_output['step1'].round()

step1_output['selling_amount'] = step1_output['selling_amount'].swifter.apply(calculation)
step1_output['step1'] = step1['step1'].astype(int)

# 如果step1是 0 改成 1
step1_output.loc[step1_output.step1 == 0, "step1"] = 1

print(step1_output)
# step1_output.to_csv('test2.csv')

# arr = []
# amount = [300, 600, 900, 1200, 1500, 1800, 2100]
# hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
# for row in amount:
#     for row2 in hour:
#         arr.append([row, row2])
# data = pd.DataFrame(arr, columns=['a', 'b'])

result1 = step1_output.groupby(step1_output.columns.tolist(), as_index=False).size().to_frame('count')
# result1['amount'] = result1['selling_amount']
# result1['hour'] = result1['step1']
result1 = result1.reset_index(level=['selling_amount', 'step1'])
result1['step1'] = result1['step1'] - 1
print(result1)
result1.to_json('main1.json', orient='split')
# result1.to_numpy()
# test.to_csv('test.csv')

# for index, row in data.iterrows():

# decimals = pd.Series([0, 1], index=['step1', 'selling_amountn'])
# step1_output = step1_output.round(decimals)
# print(step1_output)

# for index, row in step1_output.iterrows():
#     print(row['step1'])
# print(step1_output.to_numpy())
# step1_output.to_json('go.json', orient='split')
