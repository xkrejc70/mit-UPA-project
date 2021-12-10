import utils

#TODO converts data to csv and stores them
def to_csv(data, path):
    pass

def select1(db):
    data = db.select1()
    to_csv(data, path):

#main body
utils.delete_dir_content(utils.extracted_data_dir())

#connect to db
db = 0

select1(db)
#select2(db)
#select3(db)
#...

#end db
db.disconnect()