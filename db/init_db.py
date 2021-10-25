import mongodb
import csv

# Establish a connection
mongo_client = mongodb.connect()

#print(mongo_client.server_info())
print(f"DBs: ", mongo_client.list_database_names())

db = mongodb.create_db(mongo_client)


# Create collections
coll_new_cases = mongodb.create_collection(db, "new_cases")
coll_vaccinated = mongodb.create_collection(db, "vaccinated")
coll_deaths = mongodb.create_collection(db, "deaths")
coll_cz_regions = mongodb.create_collection(db, "cz_regions")
coll_city = mongodb.create_collection(db, "city")

# Insert to collections
#mongodb.insert_into_collection(coll_new_cases, "data/new_cases")
mongodb.insert_into_collection(coll_new_cases, "data_test/new_cases_for_test_only")
mongodb.insert_into_collection(coll_cz_regions, "data_static/cz_regions")

mongodb.print_all(coll_new_cases)
mongodb.print_all(coll_cz_regions)

# Delete db and disconnect
print(f"DBs: ", mongo_client.list_database_names())
mongodb.disconnect(mongo_client)