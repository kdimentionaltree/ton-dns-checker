from dnschecker.core.checker import DHTChecker
from dnschecker.core.cache import CachedDHTChecker


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


dht_checker_dep = DhtCheckerDep()
