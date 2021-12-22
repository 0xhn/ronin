from utils.db import db
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math
import pandas as pd

start_day = datetime(2021, 4, 29)
end_day = datetime(2021, 11, 27)
days = (end_day - start_day).days

delta = 3
for i in range(0, math.ceil(days / delta)):
    match = {
        'timestamp': {'$gte': datetime(2021, 4, 29) + relativedelta(days=i * 3),
                      '$lte': datetime(2021, 5, 2) + relativedelta(days=i * 3)}}
    filter = {'from': 1, 'to': 1, '_id': 0}
    result = list(db['axiecontact_transfer'].find(match, filter))
    frame = pd.DataFrame(result)
    group_df = frame.groupby(by=['from', 'to']).size().reset_index(name='times')
    start_ = (datetime(2021, 4, 29) + relativedelta(days=i * 3)).strftime("%Y-%m-%d")
    end_ = (datetime(2021, 5, 2) + relativedelta(days=i * 3) - relativedelta(days=1)).strftime("%Y-%m-%d")
    group_df.to_csv('./axie_transfer_data/{}_{}.csv'.format(start_, end_), index=False)
