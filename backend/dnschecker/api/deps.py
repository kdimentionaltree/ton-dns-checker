from dnschecker.core.checker import DHTChecker


class DhtCheckerDep:
    def __init__(self):
        self.checker = None

    def init(self):
        self.settings = DHTChecker()
        return self
    
    def __call__(self):
        if self.settings is None:
            self.init()
        return self.settings