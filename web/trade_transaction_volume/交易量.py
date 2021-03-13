from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.transform import dodge
import pandas as pd

# 用户交易量的统计

output_file("html/交易量.html")

trade = pd.read_csv("../../db/new/trade.csv", low_memory=False)

trade = trade[(trade['is_chain_version'] == 1) & (trade['status'] == 40)]
trade['create_time'] = pd.to_datetime(trade['create_time'], unit='s')
trade['create_time'] = trade['create_time'].dt.strftime('%y/%m')

group_cny = trade[(trade['buying_currency'] == 'CNY') & (trade['selling_currency'] == 'USD')].groupby(['create_time'])['selling_amount'].sum().reset_index(name='sum_cny')
group_usd = trade[(trade['buying_currency'] == 'USD') & (trade['selling_currency'] == 'CNY')].groupby(['create_time'])['buying_amount'].sum().reset_index(name='sum_usd')
group = pd.merge(group_usd, group_cny, on='create_time', how='inner')
source = ColumnDataSource(group)

x_range = source.data['create_time'].tolist()

p = figure(x_range=x_range, height=400, sizing_mode='stretch_width')

p.vbar(x=dodge('create_time',  0.0,  range=p.x_range), top='sum_cny', width=0.2, source=source,
       color='#fb8072', legend_label="Buy CNY")

p.vbar(x=dodge('create_time',  0.25,  range=p.x_range), top='sum_usd', width=0.2, source=source,
       color='#80b1d3', legend_label="Buy USD")

hover = HoverTool()
hover.tooltips = [
    ('Create Time', '@create_time'),
    ('Buy CNY', '@sum_cny{($ 0.00 a)}'),
    ('Buy USD', '@sum_usd{($ 0.00 a)}'),
]

p.title.text = 'Transaction'
p.xaxis.axis_label = 'Create Time'
p.yaxis.axis_label = 'Transaction Amount'
p.add_tools(hover)

p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

show(p)
