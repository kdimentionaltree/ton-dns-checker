import ring
import redis

from dnschecker.core.checker import DHTChecker


rc = redis.StrictRedis('dns-checker-cache', port=6379)


class CachedDHTChecker(DHTChecker):
    def __ring_key__(self):
        return ('config_path', 'resolve_binary_path', 'ping_binary_path', 'port', 'timeout', tuple(self.working_status.values()))

    @ring.redis(rc, expire=10, coder='json')
    def check_adnl(self, adnl):
        return self.check_adnl_parallel(adnl)
