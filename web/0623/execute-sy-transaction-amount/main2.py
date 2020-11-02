import pandas as pd
import numpy as np

# sy: 交易额度 $200~300  $300~400  $400~500

trade = pd.read_csv("../db/trade 2020-09-28.csv", low_memory=False)

trade = trade[(trade['is_chain_version'] == 1) & (trade['status'] == 40)]
trade['create_time'] = pd.to_datetime(trade['create_time'], unit='s')
trade['create_time'] = trade['create_time'].dt.strftime('%Y-%m')    # 或者 dt.year / dt.month / dt.day / dt.data
trade = trade.drop(['id', 'uuid', 'uuid_old', 'expire_time', 'update_time', 'is_from_old', 'is_puppet', 'rate_up', 'rate_down'], axis=1)


trade07 = trade[trade['create_time'] == '2020-07']
trade07['usd'] = np.where(trade07['buying_currency'] == 'USD', trade07['buying_amount'], trade07['selling_amount'])
trade07_200_300 = trade07[(trade07['usd'] >= 200) & (trade07['usd'] < 300)]
trade07_300_400 = trade07[(trade07['usd'] >= 300) & (trade07['usd'] < 400)]
trade07_400_500 = trade07[(trade07['usd'] >= 400) & (trade07['usd'] < 500)]
trade07_500 = trade07[trade07['usd'] >= 500]

trade08 = trade[trade['create_time'] == '2020-08']
trade08['usd'] = np.where(trade08['buying_currency'] == 'USD', trade08['buying_amount'], trade08['selling_amount'])
trade08_200_300 = trade08[(trade08['usd'] >= 200) & (trade08['usd'] < 300)]
trade08_300_400 = trade08[(trade08['usd'] >= 300) & (trade08['usd'] < 400)]
trade08_400_500 = trade08[(trade08['usd'] >= 400) & (trade08['usd'] < 500)]
trade08_500 = trade08[trade08['usd'] >= 500]

trade09 = trade[trade['create_time'] == '2020-09']
trade09['usd'] = np.where(trade09['buying_currency'] == 'USD', trade09['buying_amount'], trade09['selling_amount'])
trade09_200_300 = trade09[(trade09['usd'] >= 200) & (trade09['usd'] < 300)]
trade09_300_400 = trade09[(trade09['usd'] >= 300) & (trade09['usd'] < 400)]
trade09_400_500 = trade09[(trade09['usd'] >= 400) & (trade09['usd'] < 500)]
trade09_500 = trade09[trade09['usd'] >= 500]

print('07月 $200~$300 交易笔数: ', trade07_200_300.count()[0])
print('07月 $300~$400 交易笔数: ', trade07_300_400.count()[0])
print('07月 $400~$500 交易笔数: ', trade07_400_500.count()[0])
print('07月 $500以上 交易笔数: ', trade07_500.count()[0])

print('08月 $200~$300 交易笔数: ', trade08_200_300.count()[0])
print('08月 $300~$400 交易笔数: ', trade08_300_400.count()[0])
print('08月 $400~$500 交易笔数: ', trade08_400_500.count()[0])
print('08月 $500以上 交易笔数: ', trade08_500.count()[0])

print('09月 $200~$300 交易笔数: ', trade09_200_300.count()[0])
print('09月 $300~$400 交易笔数: ', trade09_300_400.count()[0])
print('09月 $400~$500 交易笔数: ', trade09_400_500.count()[0])
print('09月 $500以上 交易笔数: ', trade09_500.count()[0])
