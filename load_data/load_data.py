import utils
from csv_handler import csv_handler

utils.delete_dir_content(utils.data_dir())

sources = [("https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/kraj-okres-nakazeni-vyleceni-umrti.csv", [1,2,3], "mzcr"),
("https://www.czso.cz/documents/62353418/143522504/130142-21data043021.csv/760fab9c-d079-4d3a-afed-59cbb639e37d?version=1.1", [10,11,12], "statistika")]

for source in sources:
    csv_h = csv_handler(source[0])
    csv_h.print_sample()
    csv_h.filter_columns(source[1], filename = source[2])
    #csv_h.filter_columns([1,2,3])