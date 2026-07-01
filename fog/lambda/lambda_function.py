import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("SensorData")

def lambda_handler(event, context):

    print("Received event:", event)

    processed = []

    for record in event['Records']:
        body = json.loads(record['body'])

        # each batch from fog node
        for item in body:

            enriched = {
                "sensor_id": item["sensor_id"],
                "type": item["type"],
                "value": item["value"],
                "timestamp": item["timestamp"],
                "processed_by": "lambda",
                "anomaly": item.get("anomaly", False)
            }

            processed.append(enriched)

            print("Processed:", enriched)

            # ✅ STORE IN DYNAMODB
            table.put_item(Item=enriched)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Data processed successfully",
            "count": len(processed)
        })
    }
