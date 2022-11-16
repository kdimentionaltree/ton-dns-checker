from fastapi.security.api_key import APIKeyHeader, APIKeyQuery
from fastapi import Depends

from dnschecker.core.cache import CachedDHTChecker, CachedDNSResolver
from loguru import logger


class DhtCheckerDep:
    def __init__(self):
        self.checker = None

    def init(self):
        self.checker = CachedDHTChecker('/run/secrets/global-config',
                                        '/app/binaries/dht-resolve',
                                        '/app/binaries/dht-ping-servers',
                                        port=32768)
        return self
    
    def __call__(self):
        if self.checker is None:
            self.init()
        return self.checker


class DnsResolverDep:
    def __init__(self):
        self.resolver = None
    
    async def init(self, loop):
        self.resolver = CachedDNSResolver('/run/secrets/global-config', loop)
        await self.resolver.init()

    def __call__(self):
        return self.resolver


dht_checker_dep = DhtCheckerDep()
dns_resolver_dep = DnsResolverDep()


# empty api key dependency for openapi schema
def api_key_dep(api_key_header: APIKeyHeader=Depends(APIKeyHeader(name='X-API-Key', auto_error=False)),
                api_key_query: APIKeyQuery=Depends(APIKeyQuery(name='api_key', auto_error=False))):
    pass
