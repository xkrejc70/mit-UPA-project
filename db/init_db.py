import mongodb, os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from load_data import utils

data_dir = utils.data_dir()
static_data_dir = utils.static_data_dir()

# Establish a connection
mongo_client = mongodb.connect()

#print(mongo_client.server_info())
print(f"DBs: ", mongo_client.list_database_names())

db = mongodb.create_db(mongo_client)

# Create collections
coll_new_cases = mongodb.create_collection(db, "new_cases")
coll_vaccinated = mongodb.create_collection(db, "vaccinated")
coll_regions_daily = mongodb.create_collection(db, "regions_daily")
coll_regions = mongodb.create_collection(db, "regions")
coll_cities = mongodb.create_collection(db, "cities")

# Insert to collections
"""
mongodb.insert_into_collection(coll_new_cases, data_dir + "/new_cases")
mongodb.insert_into_collection(coll_vaccinated, data_dir + "/vaccinated")
mongodb.insert_into_collection(coll_regions_daily, data_dir + "/regions_daily")
mongodb.insert_into_collection(coll_regions, static_data_dir + "/cz_regions")
mongodb.insert_into_collection(coll_cities, data_dir + "/cities")
"""

# TODO sjednotit krajr, pohlavi, vek (id instead of text)
# new coll sex

#"""
# Reduced .csv data for testing
mongodb.insert_into_collection(coll_new_cases, "../data_test/new_cases_for_test_only")
mongodb.insert_into_collection(coll_vaccinated, "../data_test/vaccinated_test")
mongodb.insert_into_collection(coll_regions_daily, "../data_test/regions_daily_test")
mongodb.insert_into_collection(coll_regions, static_data_dir + "/cz_regions")
mongodb.insert_into_collection(coll_cities, "../data_test/cities_test")
#"""

mongodb.add_pop(coll_regions, data_dir + "/regions_pop")

#"""
mongodb.print_all(coll_new_cases)
mongodb.print_all(coll_vaccinated)
mongodb.print_all(coll_regions_daily)
mongodb.print_all(coll_regions)
mongodb.print_all(coll_cities)
#"""


# Delete db and disconnect
print(f"DBs: ", mongo_client.list_database_names())
#mongodb.disconnect(mongo_client)