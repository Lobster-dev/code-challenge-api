import os
import mongomock
import pymongo

# Set environment variables early so they are present when application modules are imported
os.environ.setdefault("ADMIN_USERNAME", "admin")
os.environ.setdefault("ADMIN_PASSWORD", "admin")
os.environ.setdefault("USER_USERNAME", "user")
os.environ.setdefault("USER_PASSWORD", "user")
os.environ.setdefault("MONGO_URL", "mongodb://localhost:27017")
os.environ.setdefault("AWS_ENDPOINT_URL", "http://localhost:4566")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "test")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "test")
os.environ.setdefault("AWS_REGION", "us-east-1")
os.environ.setdefault("SQS_QUEUE_URL", "http://localhost:4566/000000000000/enrollment-queue")

# Patch pymongo.MongoClient with mongomock before application imports any DB code
pymongo.MongoClient = mongomock.MongoClient

print("[conftest] mongomock patched pymongo.MongoClient; tests will use in-memory MongoDB")

# Now import the application's DB module to get access to collections and seed data
from src.db import mongo as app_mongo


def _seed_db():
	# Clean collections
	try:
		app_mongo.age_groups_collection.delete_many({})
		app_mongo.enrollments_collection.delete_many({})
	except Exception:
		pass

	# Insert a default age group so enrollments can be created in tests
	default_group = {"name": "Adulto", "min_age": 18, "max_age": 99}
	app_mongo.age_groups_collection.insert_one(default_group)


# Seed on import
_seed_db()


# --- Lightweight boto3 SQS mock to avoid LocalStack network calls during tests ---
import boto3


class MockQueue:
	def __init__(self, name=None):
		self.name = name

	def send_message(self, MessageBody=None, **kwargs):
		# Return a simple dict similar to boto3's response
		return {"MessageId": "mocked-message-id", "Body": MessageBody}


class MockSQSResource:
	def __init__(self, *args, **kwargs):
		self.queues = {}

	def get_queue_by_name(self, QueueName=None):
		# return existing or create a new mock queue
		q = self.queues.get(QueueName)
		if not q:
			q = MockQueue(name=QueueName)
			self.queues[QueueName] = q
		return q


# Patch boto3.resource so producer uses the mock instead of contacting LocalStack
boto3.resource = lambda *args, **kwargs: MockSQSResource()
print("[conftest] boto3.resource patched with MockSQSResource; SQS calls are mocked")