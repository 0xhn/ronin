from utils.db import db
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=20)

block_time_dict = {}


def get_block_time(tran):
    data = {}
    if tran['blockNumber'] not in block_time_dict.keys():
        block_time = db['block'].find_one({'number': tran['blockNumber']}, {'timestamp': 1})
        block_time_dict[tran['blockNumber']] = block_time['timestamp']
    data['timestamp'] = block_time_dict[tran['blockNumber']]
    data['from'] = tran['from']
    data['hash'] = tran['hash']
    data['input'] = tran['input']
    data['blockNumber'] = tran['blockNumber']
    return data


def page_query(page, page_size):
    skip_number = (page - 1) * page_size
    axie_trans = db['transactions'].find(
        {'to': '0x213073989821f738A7BA3520C3D31a1F9aD31bBd'},
        {'from': 1, 'hash': 1, 'input': 1, 'blockNumber': 1}).limit(page_size).skip(skip_number)
    data = [get_block_time(tran) for tran in axie_trans]
    return data


a = 251 + 1
print(a)
for i in range(1, a + 1):
    result = page_query(i, 200000)
    db['marketcontact'].insert_many(result)
