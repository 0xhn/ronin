from utils.db import db
from datetime import datetime

for i in range(7000000 + 1, 8800000 + 1):
    if i % 10000 == 0:
        print('已经处理到{}'.format(i))
    try:
        block = db.block.find_one({'number': i})
        block['timestamp'] = datetime.utcfromtimestamp(block['timestamp'])
        db.block.update_one({'number': i}, {'$set': block})
    except Exception as e:
        print('出现异常：{}'.format(i))
