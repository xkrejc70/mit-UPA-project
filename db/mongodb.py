from pymongo import MongoClient
import os, csv, json
import pandas as pd

db_name = "upa_covid_db"

def connect(host = "localhost", port = 27017):
    os.system("sudo systemctl start mongod")
    #os.system("sudo systemctl status mongod")

    return MongoClient(host, port)

def create_db(mongo_client):
    return mongo_client[db_name]

def create_collection(db, collection):
    return db[collection]

def insert_into_collection(collection, csv_file):
    print(f"Inserting from", csv_file)
    
    data = pd.read_csv(csv_file + ".csv")
    payload = json.loads(data.to_json(orient='records'))
    collection.remove()
    collection.insert(payload)

"""
    with open(csv_file + '.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        mongo_docs = []

        for row in reader:
            doc = {}
            for n in range(0,len(header)):
                doc[header[n]] = row[n]

            mongo_docs += [doc]

    collection.insert_many(mongo_docs)
"""


def add_pop(collection, regions):
    with open(regions + '.csv', "r") as data_file:
        reader = csv.reader(data_file)
        for region in reader:
            myquery = { "kraj_nazev": region[1] }
            newvalues = { "$set": { "populace": region[0] } }
            collection.update_one(myquery, newvalues)

def print_all(collection):
    print(collection)
    for line in collection.find():
        print(line)

def disconnect(mongo_client):
    mongo_client.drop_database(db_name)
    mongo_client.close()
    os.system("sudo systemctl stop mongod")
