import pandas as pd
import numpy as np
import swifter

# 交易时间金额分布图 用户A确认打款到A确认收款

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

step2 = pd.merge(proof, confirm, how='inner', left_on='trade_id', right_on='receiver_trade_id')
step2 = pd.merge(step2, trade, how='inner', left_on='trade_id', right_on='id')

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

# arr = []
# amount = [300, 600, 900, 1200, 1500, 1800, 2100]
# hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
# for row in amount:
#     for row2 in hour:
#         arr.append([row, row2])
# data = pd.DataFrame(arr, columns=['a', 'b'])

result = step2_output.groupby(step2_output.columns.tolist(), as_index=False).size().to_frame('count')
# result1['amount'] = result1['selling_amount']
# result1['hour'] = result1['step1']
result = result.reset_index(level=['selling_amount', 'step2'])
result['step2'] = result['step2'] - 1
print(result)
result.to_json('main2.json', orient='split')
result.to_csv('main2.csv')

# 9小时内各个金额区间的(用户A确认打款到A确认收款)占比
hour = 9
total_count = result['count'].sum()     # 4981
all_required_hour_record = result[result['step2'] <= hour]
require_hour_count = all_required_hour_record['count'].sum()

index0_in_hour_count = all_required_hour_record[all_required_hour_record['selling_amount'] == 0]['count'].sum()
index1_in_hour_count = all_required_hour_record[all_required_hour_record['selling_amount'] == 1]['count'].sum()
index2_in_hour_count = all_required_hour_record[all_required_hour_record['selling_amount'] == 2]['count'].sum()
index3_in_hour_count = all_required_hour_record[all_required_hour_record['selling_amount'] == 3]['count'].sum()
index4_in_hour_count = all_required_hour_record[all_required_hour_record['selling_amount'] == 4]['count'].sum()
index5_in_hour_count = all_required_hour_record[all_required_hour_record['selling_amount'] == 5]['count'].sum()
index6_in_hour_count = all_required_hour_record[all_required_hour_record['selling_amount'] == 6]['count'].sum()

index0_range_count = result[result['selling_amount'] == 0].sum()['count']
index1_range_count = result[result['selling_amount'] == 1].sum()['count']
index2_range_count = result[result['selling_amount'] == 2].sum()['count']
index3_range_count = result[result['selling_amount'] == 3].sum()['count']
index4_range_count = result[result['selling_amount'] == 4].sum()['count']
index5_range_count = result[result['selling_amount'] == 5].sum()['count']
index6_range_count = result[result['selling_amount'] == 6].sum()['count']

print('all ', hour, 'hour: ', require_hour_count, ' / total: ', total_count, ' = ', "{:.1%}".format(require_hour_count / total_count))
print('0-300 ', hour, 'hour: ', index0_in_hour_count, ' / range total: ', index0_range_count, ' = ', "{:.1%}".format(index0_in_hour_count / index0_range_count))
print('300-600 ', hour, 'hour: ', index1_in_hour_count, ' / range total: ', index1_range_count, ' = ', "{:.1%}".format(index1_in_hour_count / index1_range_count))
print('600-900 ', hour, 'hour: ', index2_in_hour_count, ' / range total: ', index2_range_count, ' = ', "{:.1%}".format(index2_in_hour_count / index2_range_count))
print('900-1200 ', hour, 'hour: ', index3_in_hour_count, ' / range total: ', index3_range_count, ' = ', "{:.1%}".format(index3_in_hour_count / index3_range_count))
print('1200-1500 ', hour, 'hour: ', index4_in_hour_count, ' / range total: ', index4_range_count, ' = ', "{:.1%}".format(index4_in_hour_count / index4_range_count))
print('1500-1800 ', hour, 'hour: ', index5_in_hour_count, ' / range total: ', index5_range_count, ' = ', "{:.1%}".format(index5_in_hour_count / index5_range_count))
print('1800-2100 ', hour, 'hour: ', index6_in_hour_count, ' / range total: ', index6_range_count, ' = ', "{:.1%}".format(index6_in_hour_count / index6_range_count))


