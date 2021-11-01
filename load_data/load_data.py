import utils
from csv_handler import csv_handler
from input_models import column_model, source_model


sources = []
sources.append(source_model(
    link = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/kraj-okres-nakazeni-vyleceni-umrti.csv",
    columns = [
        column_model(0),
        column_model(1),
        column_model(3),
        column_model(4),
        column_model(5)
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
        column_model(0),
        column_model(1),
        column_model(2),
        column_model(3)
    ],
    filename = "new_cases"
))
sources.append(source_model(
    link = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-profese.csv",
    columns = [
        column_model(0),
        column_model(1),
        column_model(2),
        column_model(6),
        column_model(14),
        column_model(15),
        column_model(18)
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
        column_model(1),
        column_model(7),
        column_model(10)
    ],
    filename = "cities_new_cases"
))

#DO NOT DELETE --- TEMPLATE
"""
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

#delete all outdated data
utils.delete_dir_content(utils.data_dir())

#download new fresh data
for source in sources:
    csv_h = csv_handler(source.link, source.filename)
    if source.filename == "cities":
        data = csv_h.filter_cities(source.columns)
    elif source.filename == "regions_pop":
        data = csv_h.filter_regions(source.columns)
    elif source.filename == "cities_new_cases":
        data = csv_h.filter_cities_new_cases(source.columns)
    else:
        data = csv_h.filter_columns(source.columns)