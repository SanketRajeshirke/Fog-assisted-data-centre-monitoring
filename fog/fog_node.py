import json
import time
import random
from datetime import datetime

TEMP_THRESHOLD = 50
POWER_THRESHOLD = 3000

buffer = []

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


def process_data(data):
    enriched = data.copy()

    enriched["processed_by"] = "fog_node"
    enriched["processed_time"] = datetime.utcnow().isoformat()

    # mark anomaly
    enriched["anomaly"] = detect_anomaly(data)

    return enriched


def batch_data(data):
    buffer.append(data)

    # send batch of 5
    if len(buffer) >= 5:
        batch = buffer.copy()
        buffer.clear()
        return batch

    return None


import boto3
import json

sqs = boto3.client("sqs", region_name="us-east-1")

QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/348256052600/fog-sensor-queue"
def send_to_cloud(batch):
    print("\n☁️ Sending batch to AWS SQS")

    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(batch)
    )

    print("✅ Sent to SQS successfully")

# -------------------------
# SIMULATED INPUT STREAM
# -------------------------
def simulate_sensor_input():
    sensors = ["temperature", "humidity", "power", "smoke", "door"]

    while True:
        sensor_type = random.choice(sensors)

        if sensor_type == "temperature":
            value = round(random.uniform(20, 60), 2)
        elif sensor_type == "humidity":
            value = round(random.uniform(30, 70), 2)
        elif sensor_type == "power":
            value = round(random.uniform(1000, 4000), 2)
        elif sensor_type == "smoke":
            value = random.choice(["NORMAL", "ALERT"])
        else:
            value = random.choice(["OPEN", "CLOSED"])

        data = {
            "sensor_id": f"{sensor_type.upper()}_01",
            "type": sensor_type,
            "value": value,
            "timestamp": datetime.utcnow().isoformat()
        }

        print("\n📥 Incoming:", data)

        processed = process_data(data)

        batch = batch_data(processed)

        if batch:
            send_to_cloud(batch)

        time.sleep(1)


if __name__ == "__main__":
    simulate_sensor_input()
