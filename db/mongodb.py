from pymongo import MongoClient
import os, csv

def connect(host = "localhost", port = 27017):
    os.system("sudo systemctl start mongod")
    #os.system("sudo systemctl status mongod")

    return MongoClient(host, port)

def create_db(mongo_client, db_name):
    return mongo_client[db_name]

def create_collection(db, collection):
    return db[collection]

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

def add_pop(collection, regions):
    with open(regions + '.csv', "r") as data_file:
        reader = csv.reader(data_file)
        for region in reader:
            myquery = { "kraj_nazev": region[1] }
            newvalues = { "$set": { "populace": region[0] } }
            collection.update_one(myquery, newvalues)

def print_few(collection):
    print(collection)
    for line in collection.find().limit(10):
        print(line)

def disconnect(mongo_client, db_name):
    mongo_client.drop_database(db_name)
    print(db_name + " - deleted")
    mongo_client.close()
    os.system("sudo systemctl stop mongod")
