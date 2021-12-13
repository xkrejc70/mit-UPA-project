from pymongo import MongoClient
import csv

class db_context:
    def __init__(self, is_drop = False):
        self.db_name = "upa_covid_db"
        self.is_drop = is_drop

    def connect(self, host = "localhost", port = 27017):
        self.client = MongoClient(host, port)
        if self.is_drop:
            self.drop()
        self.db = self.client[self.db_name]

    def drop(self):
        self.client.drop_database(self.db_name)

    def insert_chunk(self, chunk, header, collection):
        mongo_docs = []
        for row in chunk:
            doc = {}
            for n in range(0, len(header)):
                doc[header[n]] = row[n]
            mongo_docs += [doc]

        collection.insert_many(mongo_docs)

    def insert_csv(self, collection_name, csv_file):
        print(f"Insert csv start: {collection_name}")
        collection = self.db[collection_name]
        with open(csv_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            chunk = []
            chunksize = 2048*1000

            for i, line in enumerate(reader):
                if (i % chunksize == 0 and i > 0):
                    self.insert_chunk(chunk, header, collection)
                    del chunk[:]
                chunk.append(line)
            self.insert_chunk(chunk, header, collection)
        print(f"Insert csv end: {collection_name}")

    def add_population_csv(self, csv_file):
        print(f"Insert population csv start")
        with open(csv_file, "r") as data_file:
            reader = csv.reader(data_file)
            collection = self.db["regions"]
            for region in reader:
                myquery = { "kraj_nazev": region[1] }
                newvalues = { "$set": { "populace": region[0] } }
                collection.update_one(myquery, newvalues)
        print(f"Insert population csv end")

    def disconnect(self):
        self.client.close()

# A1 - select age and region from new_cases
    def selectA1(self):
        data = self.db["new_cases"].aggregate([
            {
                "$lookup": {
                    "from": "regions",
                    "localField": "kraj_nuts_kod",
                    "foreignField": "kraj_nuts_kod",
                    "as": "kraj"
                }
            },
            {
                "$unwind": "$kraj"
            },
            {
                "$project": {
                    "_id": 0,
                    "vek": 1,
                    "kraj": "$kraj.kraj_nazev"
                }
            }
        ])
        return (list(data))

# A2 - select gender, age and region from vaccinated
    def selectA2(self):
        data = self.db["vaccinated"].find({},
            {
                "_id": 0,
                "pohlavi": 1,
                "vekova_skupina": 1,
                "kraj_nuts_kod": 1
            }
        )
        return (data)

# B - select date, region, number of (new cases, cured, deaths) from regions_daily
    def selectB(self):
        regions = self.db["regions"].find({},
            {
                "_id": 0,
                "kraj_nuts_kod": 1,
                "kraj_nazev": 1,
                "populace": 1
            }
        )

        data = self.db["regions_daily"].aggregate([
            {
                "$lookup": {
                    "from": "regions",
                    "localField": "kraj_nuts_kod",
                    "foreignField": "kraj_nuts_kod",
                    "as": "kraj"
                }
            },
            {
                "$unwind": "$kraj"
            },
            {
                "$project": {
                    "_id": 0,
                    "datum": 1,
                    "kraj": "$kraj.kraj_nazev",
                    "kumulativni_pocet_nakazenych": 1,
                    "kumulativni_pocet_vylecenych": 1,
                    "kumulativni_pocet_umrti": 1
                }
            },

        ])
        return (regions, list(data))

# C - select new cases, vaccinated and population 50 cities
    def selectC(self):
        new_cases = self.db["cities_new_cases"].find({},
            {
                "_id": 0,
                "datum": 1,
                "mesto": "$orp_nazev",
                "nove_pripady": 1
            }
        )

        vaccinated = self.db["vaccinated"].aggregate([
            {
                "$match": {
                    "poradi_davky": "1",
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "datum": "$datum",
                    "mesto": "$orp_bydliste"
                }
            }
        ])

        population = self.db["cities"].aggregate([
            {
                "$match": {
                    "pohlavi_kod": "",
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "populace": "$hodnota",
                    "vek_txt": 1,
                    "mesto": "$vuzemi_txt"
                }
            }
        ])

        return (new_cases, list(vaccinated), list(population))

# D1 (custom1) - select age, vaccine type and number of doses from vaccinated
    def selectD1(self):
        data = self.db["vaccinated"].aggregate([
            {
                "$match": {
                    "poradi_davky": "1",
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "vakcina": "$vakcina",
                    "vekova_skupina": "$vekova_skupina"
                }
            }
        ])
        return (list(data))

# D2 (custom2) - select age, vaccine type and number of doses from vaccinated
    def selectD2(self):
        data1 = self.db["vaccinated"].aggregate([
            {
                "$match": {
                    "orp_bydliste": "Brno",
                    "poradi_davky": "1",
                }
            },
            {
                "$group": {
                    "_id": "$datum",
                    "count": {"$sum": 1}
                }
            }
        ])

        data2 = self.db["cities_new_cases"].aggregate([
            {
                "$match": {
                    "orp_nazev": "Brno",
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "datum": "$datum",
                    "count": {"$sum": {"$toInt": "$nove_pripady"}}
                }
            }
        ])
        return (list(data1), list(data2))

"""
            {
                "$limit": 10
            }
"""