from ..globals import *
from .framedata import FDA



class SequencialReplacer(FDA):

    def __init__(self):
        super().__init__()

    def chooseEvicted(self):
        # TODO replace with for-else that throws exception
        while (chosen := self.fda.pop(0)).pinned:
            self.fda.append(chosen)
        
        self.fda.append(chosen)
        return chosen.frameno
        