from pymongo import MongoClient
from pprint import pprint

def connect_db(url) :
    # client = MongoClient(port=27017)
    client = MongoClient(url)
    db = client['admin']

    return db

class Database() :
    def __init__(self, url, collection) :
        db = connect_db(url)
        collection =  db[collection]
        self.db = collection
    
    def find_user(self, username) :
        return self.db.find_one({"username": username})

    def create_user(self, user) :
        return self.db.insert_one(user)
    
    def delete_user(self, username) : 
        return self.db.delete_one({"username" : username})

    def login_user(self, data) :
        return self.db.find_one({
            "username" : data['username'],
        })