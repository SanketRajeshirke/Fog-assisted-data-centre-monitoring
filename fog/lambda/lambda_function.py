import json
import boto3
from decimal import Decimal


# ==========================
# AWS CLIENTS
# ==========================

dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1"
)


sns = boto3.client(
    "sns",
    region_name="us-east-1"
)


table = dynamodb.Table("SensorData")


# SNS Topic ARN

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:348256052600:fire-alert"



# ==========================
# SEND CLOUD ALERT
# ==========================

def send_alert(sensor, severity):

    message = f"""

🚨 DATA CENTRE {severity} ALERT 🚨


Sensor ID:
{sensor['sensor_id']}


Sensor Type:
{sensor['type']}


Detected Value:
{sensor['value']}


Severity:
{severity}


Timestamp:
{sensor['timestamp']}



Recommended Action:

Please inspect the data centre infrastructure immediately.

"""


    sns.publish(

        TopicArn=SNS_TOPIC_ARN,

        Subject=f"Data Centre {severity} Alert",

        Message=message

    )


    print("SNS notification sent")



# ==========================
# BUSINESS RULE ENGINE
# ==========================

def classify_severity(item):


    sensor_type = item["type"]

    value = item["value"]


    severity = "NORMAL"



    # Smoke detection

    if sensor_type == "smoke" and value == "ALERT":

        severity = "CRITICAL"



    # Door security

    elif sensor_type == "door" and value == "OPEN":

        severity = "CRITICAL"



    # Temperature monitoring

    elif sensor_type == "temperature":


        temperature = float(value)


        if temperature > 60:

            severity = "CRITICAL"


        elif temperature > 50:

            severity = "WARNING"



    # Power monitoring

    elif sensor_type == "power":


        power = float(value)


        if power > 3500:

            severity = "WARNING"



    return severity




# ==========================
# LAMBDA ENTRY POINT
# ==========================

def lambda_handler(event, context):


    print("Received event from AWS IoT Core:")

    print(json.dumps(event))



    item = event



    value = item["value"]



    # Convert float for DynamoDB

    if isinstance(value, float):

        value = Decimal(str(value))



    # Business classification

    severity = classify_severity(item)



    enriched = {


        "sensor_id":
            item["sensor_id"],


        "type":
            item["type"],


        "value":
            value,


        "timestamp":
            item["timestamp"],


        "processed_by":
            "lambda",


        "anomaly":
            item.get("anomaly", False),


        "severity":
            severity

    }



    print("Processed data:")

    print(enriched)



    # ==========================
    # STORE IN DYNAMODB
    # ==========================

    table.put_item(

        Item=enriched

    )


    print("Stored in DynamoDB")



    # ==========================
    # CRITICAL ALERT
    # ==========================

    if severity == "CRITICAL":


        send_alert(

            enriched,

            severity

        )



    return {


        "statusCode": 200,


        "body": json.dumps({

            "message":
                "Sensor data processed successfully",


            "processed_records":
                1

        })

    }
