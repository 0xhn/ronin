from utils.db import db


def filter_transfer(tran):
    return tran['input'].startswith('0x4d51bfc4')


def page_query(page, page_size):
    skip_number = (page - 1) * page_size
    axie_trans = list(db['marketcontact'].find(
        {},
        {'from': 1, 'hash': 1, 'input': 1, 'timestamp': 1}).limit(page_size).skip(skip_number))
    data = [tran for tran in axie_trans if filter_transfer(tran)]
    return data


a = 251 + 1
print(a)
for i in range(1, a + 1):
    result = page_query(i, 200000)
    db['marketcontact_buy'].insert_many(result)
