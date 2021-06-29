from ..globals import *
from .frame import Frame


class BaseReplacer():

    def __init__(self):
        super().__init__()
        self.framearray = [Frame(bytearray(PAGESIZE), 0, False, False)]*BUFFERSIZE

    def findFrame(self, pageno: int):
        for frame in self.framearray:
            if frame.pageno == pageno:
                return frame
        else:
            return None



class SequentialReplacer(BaseReplacer):

    def __init__(self):
        super().__init__()


    def replacer(self, frame: Frame):
        for i in range(BUFFERSIZE):
            if (chosen := self.framearray.pop(0)).pinned:
                self.framearray.append(chosen)
            else:
                break

        else:
            raise Exception("All buffer frames pinned")
        
        self.framearray.append(frame)
        return chosen


class FIFOReplacer(BaseReplacer):

    def __init__(self):
        super().__init__()

    def replacer(self, frame: Frame):
        pass