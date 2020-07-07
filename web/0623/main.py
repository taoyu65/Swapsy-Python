import numpy as np
import datetime as dt
import pandas as pd
from bokeh.layouts import column
from bokeh.models import CustomJSHover, HoverTool, ColumnDataSource
from bokeh.palettes import Spectral3, Oranges3, Accent3, Accent4, Accent8

from bokeh.plotting import figure, output_file, show
from bokeh.transform import dodge

df = pd.read_csv("csv/second.csv")
df_recharge = pd.read_csv("csv/third.csv")

output_file('html/main.html')

# stacker 交易总数统计
group = df.groupby('create_time').sum()
source = ColumnDataSource(group)

# 大于3笔交易的人数
df['user_id'] = df['seller_id']
df = df[['create_time', 'user_id', 'less_than_3', 'greater_than_3']]
df['count'] = 0
df = pd.merge(df, df_recharge, on=['create_time', 'user_id'], how='left')
df['recharge_count'].fillna(0, inplace=True)
df['recharge_count'] = df['recharge_count'].astype(int)

# group2: by user amount
group_a = df[df['less_than_3'] == 0].groupby('create_time')['count'].count().reset_index(name='less_than_3_count')
group_b = df[df['greater_than_3'] == 0].groupby('create_time')['count'].count().reset_index(name='greater_than_3_count')
group2 = pd.merge(group_a, group_b, on='create_time', how='inner')
group2['count_greater_than_3_all'] = group2['less_than_3_count'] + group2['greater_than_3_count']
# source2 = ColumnDataSource(group2)

# group3: user of trade amount <3, stacker recharged and not recharged
# columns: less_than_3_not_recharged less_than_3_recharged
group3 = df[df['less_than_3'] == 0]
group3_a = group3[group3['recharge_count'] == 0].groupby(['create_time'])['count']\
    .count().reset_index(name='less_than_3_not_recharged')
group3_b = group3[group3['recharge_count'] > 0].groupby(['create_time'])['count']\
    .count().reset_index(name='less_than_3_recharged')
group3 = pd.merge(group3_a, group3_b, on='create_time')
group3['count_less_than_3_all'] = group3['less_than_3_not_recharged'] + group3['less_than_3_recharged']
# source3 = ColumnDataSource(group3)

group_with_recharge = pd.merge(group2, group3, on='create_time')
source2 = ColumnDataSource(group_with_recharge)

x = 'create_time'
ct = source.data['create_time'].tolist()
p = figure(x_range=ct, height=400, sizing_mode='stretch_width')
p2 = figure(x_range=ct, height=400, sizing_mode='stretch_width')
# p.toolbar_location = None

r1 = p.vbar_stack(stackers=['greater_than_3', 'less_than_3'],
                  x=x, source=source,
                  legend_label=['Trade Amount (>3)', 'Trade Amount (<3)'],
                  width=0.5, color=Accent3[1:3])
p2.vbar(x=dodge(x, -0.35, range=p.x_range), top='greater_than_3_count', width=0.3, source=source2,
        color=Accent8[1], legend_label="Total user (trade amount > 3)")

# p2.vbar_stack(x=dodge(x, 0.0, range=p.x_range), top='less_than_3_count', width=0.3, source=source2,
#         color=Accent8[1], legend_label="User Amount (<3)")
p2.vbar_stack(stackers=['less_than_3_not_recharged', 'less_than_3_recharged'],
              x=dodge(x, 0.0, range=p.x_range), source=source2,
              legend_label=['Total not recharged user (trade amount < 3)', 'Total recharged user (trade amount < 3)'],
              width=0.3, color=["#fbb4ae", "#7fc97f"])
# r2 = p2.line(x=x, y='greater_than_3_count', source=source2, color='#33a02c', legend_label='User Amount (>3)')
# r3 = p2.line(x=x, y='less_than_3_count', source=source2, legend_label='User Amount (<3)')

hover = HoverTool()
hover.tooltips = [
    ('create_time', '@create_time'),
    ('Trade Amount (>3)', '@greater_than_3'),
    ('Trade Amount (<3)', '@less_than_3'),
    ('Trade Total', '@status'),
]

hover2 = HoverTool()
hover2.tooltips = [
    ('create_time', '@create_time'),
    ('User Amount (>3)', '@greater_than_3_count'),
    ('User Amount (<3)', '@less_than_3_count'),
    ('User Total', '@count_greater_than_3_all'),
    ('(<3) Not Recharged', '@less_than_3_not_recharged'),
    ('(<3) Recharged', '@less_than_3_recharged'),
    ('(<3) User Total', '@count_less_than_3_all'),
]

p.title.text = 'Total Amount trade by Month'
p.xaxis.axis_label = 'Create Time'
p.yaxis.axis_label = 'Total Amount'

p.add_tools(hover)
p2.add_tools(hover2)

p.legend.location = 'top_left'
p2.legend.location = 'top_left'

# show(p)
show(p2)
