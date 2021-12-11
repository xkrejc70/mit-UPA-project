import utils
from db_manager import db_manager
from os import path

with db_manager(is_drop = True) as db:
    db.insert_csv("cities", path.join(utils.data_dir(), "cities.csv"))
    db.insert_csv("new_cases", path.join(utils.data_dir(), "new_cases.csv"))
    db.insert_csv("vaccinated", path.join(utils.data_dir(), "vaccinated.csv"))
    db.insert_csv("regions_daily", path.join(utils.data_dir(), "regions_daily.csv"))
    db.insert_csv("regions", path.join(utils.static_data_dir(), "cz_regions.csv"))
    db.insert_csv("cities_new_cases", path.join(utils.data_dir(), "cities_new_cases.csv"))
    db.add_population_csv(path.join(utils.data_dir(), "regions_pop.csv"))
