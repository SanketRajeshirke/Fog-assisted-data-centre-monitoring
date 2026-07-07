import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table("SensorData")


def lambda_handler(event, context):

    print("Received event:", event)

    processed = []

    for record in event["Records"]:

        body = json.loads(record["body"])

        # batch received from SQS
        for item in body:

            value = item["value"]

            # DynamoDB does not support float
            if isinstance(value, float):
                value = Decimal(str(value))


            enriched = {

                "sensor_id": item["sensor_id"],

                "type": item["type"],

                "value": value,

                "timestamp": item["timestamp"],

                "processed_by": "lambda",

                "anomaly": item.get("anomaly", False)

            }


            processed.append(enriched)

            print("Processed:", enriched)


            # Store in DynamoDB
            table.put_item(
                Item=enriched
            )


    return {

        "statusCode": 200,

        "body": json.dumps({

            "message": "Data processed successfully",

            "count": len(processed)

        })

    }
