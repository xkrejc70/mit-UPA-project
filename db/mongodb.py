# mongodb.py
# Proj: UPA 2021
# Authors: Honza Krejčí (xkrejc70), Matěj Sojka (xsojka04), Matěj Kudera (xkuder04)
# Function for manipulation with MongoDB

from pymongo import MongoClient
import os, csv

# Connect to local Mongo database server
def connect(host = "localhost", port = 27017):
    #os.system("sudo systemctl start mongod")
    #os.system("sudo systemctl status mongod")
    return MongoClient(host, port)

# Create new database
def create_db(mongo_client, db_name):
    # Drop db if exists
    if db_name in mongo_client.list_database_names():
        mongo_client.drop_database(db_name)
    print("Creating database " + db_name)
    return mongo_client[db_name]

# Drop database if exists
def delete_db(mongo_client, db_name):
    mongo_client.drop_database(db_name)

# Create new collection in database
def create_collection(db, collection):
    return db[collection]

# Insert data to databese in chuncks
def insert_chunk(chuck, header, collection):
    mongo_docs = []
    for row in chuck:
        doc = {}
        for n in range(0, len(header)):
            doc[header[n]] = row[n]
        mongo_docs += [doc]

    collection.insert_many(mongo_docs)

# Insert csv data from file into database collection
def insert_into_collection(collection, csv_file):
    csv_file += '.csv'
    print(f"Inserting from", csv_file)

    if not os.path.isfile(csv_file):
        print(f"No such file")
        print(f"Try: make load")
        quit()

    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        chunk = []
        chunksize = 2048*1000

        for i, line in enumerate(reader):
            if (i % chunksize == 0 and i > 0):
                insert_chunk(chunk, header, collection)
                del chunk[:]
            chunk.append(line)
        insert_chunk(chunk, header, collection)

# Add population into cities collection
def add_pop(collection, regions):
    with open(regions + '.csv', "r") as data_file:
        reader = csv.reader(data_file)
        for region in reader:
            myquery = { "kraj_nazev": region[1] }
            newvalues = { "$set": { "populace": region[0] } }
            collection.update_one(myquery, newvalues)

# Print 10 first objects of collection
def print_few(collection):
    print(collection)
    for line in collection.find().limit(10):
        print(line)

# Terminate colection with local MongoDB server
def disconnect(mongo_client, db_name):
    #mongo_client.drop_database(db_name)
    #print(db_name + " - deleted")
    mongo_client.close()
    #os.system("sudo systemctl stop mongod")

# END mongodb.py