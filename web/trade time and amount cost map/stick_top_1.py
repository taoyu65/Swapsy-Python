import pandas as pd
import numpy as np
import swifter

# 交易时间金额分布图 用户A确认打款到A确认收款

top = pd.read_csv("../../db/new/trade_chain_stick_top 2021-03-24.csv", low_memory=False)
confirm = pd.read_csv("../../db/new/trade transaction proof operation 2021-03-09.csv", low_memory=False)
confirm = confirm[confirm['status'] > 10]
proof = pd.read_csv("../../db/new/trade transaction proof 2021-03-09.csv", low_memory=False)
trade = pd.read_csv("../../db/new/trade.csv", low_memory=False)
trade = trade[['id', 'buying_currency', 'selling_amount']]
# 仅仅需要 美金换人民币
trade = trade[trade['buying_currency'] == 'CNY']
# trade = pd.merge(trade, top, how='inner', left_on='id', right_on='trade_id')

proof['date'] = pd.to_datetime(proof['create_time'], unit='s')
proof['date'] = proof['date'].dt.strftime('%y/%m')  # 或者 dt.year / dt.month / dt.day / dt.data
proof = proof[proof['date'] >= '20/12']  # calculate after 2019-1-1

dealer = [80, 84, 1148, 957]
proof = proof.query('user_id not in @dealer')

step2 = pd.merge(proof, confirm, how='inner', left_on='trade_id', right_on='receiver_trade_id')
step2 = pd.merge(step2, trade, how='inner', left_on='trade_id', right_on='id')

# stick top
step2 = pd.merge(step2, top, how='inner', left_on='trade_id', right_on='trade_id')

# step2.to_csv("text.csv")
# exit()

step2['step2'] = (step2['create_time_y'] - step2['create_time_x']).div(3600).round().astype(int)
step2['selling_amount'] = step2['selling_amount'].astype(int)

step2_output = step2[['selling_amount', 'step2']]
step2_output = step2_output[step2_output['step2'] < 48]


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


print(step2)
step2_output['step2'] = step2_output['step2'].round()

step2_output['selling_amount'] = step2_output['selling_amount'].swifter.apply(calculation)
step2_output['step2'] = step2['step2'].astype(int)

# 如果step1是 0 改成 1
step2_output.loc[step2_output.step2 == 0, "step2"] = 1

print(step2_output)
# step1_output.to_csv('test2.csv')


result = step2_output.groupby(step2_output.columns.tolist(), as_index=False).size().to_frame('count')
# result1['amount'] = result1['selling_amount']
# result1['hour'] = result1['step1']
result = result.reset_index(level=['selling_amount', 'step2'])
result['step2'] = result['step2'] - 1
print(result)
result.to_json('stick_top_1.json', orient='split')
result.to_csv('stick_top_1.csv')
