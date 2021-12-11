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