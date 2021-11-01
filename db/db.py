import mongodb, os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from load_data import utils

class db:
    def __init__(self, db_name = "upa_covid_db"):
        self.data_dir = utils.data_dir()
        self.static_data_dir = utils.static_data_dir()
        self.name = db_name
        self.test_mode = False
        self.mongo_client = None
        self.db = None

    # Establish a connection
    def init_db(self):
        self.mongo_client = mongodb.connect()

        #print(mongo_client.server_info())
        print(f"DBs: ", self.mongo_client.list_database_names())

        self.db = mongodb.create_db(self.mongo_client, self.name)

    def insert_data(self):
        # Create collections
        coll_new_cases = mongodb.create_collection(self.db, "new_cases")
        coll_vaccinated = mongodb.create_collection(self.db, "vaccinated")
        coll_regions_daily = mongodb.create_collection(self.db, "regions_daily")
        coll_regions = mongodb.create_collection(self.db, "regions")
        coll_cities = mongodb.create_collection(self.db, "cities")
        coll_cities_new_cases = mongodb.create_collection(self.db, "cities_new_cases")

        if self.test_mode:
            # TODO Delete
            # Insert loaded data to collections
            mongodb.insert_into_collection(coll_new_cases, "../data_test/new_cases_for_test_only")
            mongodb.insert_into_collection(coll_vaccinated, "../data_test/vaccinated_test")
            mongodb.insert_into_collection(coll_regions_daily, "../data_test/regions_daily_test")
            mongodb.insert_into_collection(coll_regions, self.static_data_dir + "/cz_regions")
            mongodb.insert_into_collection(coll_cities, "../data_test/cities_test")

        else:
            # Reduced .csv data for testing
            mongodb.insert_into_collection(coll_new_cases, self.data_dir + "/new_cases")
            mongodb.insert_into_collection(coll_vaccinated, self.data_dir + "/vaccinated")
            mongodb.insert_into_collection(coll_regions_daily, self.data_dir + "/regions_daily")
            mongodb.insert_into_collection(coll_regions, self.static_data_dir + "/cz_regions")
            mongodb.insert_into_collection(coll_cities, self.data_dir + "/cities")
            mongodb.insert_into_collection(coll_cities_new_cases, self.data_dir + "/cities_new_cases")

        # Add population to each region
        mongodb.add_pop(coll_regions, self.data_dir + "/regions_pop")

        print("In db:")
        mongodb.print_few(coll_new_cases)
        mongodb.print_few(coll_vaccinated)
        mongodb.print_few(coll_regions_daily)
        mongodb.print_few(coll_regions)
        mongodb.print_few(coll_cities)
        mongodb.print_few(coll_cities_new_cases)

        print(f"DBs: ", self.mongo_client.list_database_names())

    # Delete database and disconnect
    def discconnect(self):
        mongodb.disconnect(self.mongo_client, self.name)

# TODO instance in some "main script"
database = db("upa_covid_db")
database.init_db()
database.insert_data()
database.discconnect()