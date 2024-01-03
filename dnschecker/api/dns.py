import traceback
import asyncio

from fastapi import FastAPI
from fastapi import Query, Depends

from dnschecker.schemas.models import (
    DhtNodeModel, 
    DhtResolveModel,
    LiteserverModel,
    LiteserverResolveModel
)
from dnschecker.core.dht.dht_checker import DHTChecker
from dnschecker.core.dns.dns_checker import DNSResolver
from dnschecker.api.deps import dht_checker_dep, dns_resolver_dep, api_key_dep
from typing import List

from loguru import logger


api = FastAPI(docs_url='/', dependencies=[Depends(api_key_dep)])

def create_dns_routes(api: FastAPI):
    @api.get('/dhts', response_model=List[DhtNodeModel])
    async def get_dhts(checker: DHTChecker=Depends(dht_checker_dep)):
        try:
            res = []
            for idx, dht, is_online in checker.dht_status:
                # logger.error(f"{idx}, {dht}, {is_online}")
                res.append(DhtNodeModel.from_dht_node(idx, dht, is_online))
            return res
        except:
            logger.critical(f"METHOD: /dhts. Error: {traceback.format_exc()}")


    @api.get('/resolve', response_model=List[DhtResolveModel])
    async def get_resolve(adnl: str=Query(..., example='2D7CF7C6238E4E8B7DA16B0707222C3A95C8DB6A8E4FA4F101052306130EEFDC'), 
                        checker: DHTChecker=Depends(dht_checker_dep)):
        try:
            adnl = adnl.upper().strip()
            logger.info(f'/resolve with adnl: "{adnl}"')
            res = checker.check_adnl(adnl)
            return [DhtResolveModel.parse_obj(obj) for obj in res.values()]
        except:
            logger.critical(f"METHOD: /resolve. Error: {traceback.format_exc()}")
        return []    


    @api.get('/liteservers', response_model=List[LiteserverModel])
    async def get_liteservers(resolver: DNSResolver=Depends(dns_resolver_dep)):
        try:
            return [
                LiteserverModel.from_liteserver(idx, ls, True)
                for idx, ls in enumerate(resolver.liteservers)
            ]
        except:
            logger.critical(f"METHOD: /liteservers. Error: {traceback.format_exc()}")
        return []


    @api.get('/ls_resolve', response_model=List[LiteserverResolveModel])
    async def get_ls_resolve(domain: str=Query(..., example='foundation.ton'),
                            category: str=Query('site', examplee='site'),
                            resolver: DNSResolver=Depends(dns_resolver_dep)):
        try:
            res = await resolver.resolve(domain, category)
            if category == 'site': 
                return [LiteserverResolveModel.parse_obj({'adnl': adnl}) for adnl in res]
            if category == 'wallet':
                return [LiteserverResolveModel.parse_obj({'wallet': wallet}) for wallet in res]
            raise ValueError(f"unknown category '{category}'")
        except:
            logger.critical(f"METHOD: /ls_resolve. Error: {traceback.format_exc()}")
        return []
