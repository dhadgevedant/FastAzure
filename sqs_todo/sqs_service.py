import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

sqs = boto3.client(
    "sqs",
    aws_access_key_id=os.getenv(
        "AWS_ACCESS_KEY_ID"
    ),
    aws_secret_access_key=os.getenv(
        "AWS_SECRET_ACCESS_KEY"
    ),
    region_name=os.getenv(
        "AWS_REGION"
    )
)

QUEUE_URL = os.getenv(
    "SQS_QUEUE_URL"
)


def send_todo_created_event(todo):
    message = {
        "event": "todo_created",
        "data": todo
    }

    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message)
    )

    return response