import utils
from typing import List

class column_model:
    def __init__(self, index, func=lambda x:x):
        self.index = index
        self.func = func

class source_model:
    def __init__(self, link, columns : List[column_model], filename):
        self.link = link
        self.columns = columns
        self.filename = filename