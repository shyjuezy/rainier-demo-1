import json
import logging


print("Loading function")
# table_name = os.environ.get("TABLE_NAME")
# dynamodb_client = boto3.resource("dynamodb")
# table = dynamodb_client.Table(table_name)


def handler(event, _):
    logging.info({"event": json.dumps(event)})
