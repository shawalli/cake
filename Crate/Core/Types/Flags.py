
import List

class Flags(List.List):
    def init(self, iterable=list(), prefix='', suffix=''):
        List.__init__(self, iterable)
        self.prefix = prefix
        self.suffix = suffix

    def prepare(self):
        s = [self.prefix + f + self.suffix for f in self]
        s = ' '.join(s)
        return s
