import pandas as pd
import numpy as np
import swifter

# 交易时间金额分布图 用户A确认打款到B确认收款

confirm = pd.read_csv("../../db/new/trade transaction proof operation 2021-03-09.csv", low_memory=False)
confirm = confirm[confirm['status'] > 10]
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

step = pd.merge(proof, confirm, how='inner', left_on='trade_id', right_on='sender_trade_id')
step = pd.merge(step, trade, how='inner', left_on='trade_id', right_on='id')

step['hour'] = (step['create_time_y'] - step['create_time_x']).div(3600).round().astype(int)
step['selling_amount'] = step['selling_amount'].astype(int)

step_output = step[['selling_amount', 'hour']]
step_output = step_output[step_output['hour'] < 48]


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


print(step)
step_output['hour'] = step_output['hour'].round()

step_output['selling_amount'] = step_output['selling_amount'].swifter.apply(calculation)
step_output['hour'] = step['hour'].astype(int)

# 如果step1是 0 改成 1
step_output.loc[step_output.hour == 0, "hour"] = 1

print(step_output)
step_output.to_csv('test.csv')

result = step_output.groupby(step_output.columns.tolist(), as_index=False).size().to_frame('count')
# result1['amount'] = result1['selling_amount']
# result1['hour'] = result1['step1']
print(result)
result = result.reset_index(level=['selling_amount', 'hour'])
# result['hour'] = result['hour'] - 1
print(result)
result.to_csv("main3.csv")
result.to_json('main3.json', orient='split')
