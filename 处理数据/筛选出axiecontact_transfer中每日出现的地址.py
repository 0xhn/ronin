from utils.db import db
from utils.contact_decoder import contact


def decoder_input(tran):
    decoder_input = contact.decode_function_input(tran['input'])
    to = decoder_input[1]['_to']
    token_id = decoder_input[1]['_tokenId']
    return to, token_id


def page_query(page, page_size):
    skip_number = (page - 1) * page_size
    axie_trans = list(db['axiecontact_transfer'].find(
        {},
        {'_id': 1, 'input': 1}).limit(page_size).skip(skip_number))
    for tran in axie_trans:
        to, token_id = decoder_input(tran)
        db['axiecontact_transfer'].update_one({'_id': tran['_id']}, {'$set': {'to': to, 'token_id': token_id}})


a = 401 + 1
print(a)
for i in range(1, a + 1):
    result = page_query(i, 200000)
