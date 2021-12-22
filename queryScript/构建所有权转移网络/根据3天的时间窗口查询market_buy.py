from utils.db import db
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math
import pandas as pd

start_day = datetime(2021, 4, 26)
end_day = datetime(2021, 11, 27)
days = (end_day - start_day).days

delta = 3
for i in range(0, math.ceil(days / delta)):
    match = {
        'timestamp': {'$gte': datetime(2021, 4, 26) + relativedelta(days=i * 3),
                      '$lte': datetime(2021, 4, 29) + relativedelta(days=i * 3)}}
    filter = {'from': 1, 'seller': 1, '_id': 0}
    result = list(db['marketcontact_buy'].find(match, filter))
    frame = pd.DataFrame(result)

    group_df = frame.groupby(by=['from', 'seller']).size().reset_index(name='times')
    group_df.rename(columns={'from': 'to', 'seller': 'from'}, inplace=True)

    start_ = (datetime(2021, 4, 26) + relativedelta(days=i * 3)).strftime("%Y-%m-%d")
    end_ = (datetime(2021, 4, 29) + relativedelta(days=i * 3) - relativedelta(days=1)).strftime("%Y-%m-%d")

    group_df.to_csv('./market_buy_data/{}_{}.csv'.format(start_, end_), index=False)
