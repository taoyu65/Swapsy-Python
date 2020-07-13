import pandas as pd
import numpy as np

db = pd.read_csv("csv/main.csv", low_memory=False)

db2 = db[db['count'] == 0]
print(db2.count())     # count: 431

db2 = db2[['user_id']]

db2.to_csv('csv/main2.csv')



