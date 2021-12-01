from utils.db import db


def filter_transfer(tran):
    return tran['input'].startswith('0x42842e0e')


def page_query(page, page_size):
    skip_number = (page - 1) * page_size
    axie_trans = list(db['axiecontact'].find(
        {},
        {'from': 1, 'hash': 1, 'input': 1, 'timestamp': 1}).limit(page_size).skip(skip_number))
    data = [tran for tran in axie_trans if filter_transfer(tran)]
    return data


a = 401 + 1
print(a)
for i in range(1, a + 1):
    result = page_query(i, 200000)
    db['axiecontact_transfer'].insert_many(result)
