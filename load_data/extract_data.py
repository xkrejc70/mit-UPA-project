import utils
from db_manager import db_manager
from os import path
import csv  

suffix_part1 = "part1"
suffix_part2 = "part2"

#uklada selekty so souboru
def to_csv(data, path):
    with open(path, 'w', encoding='UTF8') as f:
        keys = data[0].keys()
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(data)

#EXAMPLE
def select0(db):
    #jmeno souboru
    name = "select0"
    #ziskani dat
    part1, part2 = db.select0()
    #ulozeni
    to_csv(part1, utils.path_part1(name))
    to_csv(part2, utils.path_part2(name))

# A1 - select age and region from new_cases
def selectA1(db):
    #jmeno souboru
    name = "selectA1"
    #ziskani dat
    part1, part2 = db.selectA1()
    #ulozeni
    to_csv(part1, utils.path_part1(name))
    to_csv(part2, utils.path_part2(name))

    

############################################
#main body
utils.delete_dir_content(utils.extracted_data_dir())

#connect to db --- takhle neni treba volat disconnect... zavola se sam
with db_manager() as db:
    select0(db)
    selectA1(db)
