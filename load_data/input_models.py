# input_models.py
# Proj: UPA 2021
# Authors: Matěj Sojka (xsojka04), Matěj Kudera (xkuder04), Honza Krejčí (xkrejc70)
# Models for download data selection and column manipulation

from typing import List

# Column model defines column that will be saved with belonging data manipulation function (default function returns same values)
class column_model:
    def __init__(self, index, func=lambda x:x):
        self.index = index
        self.func = func

# Source model defines data file that will by downloaded with columns that will by filtered
class source_model:
    def __init__(self, link, columns : List[column_model], filename):
        self.link = link
        self.columns = columns
        self.filename = filename

# END input_models.py