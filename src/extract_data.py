import utils
from db_manager import db_manager
from os import path
import csv

#uklada selekty so souboru
def to_csv(data, path):
    with open(path, 'w', encoding='UTF8') as f:
        keys = data[0].keys()
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(data)

# A1 - select age and region from new_cases
def selectA1(db):
    name = "selectA1"
    print("- " + name)
    data = db.selectA1()
    to_csv(data, utils.path_extracted_data(name))

# A2 - select gender, age and region from vaccinated
def selectA2(db):
    name = "selectA2"
    print("- " + name)
    data = db.selectA2()
    to_csv(data, utils.path_extracted_data(name))

# B - select date, region, number of (new cases, cured, deaths) from regions_daily
def selectB(db):
    name = "selectB"
    print("- " + name)
    regions, data = db.selectB()
    to_csv(regions, utils.path_extracted_data(name + "_regions"))
    to_csv(data, utils.path_extracted_data(name))

# C - TODO
def selectC(db):
    None

# D1 (custom1) - select age, vaccine type and number of doses from vaccinated
def selectD1(db):
    name = "selectD1"
    print("- " + name)
    data = db.selectD1()
    to_csv(data, utils.path_extracted_data(name))

# D2 (custom2) - select age, vaccine type and number of doses from vaccinated
def selectD2(db):
    name = "selectD2"
    print("- " + name)
    data1, data2 = db.selectD2()
    to_csv(data1, utils.path_extracted_data(name + "_vaccinated"))
    to_csv(data2, utils.path_extracted_data(name + "_new_cases"))

############################################
#main body
utils.delete_dir_content(utils.extracted_data_dir())

#connect to db --- takhle neni treba volat disconnect... zavola se sam
with db_manager() as db:
    selectA1(db)
    selectA2(db)
    selectB(db)
    selectC(db)
    selectD1(db)
    selectD2(db)

    print("Extraction Done")
