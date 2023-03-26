import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

class Database:
    connection_string = ""
    db = None
    users = None
    


def get_user_collection():
    try:
        client = MongoClient(MONGODB_URI)
    except:
        raise Exception(f"Couldn't connect to mongoDB in the following address: {MONGODB_URI}")
    flask_db = client["flask"]
    return flask_db["user"]

user_result = user_collection.insert_one({"name":"John Doe","password":"secret"})
user_id = user_result.inserted_id