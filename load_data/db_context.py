from pymongo import MongoClient

class db_context:
    def __init__(self):
        self.db_name = "upa_covid_db"

    def connect(self, host = "localhost", port = 27017):
        self.client = MongoClient(host, port)
        self.db = self.client[self.db_name]

    def disconnect(self):
        self.client.close()

    def select0(self):
        #dobs_part1
        part1 = self.db["cities"].find()
        #dobs_part2
        part2 = self.db["cities"].find()
        return (part1, part2)

    def selectA1(self):
        #dobs_part2
        part2 = self.db["cities"].find()
        return (part2)