import pandas as pd
import numpy as np
from bokeh.models import CustomJSHover, HoverTool, ColumnDataSource
from bokeh.palettes import Spectral3, Oranges3, Accent3, Accent4, Accent8
from bokeh.plotting import figure, output_file, show

db = pd.read_csv("../../db/new/credit_payment 2021-01-25.csv", low_memory=False)

output_file('html/main.html')

db['create_time'] = pd.to_datetime(db['create_time'], unit='s')
db['create_time'] = db['create_time'].dt.strftime('%Y-%m')    # 或者 dt.year / dt.month / dt.day / dt.data

db = db[['method', 'pay_sum_amount', 'is_payed', 'create_time']]
db = db[db['is_payed'] == 1]
db = db[db['create_time'] >= '2020-01']
db = db[(db['method'] == 'alipay') | (db['method'] == 'wxpay')]

db['alipay'] = np.where(db['method'] == 'alipay', db['pay_sum_amount'], 0)
db['wxpay'] = np.where(db['method'] == 'wxpay', db['pay_sum_amount'], 0)

group = db.groupby('create_time')[['alipay', 'wxpay', 'pay_sum_amount']].sum()
print(group)

source = ColumnDataSource(group)

ct = source.data['create_time'].tolist()

p = figure(x_range=ct, height=400, sizing_mode='stretch_width')
p.vbar_stack(stackers=['alipay', 'wxpay'],
             x='create_time', source=source,
             legend_label=['Alipay', 'WeChat Pay'],
             width=0.5, color=Accent8[1:3])

hover = HoverTool()
hover.tooltips = [
    ('create_time', '@create_time'),
    ('Alipay', '@alipay{0}'),
    ('WeChat Pay', '@wxpay{0}'),
    ('Total', '@pay_sum_amount{0}'),
]
p.title.text = '人民币充值 Unit: CNY'
p.add_tools(hover)

show(p)
