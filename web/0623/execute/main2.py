import pandas as pd
import numpy as np

db = pd.read_csv("csv/main.csv", low_memory=False)

print(db[db['count'] == 0].count())     # count: 431

