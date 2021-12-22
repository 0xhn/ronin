from decimal import Decimal
from bson.decimal128 import Decimal128
from pymongo import UpdateOne

from utils.db import db
from utils.contact_decoder import contact


def decoder_input(tran):
    seller = None
    bidAmount = None
    try:
        decoder_input = contact.decode_function_input(tran['input'])
        seller = decoder_input[1]['_seller']
        bidAmount = decoder_input[1]['_bidAmount']
        if bidAmount > 0xffffffff:
            bidAmount = Decimal128(Decimal(bidAmount) / 10 ** 18)
    except Exception as e:
        print(tran['_id'])
        print(e)
    return seller, bidAmount


def page_query(page, page_size):
    skip_number = (page - 1) * page_size
    axie_trans = list(db['marketcontact_buy'].find(
        {},
        {'_id': 1, 'input': 1}).limit(page_size).skip(skip_number).sort([('_id', 1)]))
    bulk_list = []
    for tran in axie_trans:
        seller, bidAmount = decoder_input(tran)
        bulk_list.append(UpdateOne({'_id': tran['_id']},
                                   {'$set': {'seller': seller, 'price': bidAmount}}))
    db['marketcontact_buy'].bulk_write(bulk_list)


a = 137 + 1
print(a)
for i in range(1, a + 1):
    print(i)
    result = page_query(i, 100000)
