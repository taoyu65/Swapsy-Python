from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.transform import dodge
import pandas as pd

# 用户交易笔数的统计

output_file("html/交易笔数.html")

trade = pd.read_csv("../../db/new/trade 2020-12-26.csv", low_memory=False)

trade = trade[(trade['is_chain_version'] == 1) & (trade['status'] == 40)]
trade['create_time'] = pd.to_datetime(trade['create_time'], unit='s')
trade['create_time'] = trade['create_time'].dt.strftime('%y/%m')

trade['sum'] = 0
group_all = trade.groupby(['create_time'])['sum'].count().reset_index(name='sum_all')
group_cny = trade[trade['buying_currency'] == 'CNY'].groupby(['create_time'])['sum'].count().reset_index(name='sum_cny')
group_usd = trade[trade['buying_currency'] == 'USD'].groupby(['create_time'])['sum'].count().reset_index(name='sum_usd')
group = pd.merge(group_all, group_cny, on='create_time', how='inner')
group = pd.merge(group, group_usd, on='create_time', how='inner')
source = ColumnDataSource(group)

x_range = source.data['create_time'].tolist()

p = figure(x_range=x_range, height=400, sizing_mode='stretch_width')

p.vbar(x=dodge('create_time', -0.25, range=p.x_range), top='sum_all', width=0.2, source=source,
       color='#bebada', legend_label="All Users")

p.vbar(x=dodge('create_time',  0.0,  range=p.x_range), top='sum_cny', width=0.2, source=source,
       color='#fb8072', legend_label="Require CNY")

p.vbar(x=dodge('create_time',  0.25,  range=p.x_range), top='sum_usd', width=0.2, source=source,
       color='#80b1d3', legend_label="Require USD")

hover = HoverTool()
hover.tooltips = [
    ('Create Time', '@create_time'),
    ('All', '@sum_all'),
    ('Require CNY', '@sum_cny'),
    ('Require USD', '@sum_usd'),
]

p.title.text = 'Transaction'
p.xaxis.axis_label = 'Create Time'
p.yaxis.axis_label = 'Transaction Number'
p.add_tools(hover)

p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

show(p)
