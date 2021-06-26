import mmap
from ..globals.globalconst import GlobalConst

class Storage(GlobalConst):
    
    def __init__(self, filename='storage.toydb'):
        super().__init__()
        self.f = open(filename, "a+b")
        self.mm = mmap.mmap(f.fileno(), 0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self.mm.close()
        self.f.close()
        