import os
import time
import json
import logging
from dotenv import load_dotenv
import boto3
from pymongo import MongoClient
from botocore.exceptions import ClientError

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("worker")

QUEUE_NAME = os.getenv("QUEUE_NAME", "enrollment-queue")
SQS_ENDPOINT = os.getenv("SQS_ENDPOINT")
REGION_NAME = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

MONGO_URL = os.getenv("MONGO_URL")
mongo_client = MongoClient(MONGO_URL)
db = mongo_client["code_challenge"]
enrollments_collection = db["enrollments"]

sqs = boto3.resource(
    "sqs",
    endpoint_url=SQS_ENDPOINT,
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

max_retries = 20
for attempt in range(max_retries):
    try:
        queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
        logger.info(f"Fila encontrada: {QUEUE_NAME}")
        break
    except ClientError as e:
        logger.warning(f"Fila {QUEUE_NAME} não encontrada, tentativa {attempt+1}/{max_retries}. Aguardando...")
        time.sleep(2)
else:
    logger.error(f"Não foi possível encontrar a fila {QUEUE_NAME} após {max_retries} tentativas. Encerrando worker.")
    exit(1)

logger.info(f"[Standalone Worker] Consumindo mensagens da fila: {QUEUE_NAME}")
while True:
    messages = queue.receive_messages(MaxNumberOfMessages=1, WaitTimeSeconds=10)
    if not messages:
        logger.info("Nenhuma mensagem nova.")
        continue
    for message in messages:
        try:
            logger.info(f"Mensagem recebida: {message.body}")
            data = json.loads(message.body)
            time.sleep(2)  # Simula processamento mínimo
            result = enrollments_collection.insert_one({
                **data,
                "status": "processed",
                "processed_at": time.time(),
            })
            logger.info(f"Inscrição processada e salva com _id: {result.inserted_id}")
            message.delete()
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
