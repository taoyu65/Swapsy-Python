import pandas as pd

# 要邀请人所有交易数 和 充值总数

YEAR_MONTH = '2022-01'

inviter = pd.read_csv("../../db/new/invitation_user_2022-02-27.csv", low_memory=False)
nmi = pd.read_csv("../../db/new/credit_nmi_transaction_2022-02-27.csv", low_memory=False)
manual = pd.read_csv("../../db/new/credit_payment_2022-02-27.csv", low_memory=False)
redeem = pd.read_csv("../../db/new/invitation_redeem_2022-02-27.csv", low_memory=False)

inviter['create_time'] = pd.to_datetime(inviter['create_time'], unit='s')
inviter['create_time'] = inviter['create_time'].dt.strftime('%Y-%m')
inviter = inviter[(inviter['create_time'] == YEAR_MONTH)]

nmi['create_time'] = pd.to_datetime(nmi['create_time'], unit='s')
nmi['create_time'] = nmi['create_time'].dt.strftime('%Y-%m')
nmi = nmi[(nmi['create_time'] == YEAR_MONTH)]

manual['create_time'] = pd.to_datetime(manual['create_time'], unit='s')
manual['create_time'] = manual['create_time'].dt.strftime('%Y-%m')
manual = manual[(manual['create_time'] == YEAR_MONTH)]

redeem['complete_time'] = pd.to_datetime(redeem['complete_time'], unit='s')
redeem['complete_time'] = redeem['complete_time'].dt.strftime('%Y-%m')
redeem = redeem[(redeem['complete_time'] == YEAR_MONTH) & redeem['is_complete'] == 1]
# trade = trade[trade['status'] == 40]

# a = pd.merge(inviter, trade, left_on='invitee_id', right_on='seller_id')
# a = a[['inviter_id', 'invitee_id']]
# print('total_invitee_transaction:', a.count()[0])

#
b = pd.merge(inviter, nmi, left_on='invitee_id', right_on='user_id')
c = pd.merge(inviter, manual, left_on='invitee_id', right_on='user_id')
b = b[['inviter_id', 'invitee_id', 'discount_amount']]
c = c[(c['is_payed'] == 1) & (c['return_credit_transaction_id'] == 0)]
c = c[['inviter_id', 'invitee_id', 'pay_sum_discount']]
print(c)
b.to_csv('csv/nmi.csv')
c.to_csv('csv/manual.csv')

totalSendOut = round(redeem['amount'].sum(), 2)
totalNmi = round(b['discount_amount'].sum(), 2)
totalManual = round(c['pay_sum_discount'].sum(), 2)
print('total send out: ', totalSendOut)
print('total nmi: ', totalNmi)
print('total CNY:', totalManual)
print('sum:', totalNmi + totalManual)
