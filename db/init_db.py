import mongodb

# Establish a connection
mongo_client = mongodb.connect()

#print(mongo_client.server_info())
print(mongo_client.list_database_names())

db = mongodb.create_db(mongo_client)



############x TEST DB

db_test = mongodb.create_collection(db, "test")

result = db_test.insert_one({
        "datum": "2021-01-20",
        "vek": 84,
        "pohlavi": "Z",
        "kraj_nuts_kod": "CZ042",
        "okres_lau_kod": "CZ0425"
    })
print(result)

test_data = [
    {
        "datum": "2021-01-20",
        "vek": 84,
        "pohlavi": "Z",
        "kraj_nuts_kod": "CZ042",
        "okres_lau_kod": "CZ0425"
    },
    {
        "datum": "2020-12-12",
        "vek": 65,
        "pohlavi": "Z",
        "kraj_nuts_kod": "CZ080",
        "okres_lau_kod": "CZ0806"
    },
    {
        "datum": "2020-10-27",
        "vek": 38,
        "pohlavi": "Z",
        "kraj_nuts_kod": "CZ064",
        "okres_lau_kod": "CZ0642"
    },
    {
        "datum": "2021-01-09",
        "vek": 27,
        "pohlavi": "M",
        "kraj_nuts_kod": "CZ020",
        "okres_lau_kod": "CZ020C"
    }
]

result = db_test.insert_many(test_data)
print(result)

for x in db_test.find():
    print(x)

#collist = db.list_collection_names()
#if "test" in collist:
#    print("upa_covid_db in collist")



# Delete db and disconnect
print(mongo_client.list_database_names())
mongodb.disconnect(mongo_client)