import os
from pymongo import MongoClient

IS_TESTING = "PYTEST_CURRENT_TEST" in os.environ
MONGO_HOST = "localhost" if IS_TESTING else os.getenv("MONGO_HOST", "mongo")
MONGO_URL = f"mongodb://{MONGO_HOST}:27017/"

client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
try:
    client.admin.command('ismaster')
except Exception:
    print("Falha ao conectar ao MongoDB. Verifique se o serviço está rodando.")

db = client["code_challenge"]

age_groups_collection = db["age_groups"]
enrollments_collection = db["enrollments"]
