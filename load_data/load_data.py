import utils
from csv_handler import csv_handler
from input_models import column_model, source_model

utils.delete_dir_content(utils.data_dir())

sources = []
sources.append(source_model(
    link = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/kraj-okres-nakazeni-vyleceni-umrti.csv",
    columns = [
        column_model(1),
        column_model(2),
        column_model(3)
    ],
    filename = "mzcr"
))
sources.append(source_model(
    link = "https://www.czso.cz/documents/62353418/143522504/130142-21data043021.csv/760fab9c-d079-4d3a-afed-59cbb639e37d?version=1.1",
    columns = [
        column_model(10),
        column_model(11, utils.all_before_bracket),
        column_model(12)
    ],
    filename = "statistika"
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
# TODO size: 2GB
"""
sources.append(source_model(
    link = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-profese.csv",
    columns = [
        column_model(0),
        column_model(2),
        column_model(14),
        column_model(15),
        column_model(18)
    ],
    filename = "vaccinated"
))
"""

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

for source in sources:
    csv_h = csv_handler(source.link, source.filename)
    csv_h.print_sample()
    data = csv_h.filter_columns(source.columns, filename = source.filename)
    if source.filename == "statistika":
        csv_h.group_column(1,data)