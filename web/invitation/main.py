import pandas as pd

# 要邀请人所有交易数 和 充值总数

trade = pd.read_csv("../../db/new/trade.csv", low_memory=False)
inviter = pd.read_csv("../../db/invitation_user 11-16.csv", low_memory=False)
nmi = pd.read_csv("../../db/credit_nmi_transaction 11-16.csv", low_memory=False)
manual = pd.read_csv("../../db/credit_payment 11-16.csv", low_memory=False)

# check specific inviters contribute
# inviter = inviter[inviter['inviter_id'] == 22328]
trade = trade[trade['status'] == 40]

a = pd.merge(inviter, trade, left_on='invitee_id', right_on='seller_id')
a = a[['inviter_id', 'invitee_id']]
print('total_invitee_transaction:', a.count()[0])

#
b = pd.merge(inviter, nmi, left_on='invitee_id', right_on='user_id')
c = pd.merge(inviter, manual, left_on='invitee_id', right_on='user_id')
b = b[['inviter_id', 'invitee_id', 'discount_amount']]
c = c[(c['is_payed'] == 1) & (c['return_credit_transaction_id'] == 0)]
c = c[['inviter_id', 'invitee_id', 'pay_sum_discount']]
print(c)
b.to_csv('csv/nmi.csv')
c.to_csv('csv/manual.csv')

totalNmi = b['discount_amount'].sum()
totalManual = c['pay_sum_discount'].sum()
print('total nmi: ', totalNmi)
print('total manual:', totalManual)
print('sum:', totalNmi + totalManual)
