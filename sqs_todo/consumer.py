import boto3
import os
import json
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

print("Listening for messages...")

while True:
    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20
    )

    messages = response.get(
        "Messages",
        []
    )

    for message in messages:
        body = json.loads(
            message["Body"]
        )

        print("Received:")
        print(body)

        # delete message after processing
        sqs.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=message[
                "ReceiptHandle"
            ]
        )

        print("Message deleted")