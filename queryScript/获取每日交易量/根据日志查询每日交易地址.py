import datetime
from dateutil.relativedelta import relativedelta
from utils.db import db
import pandas as pd

start_day = datetime.datetime(2020, 2, 11)
end_day = datetime.datetime(2020, 11, 27)
days = (end_day - start_day).days

# for i in range(0, days + 1):
#     result = list(
#         db['marketcontact'].find({'timestamp': {'$gte': datetime.datetime(2021, 2, 11) + relativedelta(days=i),
#                                                 '$lte': datetime.datetime(2021, 2, 12) + relativedelta(days=i)}},
#                                  {'from': 1}))

result = list(db['marketcontact'].find({'timestamp': {'$gte': datetime.datetime(2021, 5, 11) + relativedelta(days=0),
                                                      '$lte': datetime.datetime(2021, 5, 12) + relativedelta(days=0)}},
                                       {'_id': 0, 'from': 1}))
set1 = set([res['from'] for res in result])
frame = pd.DataFrame(data)
print(len(set1))
