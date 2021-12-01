from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.providers import HTTPProvider
from concurrent.futures import ThreadPoolExecutor
import json
from utils.db import db
import time

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36"
w3 = Web3(HTTPProvider('https://api.roninchain.com/rpc',
                       request_kwargs={"headers": {"content-type": "application/json", "user-agent": USER_AGENT},
                                       'timeout': 10}))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
executor = ThreadPoolExecutor(max_workers=1000)

def pop_block(block):
    block.pop('transactions')
    block.pop('proofOfAuthorityData')
    block.pop('transactionsRoot')
    block.pop('logsBloom')
    block.pop('mixHash')
    block.pop('parentHash')
    block.pop('sha3Uncles')
    block.pop('stateRoot')


def pop_tran(tran):
    tran.pop('blockHash')
    tran.pop('v')
    tran.pop('r')
    tran.pop('s')


def getblock_and_transactions(block_number):
    if block_number % 1000 == 0:
        print('[{}]at {}'.format(block_number, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    block = {'number': block_number, 'hash': 'error'}
    transactions = {}
    try:
        block = json.loads(Web3.toJSON(w3.eth.get_block(block_number, True)))
        transactions = block['transactions']
        pop_block(block)
        block['tnumber'] = len(transactions)
        if transactions:
            [pop_tran(tran) for tran in transactions]

    except Exception as e:
        print(e)
    finally:
        db.block.insert_one(block)
        if transactions:
            db.transactions.insert_many(transactions)

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
for number in range(6400000 + 1, 7000000 + 1):
    executor.submit(getblock_and_transactions, number)
