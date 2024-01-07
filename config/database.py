from pymongo import MongoClient

import os
from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:R7pYP4bwqKEo3J7j@cluster0.vrrkifh.mongodb.net/?retryWrites=true&w=majority")

db = client.todo_db

collection_name = db["todo_collection"]
