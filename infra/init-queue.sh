#!/bin/sh

set -e

export AWS_ENDPOINT_URL=http://localstack:4566
export AWS_DEFAULT_REGION=us-east-1

# Aguarda o LocalStack estar pronto
until awslocal --endpoint-url=$AWS_ENDPOINT_URL sqs list-queues; do
  echo "Aguardando LocalStack..."
  sleep 2
done

# Cria a fila se não existir
awslocal --endpoint-url=$AWS_ENDPOINT_URL sqs create-queue --queue-name enrollment-queue || true
