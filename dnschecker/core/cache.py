import ring
import redis

import aioredis

from ring.func.asyncio import Aioredis2Storage

from dnschecker.core.dht.dht_checker import DHTChecker
from dnschecker.core.dns.dns_checker import DNSResolver


rc = redis.StrictRedis(host='dns-checker-cache', port=6379)
arc = aioredis.from_url(f'redis://dns-checker-cache:6379')


class CachedDHTChecker(DHTChecker):
    def __ring_key__(self):
        return ('config_path', 'resolve_binary_path', 'ping_binary_path', 'port', 'timeout', tuple(self.working_status.values()))

    @ring.redis(rc, expire=10, coder='json')
    def check_adnl(self, adnl):
        return self.check_adnl_parallel(adnl)


class CachedDNSResolver(DNSResolver):
    def __ring_key__(self):
        return ('config_path', tuple(self.liteservers))

    @ring.aioredis(arc, expire=10, coder='pickle', storage_class=Aioredis2Storage)
    async def resolve(self, domain, category):
        return await self._resolve(domain, category)
