import asyncio

from eth_typing import Address
from web3 import Web3, AsyncWeb3

ext_eth_rpc_node = "https://rpc-mainnet-ethereum.forbole.com?apikey=lmPL2NNKtjE7nLpGZEZBwuFAOonrkBQD"
query_address: str = '0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5'

w3 = Web3(Web3.HTTPProvider(ext_eth_rpc_node))
print(w3.from_wei(w3.eth.get_balance(query_address, 'latest'), 'ether'))



