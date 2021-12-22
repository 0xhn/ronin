from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.providers import HTTPProvider

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36"
w3 = Web3(HTTPProvider('https://api.roninchain.com/rpc',
                       request_kwargs={"headers": {"content-type": "application/json", "user-agent": USER_AGENT},
                                       'timeout': 10}))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)