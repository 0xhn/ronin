from utils.db import db

for i in range(500000 + 1, 7000000 + 1):
    if i % 10000 == 0:
        print('已经处理到{}'.format(i))
    try:
        block = db.block.find_one({'number': i})
        trans_num = block['tnumber']
        if trans_num > 0:
            trans = db.transactions.find({'blockNumber': i}).count()
            if trans_num != trans:
                print('不匹配[{}]'.format(i))
    except Exception as e:
        print('出现异常：{}'.format(i))
