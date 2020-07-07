from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Accent3, Accent8
from bokeh.plotting import figure
from bokeh.transform import dodge
import pandas as pd

df = pd.read_csv("csv/first.csv")

output_file("html/main.html")

# 总数统计
df['sum'] = 0
group_all = df.groupby(['login_time'])['sum'].count().reset_index(name='sum_all')
group_verified = df[df['is_verified'] == 1.0].groupby(['login_time'])['sum'].count().reset_index(name='sum_verified')
group = pd.merge(group_all, group_verified, on='login_time', how='inner')
source = ColumnDataSource(group)

x_range = source.data['login_time'].tolist()

p = figure(x_range=x_range, height=400, sizing_mode='stretch_width')

p.vbar(x=dodge('login_time', -0.35, range=p.x_range), top='sum_all', width=0.3, source=source,
       color=Accent8[0], legend_label="All Users")

p.vbar(x=dodge('login_time',  0.0,  range=p.x_range), top='sum_verified', width=0.3, source=source,
       color=Accent8[1], legend_label="ID Verified Users")

hover = HoverTool()
hover.tooltips = [
    ('All Users', '@sum_all'),
    ('Only Verified Users', '@sum_verified'),
]

p.title.text = 'User Login'
p.xaxis.axis_label = 'Create Time'
p.yaxis.axis_label = 'Total Amount'
p.add_tools(hover)

p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

show(p)
