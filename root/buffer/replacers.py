from ..globals import *
from .frame import Frame


def sequentialReplaceWith(frame: Frame, framearray: list):
    for i in range(BUFFERSIZE):
        if (chosen := framearray.pop(0)).pinned:
                framearray.append(chosen)
        else:
            break

    else:
        raise Exception("All buffer frames pinned")
        
    framearray.append(frame)
    return chosen


def fifoReplaceWith(frame: Frame, framearray: list):
    pass