import asyncio
import json
import time
from asyncio.log import logger

from eth_typing import Address
from web3 import Web3, AsyncWeb3
from web3.middleware import geth_poa_middleware
from websockets import connect

ext_eth_rpc_node = "https://rpc-mainnet-ethereum.forbole.com?apikey=lmPL2NNKtjE7nLpGZEZBwuFAOonrkBQD"
ext_eth_rpc_node_block_pi = 'https://ethereum.blockpi.network/v1/rpc/e1cf34328f54212022c29bea0fc2d3f2ac8ea88b'
ext_eth_wss_node_block_pi = 'wss://ethereum.blockpi.network/v1/ws/e1cf34328f54212022c29bea0fc2d3f2ac8ea88b'
ext_eth_wss_alchemy = 'wss://eth-mainnet.g.alchemy.com/v2/o8X3Wvkhu3UUny2NVp9A-2yHSGlU8DYj'

w3 = Web3(Web3.HTTPProvider(ext_eth_rpc_node_block_pi))


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
            

if __name__ == '__main__':
    asyncio.run(get_eth_tx_detail())
    