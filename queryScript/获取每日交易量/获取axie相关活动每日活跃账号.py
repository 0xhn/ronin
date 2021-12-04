from utils.db import db
import pandas as pd

match_axie_market_contract = {'$match': {
    'to': {'$in': ['0x32950db2a7164aE833121501C797D79E7B79d74C', '0x213073989821f738A7BA3520C3D31a1F9aD31bBd']}}}

project1 = {'$project': {
    'from': '$from',
    'year': {'$year': '$timestamp'},
    'month': {'$month': '$timestamp'},
    'day': {'$dayOfMonth': '$timestamp'},
}}

gropu_date_script = {'$group': {
    '_id': {
        'year': '$year',
        'month': '$month',
        'day': '$day'
    },
    'address': {'$addToSet': '$from'}
}}
sort = {
    '$sort': {
        'year': 1,
        "month": 1,
        "day": 1
    }
}
project2 = {'$project': {
    '_id': 0,
    'count': {'$size': '$address'},
    'date': {'$concat': [{'$toString': "$_id.year"}, "-", {'$toString': "$_id.month"}, '-', {'$toString': "$_id.day"}]}
}}
print('--------------')
results = db['transactions'].aggregate(
    [project1, gropu_date_script, sort, project2],
    allowDiskUse=True)

# results = db.block.find({'timestamp': {'$gt': datetime(2021, 5, 16), '$lt': datetime(2021, 5, 17)}})

data = list(results)
frame = pd.DataFrame(data)

frame.to_csv('market_contract每日活跃地址量.csv', index=False)
