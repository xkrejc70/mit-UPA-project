# load_data.py
# Proj: UPA 2021
# Authors: Matěj Sojka (xsojka04), Matěj Kudera (xkuder04), Honza Krejčí (xkrejc70)
# Data selection for downloading

import utils
from csv_handler import csv_handler
from input_models import column_model, source_model

# List of needed CSV data files
# Every file is defined by download url, needed columns (optinal is function for data transformation in specified clolumn) and save name 
"""
Imput data template

sources.append(source_model(
    link = "",
    columns = [
        column_model(),
        column_model(),
        column_model()
    ],
    filename = ""
))
"""

sources = []
sources.append(source_model(
    link = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/kraj-okres-nakazeni-vyleceni-umrti.csv",
    columns = [
        column_model(1),
        column_model(2),
        column_model(4),
        column_model(5),
        column_model(6)
    ],
    filename = "regions_daily"
))
sources.append(source_model(
    link = "https://www.czso.cz/documents/62353418/143522504/130142-21data043021.csv/760fab9c-d079-4d3a-afed-59cbb639e37d?version=1.1",
    columns = [
        column_model(1),
        column_model(4, utils.rename_gender),
        column_model(11, utils.all_before_bracket),
        column_model(12)
    ],
    filename = "cities"
))
sources.append(source_model(
    link = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/osoby.csv",
    columns = [
        column_model(1),
        column_model(2),
        column_model(3),
        column_model(4)
    ],
    filename = "new_cases"
))
sources.append(source_model(
    link = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-profese.csv",
    columns = [
        column_model(1),
        column_model(2),
        column_model(3),
        column_model(7),
        column_model(15),
        column_model(16),
        column_model(19)
    ],
    filename = "vaccinated"
))
sources.append(source_model(
    link = "https://www.czso.cz/documents/62353418/143522504/130142-21data043021.csv/760fab9c-d079-4d3a-afed-59cbb639e37d?version=1.1",
    columns = [
        column_model(1),
        column_model(12)
    ],
    filename = "regions_pop"
))

sources.append(source_model(
    link = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/obce.csv",
    columns = [
        column_model(2),
        column_model(8),
        column_model(11)
    ],
    filename = "cities_new_cases"
))

# Delete all outdated data
utils.delete_dir_content(utils.data_dir())

# Download new fresh data
print("Downloading data:")

for source in sources:
    print(f"Downloading start: {source.filename}")
    csv_h = csv_handler(source.link, source.filename)
    print(f"Downloading end: {source.filename}")

    # Apply specific filtration function
    if source.filename == "cities":
        data = csv_h.filter_cities(source.columns)
    elif source.filename == "regions_pop":
        data = csv_h.filter_regions(source.columns)
    elif source.filename == "cities_new_cases":
        data = csv_h.filter_cities_new_cases(source.columns)
    else:
        data = csv_h.filter_columns(source.columns)

    print(f"Filtering end: {source.filename}")

print("Download done")

# END load_data.py