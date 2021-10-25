from pymongo import MongoClient
import os
import csv

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
    with open('../'+ csv_file +'.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        print(f"Inserting", csv_file)
        for row in reader:
            doc = {}
            for n in range(0,len(header)):
                doc[header[n]] = row[n]

            collection.insert_one(doc)

def print_all(collection):
    print(collection)
    for line in collection.find():
        print(line)

def disconnect(mongo_client):
    mongo_client.drop_database(db_name)
    mongo_client.close()
    os.system("sudo systemctl stop mongod")
