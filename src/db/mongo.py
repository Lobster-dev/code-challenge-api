import os
from pymongo import MongoClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

client = MongoClient(MONGO_URL)
db = client["code_challenge"]

age_groups_collection = db["age_groups"]
enrollments_collection = db["enrollments"]
