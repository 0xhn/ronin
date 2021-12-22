from utils.db import db

for i in range(500000 + 1, 8800000 + 1):
    block_time = db['block'].find_one({'number': i}, {'timestamp': 1})
    db['transactions'].update_many({'blockNumber': i}, {'$set': {'timestamp': block_time['timestamp']}})
    if i % 10000 == 0:
        print('已经处理到{}'.format(i))
