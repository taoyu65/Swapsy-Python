import numpy as np
import datetime as dt
import pandas as pd
from bokeh.models import CustomJSHover, HoverTool, ColumnDataSource
from bokeh.palettes import Spectral3, Oranges3, Accent3, Accent4

from bokeh.plotting import figure, output_file, show

df = pd.read_csv("csv/second.csv")

output_file('html/main.html')

# stacker 交易总数统计
group = df.groupby('create_time').sum()
source = ColumnDataSource(group)

# 大于3笔交易的人数
group2 = df[df['less_than_3'] == 0].groupby('create_time').count()
source2 = ColumnDataSource(group2)

# 小于3笔交易的人数
group3 = df[df['greater_than_3'] == 0].groupby('create_time').count()
source3 = ColumnDataSource(group3)

x = 'create_time'
ct = source.data['create_time'].tolist()
p = figure(x_range=ct, height=400, sizing_mode='stretch_width')
# p.toolbar_location = None

r1 = p.vbar_stack(stackers=['greater_than_3', 'less_than_3'],
                  x=x, source=source,
                  legend_label=['Trade Amount (>3)', 'Trade Amount (<3)'],
                  width=0.5, color=Accent3[1:3])
r2 = p.line(x=x, y='seller_id', source=source2, color='#33a02c', legend_label='User Amount (>3)')
r3 = p.line(x=x, y='seller_id', source=source3, legend_label='User Amount (<3)')

hover = HoverTool()
hover.tooltips = [
    ('create_time', '@create_time'),
    ('Trade Amount (>3)', '@greater_than_3'),
    ('Trade Amount (<3)', '@less_than_3'),
    ('Trade Total', '@status'),
]

p.title.text = 'Total Amount trade by Month'
p.xaxis.axis_label = 'Create Time'
p.yaxis.axis_label = 'Total Amount'

p.add_tools(hover)

p.legend.location = 'top_left'

show(p)
