from utils.db import db
from datetime import datetime
import pandas as pd

gropu_script = {'$group': {
    '_id': {
        'year': {'$year': '$timestamp'},
        'month': {'$month': '$timestamp'},
        'day': {'$dayOfMonth': '$timestamp'},
    },
    'count': {'$sum': 1},
}}
project = {'$project': {
    '_id': 0,
    'count': 1,
    'date': {'$concat': [{'$toString': "$_id.year"}, "-", {'$toString': "$_id.month"}, '-', {'$toString': "$_id.day"}]}
}}
sort = {
    '$sort': {
        '_id.year': 1,
        "_id.month": 1,
        "_id.day": 1
    }
}
print('--------------')
results = db['marketcontact'].aggregate([gropu_script, sort, project], allowDiskUse=True)

# results = db.block.find({'timestamp': {'$gt': datetime(2021, 5, 16), '$lt': datetime(2021, 5, 17)}})

data = list(results)
frame = pd.DataFrame(data)

frame.to_csv('market_contract每日交易量.csv', index=False)
