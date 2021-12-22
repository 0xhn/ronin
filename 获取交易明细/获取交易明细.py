import time
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import json

from utils.db import db
from utils.w3client import w3
from web3 import Web3

from concurrent import futures
import queue


class ThreadPoolExecutorWithQueueSizeLimit(futures.ThreadPoolExecutor):
    def __init__(self, maxsize=50, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._work_queue = queue.Queue(maxsize=maxsize)


def pop_receipt(receipt):
    receipt.pop('blockHash')
    receipt.pop('logsBloom')


def get_transaction_receipt(hash):
    receipt = {'transactionHash': hash, 'status': 3}
    try:
        receipt = json.loads(Web3.toJSON(w3.eth.get_transaction_receipt(hash)))
        pop_receipt(receipt)
    except Exception as e:
        print('[{}] is error'.format(hash))
    finally:
        db['transaction_receipts'].insert_one(receipt)


executor = ThreadPoolExecutorWithQueueSizeLimit(maxsize=200000, max_workers=800)
# 500-250
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
for i in range(8000000 + 1, 8800000 + 1):
    tran_hashs = list(db['transactions'].find({'blockNumber': i}, {'hash': 1, '_id': 0}))
    all_task = [executor.submit(get_transaction_receipt, tran_hash['hash']) for tran_hash in tran_hashs]
    # wait(all_task, return_when=ALL_COMPLETED)

# result = json.loads(Web3.toJSON(w3.eth.get_transaction_by_block(500040,0)))
# print(result)
