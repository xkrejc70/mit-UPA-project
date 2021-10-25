from pymongo import MongoClient
import os

db_name = "upa_covid_db"

def connect(host = "localhost", port = 27017):
    os.system("sudo systemctl start mongod")
    #os.system("sudo systemctl status mongod")

    return MongoClient(host, port)

def create_db(mongo_client):
    return mongo_client[db_name]

def create_collection(db, collection):
    return db[collection]

def insert_into_collection():
    pass

def disconnect(mongo_client):
    mongo_client.drop_database(db_name)
    mongo_client.close()
    os.system("sudo systemctl stop mongod")
