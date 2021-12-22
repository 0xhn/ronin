from bson import Decimal128

from utils.db import db
import pandas as pd
from datetime import datetime
import math
from dateutil.relativedelta import relativedelta
import csv

start_day = datetime(2021, 4, 26)
end_day = datetime(2021, 11, 27)
days = (end_day - start_day).days

file = open('result.csv', "a+", newline='')
csv_file = csv.writer(file)
head = ["date", "mean", 'median']
csv_file.writerow(head)

delta = 1
for i in range(0, math.ceil(days / delta)):
    match = {
        'timestamp': {'$gte': datetime(2021, 4, 26) + relativedelta(days=i * delta),
                      '$lte': datetime(2021, 4, 27) + relativedelta(days=i * delta)}}
    filter = {'price': 1, '_id': 0}
    result = list(db['marketcontact_buy'].find(match, filter))

    frame = pd.DataFrame(result)

    frame.dropna()
    frame['price'] = frame['price'].astype(str)
    frame = frame.loc[frame.price != 'None']
    frame['price'] = frame['price'].astype(float)
    # frame = frame.loc[frame.price.apply(type) != Decimal128]
    # apply(lambda x: not isinstance(x, Decimal128)).dropna()
    mean = frame['price'].mean()
    median = frame['price'].median()
    start_ = (datetime(2021, 4, 26) + relativedelta(days=i * delta)).strftime("%Y/%m/%d")
    csv_file.writerow([start_, mean, median])
