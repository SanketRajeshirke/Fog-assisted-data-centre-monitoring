import json
import boto3
from datetime import datetime
from flask import Flask, request, jsonify


app = Flask(__name__)


TEMP_THRESHOLD = 50
POWER_THRESHOLD = 3000

buffer = []


# AWS SQS
sqs = boto3.client(
    "sqs",
    region_name="us-east-1"
)


QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/348256052600/fog-sensor-queue"



# -------------------------
# ANOMALY DETECTION
# -------------------------

def detect_anomaly(data):

    if data["type"] == "temperature" and data["value"] > TEMP_THRESHOLD:
        return True

    if data["type"] == "power" and data["value"] > POWER_THRESHOLD:
        return True

    if data["type"] == "smoke" and data["value"] == "ALERT":
        return True

    if data["type"] == "door" and data["value"] == "OPEN":
        return True

    return False



# -------------------------
# FOG PROCESSING
# -------------------------

def process_data(data):

    enriched = data.copy()


    enriched["processed_by"] = "fog_node"

    enriched["processed_time"] = datetime.utcnow().isoformat()


    anomaly = detect_anomaly(data)

    enriched["anomaly"] = anomaly


    if anomaly:
        enriched["fog_action"] = "alert_generated"
    else:
        enriched["fog_action"] = "normal_forward"


    enriched["fog_status"] = "processed"


    return enriched



# -------------------------
# BATCHING
# -------------------------

def batch_data(data):

    buffer.append(data)


    if len(buffer) >= 5:

        batch = buffer.copy()

        buffer.clear()

        return batch


    return None



# -------------------------
# SEND TO CLOUD
# -------------------------

def send_to_cloud(batch):

    print("\n☁ Sending batch to AWS SQS")


    sqs.send_message(

        QueueUrl=QUEUE_URL,

        MessageBody=json.dumps(batch)

    )


    print("✅ Batch sent successfully")



# -------------------------
# SENSOR API
# -------------------------

@app.route("/sensor", methods=["POST"])
def receive_sensor_data():

    data = request.json


    print("\n📥 Received sensor:")

    print(data)



    processed = process_data(data)



    batch = batch_data(processed)



    if batch:

        send_to_cloud(batch)



    return jsonify({

        "status": "processed",

        "anomaly": processed["anomaly"]

    })



# -------------------------
# START FOG NODE
# -------------------------

if __name__ == "__main__":

    print("Fog node started. Waiting for sensor data...")


    app.run(

        host="0.0.0.0",

        port=5000

    )
