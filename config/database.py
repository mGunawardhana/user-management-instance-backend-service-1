from pymongo import MongoClient

import os
from pymongo import MongoClient

MONGODB_URL = os.getenv('MONGODB_CLUSTER_URL')

client = MongoClient(MONGODB_URL)

db = client.todo_db

collection_name = db["todo_collection"]