import os
import json
import time
import boto3
from botocore.exceptions import ClientError

QUEUE_NAME = "enrollment-queue"
SQS_ENDPOINT = os.getenv("SQS_ENDPOINT", "http://localstack:4566")
REGION_NAME = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")

sqs = boto3.resource(
    "sqs",
    endpoint_url=SQS_ENDPOINT,
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

def get_queue_with_retry(max_retries=20, wait=2):
    for attempt in range(max_retries):
        try:
            queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
            return queue
        except ClientError:
            time.sleep(wait)
    raise RuntimeError(f"Não foi possível encontrar a fila {QUEUE_NAME} após {max_retries} tentativas.")

def send_enrollment_to_queue(enrollment_data: dict):
    queue = get_queue_with_retry()
    response = queue.send_message(MessageBody=json.dumps(enrollment_data))
    return response
