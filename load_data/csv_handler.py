import csv, requests, utils, os, io
from typing import List

class csv_handler:
    def __init__(self, link, encoding = "utf-8-sig"):
        self.link = link
        self.encoding = encoding
        self.load()
        self.header = next(self.reader)
        self.rows = [row for row in self.reader if row != []]

    def load(self):
        request = requests.get(self.link)
        request.encoding = 'utf-8-sig'
        data = request.text.split('\n')
        self.reader = csv.reader(data)

    def filter_columns(self, desired_columns: List[int], filename=None):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([self.header[dc] for dc in desired_columns])
        for row in self.rows:
            writer.writerow([row[dc] for dc in desired_columns])
        if filename is not None:
            utils.write_stringio(output, filename)
        return output

    def print_sample(self):
        print(self.header)
        print(self.rows[0])
        print(self.rows[-1])
        print(len(self.rows))