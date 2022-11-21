import asyncio
import json

from pytonlib import TonlibClient
from dnschecker.core.dns.utils import _resolve_impl, encode_domain
from dnschecker.schemas.liteserver import Liteserver

from pathlib import Path

from loguru import logger


mainnet_root_dns_address = 'Ef-OJd0IF0yc0xkhgaAirq12WawqnUoSuE9RYO3S7McG6lDh'


class DNSResolver:
    def __init__(self, config_path, loop):
        self.config_path = config_path
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)

        self.loop = loop

        self.clients = {}
        for idx in range(len(self.config['liteservers'])):
            keystore_dir = f'/tmp/ton_keystore/worker_{idx}'
            Path(keystore_dir).mkdir(parents=True, exist_ok=True)
            self.clients[idx] = TonlibClient(idx, 
                                             self.config, 
                                             keystore_dir,
                                             loop=loop,
                                             tonlib_timeout=10)

        self.liteservers = [Liteserver.parse_obj(x) for x in self.config['liteservers']]

    # async def _ping_loop(self):
    #     while True:
    #         tasks = []
    #         for idx, client in self.clients.items():
    #             task = client.get_masterchain_info()
    #             tasks.append(task)
    #         results = asyncio.wait(tasks)
    #         for task in results:
    #             try:
    #                 task.result()
    #             except:
    #                 pass

        
    async def init(self):
        coro_list = [client.init() for client in self.clients.values()]
        await asyncio.wait(coro_list)

        # coro_list = [client.sync_tonlib() for client in self.clients.values()]
        # await asyncio.wait(coro_list)
        return self

    async def _resolve_ls(self, idx, domain_raw, category):
        try:
            res = await _resolve_impl(self.clients[idx],
                                mainnet_root_dns_address,
                                domain_raw,
                                category,
                                one_step=False)
            return res
        except Exception as ee:
            logger.warning(f"LS{idx:03d} resolve failed: {ee}")
        return None

    async def _resolve(self, domain, category):
        domain_raw = encode_domain(domain.strip())

        tasks = [self._resolve_ls(idx, domain_raw, category)
                 for idx in self.clients]
        done, _ = await asyncio.wait(tasks)
        result = [task.result() for task in done]
        return result
    
    async def resolve(self, domain, category):
        return await self._resolve(domain, category)
