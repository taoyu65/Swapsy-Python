import pandas as pd
from bokeh.models import CustomJSHover, HoverTool, ColumnDataSource
from bokeh.palettes import Spectral3, Oranges3, Accent3, Accent4, Accent8

from bokeh.plotting import figure, output_file, show

# 充值统计

db = pd.read_csv("csv/main.csv", low_memory=False)

output_file('html/main2.html')

group = db.groupby('create_time')[['usd10', 'usd20', 'usd50', 'usd200', 'usd']].sum()
print(group)
source = ColumnDataSource(group)

ct = source.data['create_time'].tolist()

p = figure(x_range=ct, height=400, sizing_mode='stretch_width')
p.vbar_stack(stackers=['usd200', 'usd50', 'usd20', 'usd10'],
             x='create_time', source=source,
             legend_label=['usd 169.9', 'usd 44.9', 'usd 18.9', 'usd 9.9'],
             width=0.5, color=Accent8[1:5])

hover = HoverTool()
hover.tooltips = [
    ('create_time', '@create_time'),
    ('$9.9', '@usd10{0}'),
    ('$18.9', '@usd20{0}'),
    ('$44.9', '@usd50{0}'),
    ('$169.9', '@usd200{0}'),
    ('Total', '@usd{0}'),
]
p.title.text = 'Unit: dollar $'
p.add_tools(hover)

show(p)
