import asyncio
import json
import time
from asyncio.log import logger

import requests
from eth_account import account, Account
from eth_typing import Address
from web3 import Web3, AsyncWeb3
from websockets import connect

ext_eth_rpc_node = "https://rpc-mainnet-ethereum.forbole.com?apikey=lmPL2NNKtjE7nLpGZEZBwuFAOonrkBQD"
ext_eth_rpc_node_block_pi = 'https://ethereum.blockpi.network/v1/rpc/e1cf34328f54212022c29bea0fc2d3f2ac8ea88b'
ext_eth_wss_node_block_pi = 'wss://ethereum.blockpi.network/v1/ws/e1cf34328f54212022c29bea0fc2d3f2ac8ea88b'
ext_eth_wss_alchemy = 'wss://eth-mainnet.g.alchemy.com/v2/o8X3Wvkhu3UUny2NVp9A-2yHSGlU8DYj'
ext_infura_rpc_node = 'https://mainnet.infura.io/v3/41c2b28427ac4d7b9a9124c440402ee4'

web3 = Web3(Web3.HTTPProvider(ext_infura_rpc_node))


async def get_eth_tx_detail():
    while True:
        try:
            async with connect(ext_eth_wss_alchemy) as ws:
                await ws.send(json.dumps({
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "eth_subscribe",
                    "params": ['alchemy_pendingTransactions',
                               {
                                   'hashesOnly': False
                               }
                               ],
                }))
                resp = await ws.recv()
                logger.info(f'connect wss, return resp: ', {resp})
                while True:
                    message = await asyncio.wait_for(ws.recv(), timeout=15)
                    result = json.dumps(json.loads(message)['params']['result'])
                    print(result)
                    
        except Exception as e:
            logger.error(f'Get trade Error: ', {e})
            await asyncio.sleep(0, 5)
            
            
def simulate_execution(tx: dict):
    if not web3.is_connected():
        print("Failed to connect to Ethereum network!")
    else:
        print("Successfully connected to Ethereum network")
    return web3.eth.call(tx, block_identifier='pending')


if __name__ == '__main__':
    asyncio.run(get_eth_tx_detail())
    # current_block = web3.eth.get_block('latest')
    # base_fee = current_block['baseFeePerGas'] * 2
    # transaction = {
    #     'from': web3.to_checksum_address('0x1ccc30a58dfffc6934592fa78b5ec1bf83cdade5'),  # 发送方地址
    #     'to': web3.to_checksum_address('0x65f7ba4ec257af7c55fd5854e5f6356bbd0fb8ec'),  # 接收方地址或合约地址
    #     'nonce': '0x2df',
    #     'value': 0x0,  # 发送的以太币数量
    #     'gas': base_fee,  # Gas限制
    #     'gasPrice': 0x690fbccd4,  # Gas价格
    #     'data': '0x9ee679e800000000000000000000000000000000000000000000001cce0725ee5d851e69',  # 调用数据，如果是合约调用
    #     'chainId': 1  # 链ID，主网为1
    # }
    # execution = simulate_execution(transaction)
    # execution.hex()
    
    
    