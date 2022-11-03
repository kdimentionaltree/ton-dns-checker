from dnschecker.core.checker import DHTChecker


class DhtCheckerDep:
    def __init__(self):
        self.checker = None

    def init(self):
        self.checker = DHTChecker('/run/secrets/global-config',
                                  '/app/binaries/dht-resolve',
                                  '/app/binaries/dht-ping-ser',
                                  port=32768)
        return self
    
    def __call__(self):
        if self.checker is None:
            self.init()
        return self.checker
