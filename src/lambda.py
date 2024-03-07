import json
import boto3
import logging

from datetime import datetime
import os

print("Loading function")
table_name = os.environ.get("TABLE_NAME")
dynamodb_client = boto3.resource("dynamodb")
table = dynamodb_client.Table(table_name)


def handler(event, context):
    logging.info({"event": json.dumps(event)})

    if "name" in event:
        name = event["name"]
        logging.info("Hello " + name)
        add_data_to_dynamodb(event)

        return name  # Echo back the first key value
    else:
        logging.error("name not found in event")
        raise Exception("name not found in event")


def add_data_to_dynamodb(event):
    event["timestamp"] = str(datetime.now())
    response = table.put_item(Item=event)
    logging.info("PutItem succeeded:")
    logging.info({"response": json.dumps(response, indent=4)})
    return response
