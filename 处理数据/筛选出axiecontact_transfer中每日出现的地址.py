from pymongo import UpdateOne

from utils.db import db
from utils.contact_decoder import contact


def decoder_input(tran):
    to = ''
    token_id = ''
    try:
        decoder_input = contact.decode_function_input(tran['input'])
        to = decoder_input[1]['_to']
        token_id = decoder_input[1]['_tokenId']
        if token_id > 0xffffffff:
            to = ''
            token_id = ''
    except Exception as e:
        print('[{}]is error,because [{}]'.format(tran['_id'], e))
    return to, token_id


def page_query(page, page_size):
    skip_number = (page - 1) * page_size
    axie_trans = list(db['axiecontact_transfer'].find(
        {},
        {'_id': 1, 'input': 1, 'token_id': 1}).limit(page_size).skip(skip_number).sort([('_id', 1)]))
    bulk_list = []
    for tran in axie_trans:
        if 'token_id' in tran.keys():
            continue
        to, token_id = decoder_input(tran)
        bulk_list.append(UpdateOne({'_id': tran['_id']},
                                   {'$set': {'to': to, 'token_id': token_id}}))
    if bulk_list:
        db['axiecontact_transfer'].bulk_write(bulk_list)
    #     try:
    #         db['axiecontact_transfer'].update_one({'_id': tran['_id']}, {'$set': {'to': to, 'token_id': token_id}})
    #     except Exception as e:
    #         print(tran['_id'])


a = 442 + 1

for i in range(1, a + 1):
    page_query(i, 100000)
    print(i)
