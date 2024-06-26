import base64
import json
import boto3
# import logger
from dynamodb_json import json_util
import os
import daiquiri

QUEUE_URL = os.environ.get("QUEUE_URL")
sqs = boto3.client("sqs")
# logger.basicConfig(level="INFO")
daiquiri.setup(level="INFO")
logger = daiquiri.getLogger(__name__)

# process kinesis stream events
def handler(event, _):
    logger.info({"event": json.dumps(event)})

    if "Records" in event:
        for record in event["Records"]:
            logger.info({"record - 5": json.dumps(record)})
            kinesis_event = json.loads(
                base64.b64decode(record["kinesis"]["data"])
            )
            dynamodb_event = json.loads(
                json.dumps(json_util.loads(kinesis_event))
            )

            logger.info(
                {
                    "dynamodb_event": json.dumps(
                        dynamodb_event, indent=4, sort_keys=True, default=str
                    )
                }
            )
            # get new image
            new_image = dynamodb_event["dynamodb"]["NewImage"]

            if "name" in new_image:
                name = new_image["name"]
                logger.info("Hello " + name)
                send_data_to_sqs(new_image)

                return name  # Echo back the first key value
            else:
                logger.error("name not found in event")
                raise Exception("name not found in event")
    else:
        logger.error("Records not found in event")
        raise Exception("Records not found in event")


def send_data_to_sqs(data):
    response = sqs.send_message(
        QueueUrl=QUEUE_URL, MessageBody=json.dumps(data)
    )

    logger.info({"response": json.dumps(response, indent=4)})
    return response
