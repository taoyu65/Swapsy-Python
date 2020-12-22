import pandas as pd
from datetime import date
from random import randint

from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn


# 邀请数统计 (多少用户邀请多少人)

invite = pd.read_csv("../../db/new/invitation_user 12-21.csv", low_memory=False)
# identification = pd.read_csv("../../db/new/user_identification 12-21.csv", low_memory=False)
#
# identification = identification[identification['user_id', 'status']]

invite_dup = invite.pivot_table(index=['inviter_id'], aggfunc='size')
df = pd.DataFrame(invite_dup)
df.columns = ['invite_count']
# print(df)
df = df.pivot_table(index=['invite_count'], aggfunc='size')
# 邀请总数m的人有n个
df = pd.DataFrame(df)
df.columns = ['count']
# print(df)
print(df.index)
print(df['count'].values)
# print([randint(0, 100) for i in range(10)])

output_file("html/data_table.html")

data = dict(
        invite=df.index,
        count=df['count'].values,
    )
source = ColumnDataSource(data)

columns = [
        TableColumn(field="invite", title="Invite Users"),
        TableColumn(field="count", title="Count"),
    ]
data_table = DataTable(source=source, columns=columns, width=400, height=700, index_position=None)

show(widgetbox(data_table))

