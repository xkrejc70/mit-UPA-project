import csv, requests, utils, os, io
from input_models import column_model
from typing import List

class csv_handler:
    def __init__(self, link, name, encoding = "utf-8-sig"):
        self.link = link
        self.encoding = encoding
        self.name = name
        self.load()
        self.header = next(self.reader)
        self.rows = [row for row in self.reader if row != []]

    def load(self):
        request = requests.get(self.link)
        request.encoding = 'utf-8-sig'
        data = request.text.split('\n')
        self.reader = csv.reader(data)

    def filter_columns(self, desired_columns : List[column_model], filename=None):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([self.header[dc.index] for dc in desired_columns])
        for row in self.rows:
            new_row = []
            for dc in desired_columns:
                new_row.append(dc.func(row[dc.index]))
            writer.writerow(new_row)
        if filename is not None:
            utils.write_stringio(output, filename)
        return output

    def filter_cities(self, desired_columns : List[column_model], filename=None):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([self.header[dc.index] for dc in desired_columns])

        # Filter 50 cities from 2020
        with open(utils.static_data_dir() + '/top_50_cities.csv', 'r') as csvfile:
            csv_top_50_cities = csv.reader(csvfile)

            top_50_cities = []
            for city in csv_top_50_cities:
                top_50_cities.append(city[0])

        for row in self.rows:
            if "2020" not in row[9] or row[12] not in top_50_cities:
                continue 
            new_row = []
            for dc in desired_columns:
                new_row.append(dc.func(row[dc.index]))
            writer.writerow(new_row)
        utils.write_stringio(output, filename)
        return output

    def group_column(self, index, data : io.StringIO = None):
        if data is None:
            rows = self.rows
            header = self.header
        else:
            reader = csv.reader(data.getvalue().split('\n'))
            header = next(reader)
        print()
        print(f'Group by of column: "{header[index]}"')
        rows = [row for row in reader if row != []]
        group_count_dict = {}
        for row in rows:
            group_count_dict[f"{row[index]}"] = group_count_dict.get(f"{row[index]}", 0) + 1 
        for group_count in sorted(group_count_dict.items()):
            print(f'Text: "{group_count[0]}", Count: "{group_count[1]}"')

    def print_sample(self):
        print(f'\n{self.name}')
        print(f'Header: {self.header}')
        print(f'First row: {self.rows[0]}')
        print(f'Last row: {self.rows[-1]}')
        print(f'Row count: {len(self.rows)}')