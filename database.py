from pymongo import MongoClient
from pprint import pprint

def connect_db(url) :
    # client = MongoClient(port=27017)
    client = MongoClient(url)
    db = client['admin']

    return db