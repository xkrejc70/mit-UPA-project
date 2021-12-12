# csv_handler.py
# Proj: UPA 2021
# Authors: Matěj Sojka (xsojka04), Matěj Kudera (xkuder04), Honza Krejčí (xkrejc70)
# CSV manipulation class

import csv, requests, utils, os
from input_models import column_model
from typing import List

# Class for downloading and filtering CSV data.
class csv_handler:
    def __init__(self, link, name, encoding = "utf-8-sig"):
        self.link = link
        self.encoding = encoding
        self.name = name
        self.path = os.path.join(utils.data_dir(), f"{self.name}.csv")
        self.path_tmp = os.path.join(utils.data_dir(), f"{self.name}_tmp.csv")
        self.download()

    # Download data to data folder from given url
    def download(self):
        response = requests.get(self.link, stream=True)
        response.encoding = 'utf-8-sig'
        response.raise_for_status()
        with open(self.path, 'wb') as handle:
            for block in response.iter_content(1024):
                handle.write(block)

    # Get file of 50 cities from static data folder
    def get_50_cities(self):
        top_50_cities = []
        with open(os.path.join(utils.static_data_dir(), 'top_50_cities.csv'), 'r') as csvfile:
            csv_top_50_cities = csv.reader(csvfile)
            for city in csv_top_50_cities:
                top_50_cities.append(city[0])
        return top_50_cities

    # Removes original file and repleces it with new filtered version.
    def tmp2origin(self):
        a = self.path + "a"
        os.rename(self.path, a)
        os.rename(self.path_tmp, self.path)
        os.remove(a)

############## File filtration functions ###################

    # Filter file to save only specified columns and apply optional column function where given
    def filter_columns(self, desired_columns : List[column_model]):
        with open(self.path, "r") as data_file:
            with open(self.path_tmp, "w") as tmp_file:
                reader = csv.reader(data_file)
                writer = csv.writer(tmp_file)
                header = next(reader)
                writer.writerow([header[dc.index] for dc in desired_columns])
                for row in reader:
                    if row == []:
                        continue
                    new_row = []
                    for dc in desired_columns:
                        new_row.append(dc.func(row[dc.index]))
                    writer.writerow(new_row)
        self.tmp2origin()

    # Filter 50 cities from 2020
    def filter_cities(self, desired_columns : List[column_model]):
        top_50_cities = self.get_50_cities()

        with open(self.path, "r") as data_file:
            with open(self.path_tmp, "w") as tmp_file:
                reader = csv.reader(data_file)
                writer = csv.writer(tmp_file)
                header = next(reader)
                writer.writerow([header[dc.index] for dc in desired_columns])
                for row in reader:
                    if row == []:
                        continue
                    if "2020" not in row[9] or row[12] not in top_50_cities:
                        continue 
                    new_row = []
                    for dc in desired_columns:
                        new_row.append(dc.func(row[dc.index]))
                    writer.writerow(new_row)
        self.tmp2origin()

    # Filter population of regions
    def filter_regions(self, desired_columns : List[column_model]):
        with open(self.path, "r") as data_file:
            with open(self.path_tmp, "w") as tmp_file:
                reader = csv.reader(data_file)
                writer = csv.writer(tmp_file)
                header = next(reader)
                writer.writerow([header[dc.index] for dc in desired_columns])
                for row in reader:
                    if row == []:
                        continue
                    # Filter only year 2020, regions (code 100) and both gender together (empty)
                    if "2020" not in row[9] or row[7] != "100" or row[4] != "" or row[5] != "":
                        continue 
                    new_row = []
                    for dc in desired_columns:
                        new_row.append(dc.func(row[dc.index]))
                    writer.writerow(new_row)
        self.tmp2origin()

    # Filter 50 cities
    def filter_cities_new_cases(self, desired_columns : List[column_model]):
        top_50_cities = self.get_50_cities()
        with open(self.path, "r") as data_file:
            with open(self.path_tmp, "w") as tmp_file:
                reader = csv.reader(data_file)
                writer = csv.writer(tmp_file)
                header = next(reader)
                writer.writerow([header[dc.index] for dc in desired_columns])
                for row in reader:
                    if row == []: continue
                    if row[6] not in top_50_cities: continue
                    new_row = []
                    for dc in desired_columns:
                        new_row.append(dc.func(row[dc.index]))
                    writer.writerow(new_row)
        self.tmp2origin()

# END csv_handler.py