from ..page.basepage import BasePage

class Frame():

    def __init__(self, dirty: bool=False, pinned: bool=False, page: BasePage=None):
        super().__init__()
        self.dirty = dirty
        self.pinned = pinned
        self.page = page