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

    def insert_chunk(self, chunk, header, collection_name):
        mongo_docs = []
        for row in chunk:
            doc = {}
            for n in range(0, len(header)):
                doc[header[n]] = row[n]
            mongo_docs += [doc]

        self.db[collection_name].insert_many(mongo_docs)

    def insert_csv(self, collection_name, csv_file):
        print(f"Insert csv start: {collection_name}")
        with open(csv_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            chunk = []
            chunksize = 2048*1000

            for i, line in enumerate(reader):
                if (i % chunksize == 0 and i > 0):
                    self.insert_chunk(chunk, header, collection_name)
                    del chunk[:]
                chunk.append(line)
            self.insert_chunk(chunk, header, collection_name)
        print(f"Insert csv end: {collection_name}")

    def add_population_csv(self, csv_file):
        print(f"Insert population csv start")
        with open(csv_file, "r") as data_file:
            reader = csv.reader(data_file)
            for region in reader:
                myquery = { "kraj_nazev": region[1] }
                newvalues = { "$set": { "populace": region[0] } }
                self.db["regions"].update_one(myquery, newvalues)
        print(f"Insert population csv end")

    def disconnect(self):
        self.client.close()

    def select0(self):
        #dobs_part1
        part1 = self.db["cities"].find()
        #dobs_part2
        part2 = self.db["cities"].find()
        return (part1, part2)