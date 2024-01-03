import traceback
import asyncio

from fastapi import FastAPI, Query, Depends
from typing import List
from loguru import logger

from dnschecker.schemas.models import (
    DhtNodeModel, DhtResolveModel, LiteserverModel, LiteserverResolveModel
)
from dnschecker.core.dht.dht_checker import DHTChecker
from dnschecker.core.dns.dns_checker import DNSResolver
from dnschecker.api.deps import dht_checker_dep, dns_resolver_dep, api_key_dep

# Initialize FastAPI app with specified documentation URL and dependencies
api = FastAPI(docs_url='/', dependencies=[Depends(api_key_dep)])

def create_dns_routes(api: FastAPI):
    # Define a route to get the status of DHT nodes
    @api.get('/dhts', response_model=List[DhtNodeModel])
    async def get_dhts(checker: DHTChecker=Depends(dht_checker_dep)):
        try:
            res = []
            # Retrieve status for each DHT node and append it to the response
            for idx, dht, is_online in checker.dht_status:
                res.append(DhtNodeModel.from_dht_node(idx, dht, is_online))
            return res
        except:
            # Log any errors that occur
            logger.critical(f"METHOD: /dhts. Error: {traceback.format_exc()}")

    # Define a route to resolve an ADNL address
    @api.get('/resolve', response_model=List[DhtResolveModel])
    async def get_resolve(adnl: str=Query(..., example='2D7CF7C6238E4E8B7DA16B0707222C3A95C8DB6A8E4FA4F101052306130EEFDC'), 
                          checker: DHTChecker=Depends(dht_checker_dep)):
        try:
            adnl = adnl.upper().strip()
            # Resolve the ADNL address using the DHTChecker
            res = checker.check_adnl(adnl)
            return [DhtResolveModel.parse_obj(obj) for obj in res.values()]
        except:
            logger.critical(f"METHOD: /resolve. Error: {traceback.format_exc()}")

    # Define a route to get information about liteservers
    @api.get('/liteservers', response_model=List[LiteserverModel])
    async def get_liteservers(resolver: DNSResolver=Depends(dns_resolver_dep)):
        try:
            # Return information about each liteserver
            return [LiteserverModel.from_liteserver(idx, ls, True) for idx, ls in enumerate(resolver.liteservers)]
        except:
            logger.critical(f"METHOD: /liteservers. Error: {traceback.format_exc()}")

    # Define a route to resolve a domain for liteservers
    @api.get('/ls_resolve', response_model=List[LiteserverResolveModel])
    async def get_ls_resolve(domain: str=Query(..., example='foundation.ton'),
                             category: str=Query('site', example='site'),
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

# Other parts of the FastAPI app configuration...
