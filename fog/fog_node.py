import json
import paho.mqtt.client as mqtt
from aws.iot_client import connect_aws_iot, publish_message
from datetime import datetime


# -------------------------
# THRESHOLDS
# -------------------------

TEMP_THRESHOLD = 50
POWER_THRESHOLD = 3000


# -------------------------
# LOCAL MQTT CONFIG
# -------------------------

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensors/data"


# -------------------------
# AWS IoT CLIENT
# -------------------------

iot_client = None


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
# SEND TO AWS IoT CORE
# -------------------------

def send_to_iot_core(data):

    print("\nSending to AWS IoT Core:")

    print(json.dumps(data, indent=2))


    publish_message(
        iot_client,
        data
    )


# -------------------------
# MQTT CALLBACK
# -------------------------

def on_message(client, userdata, msg):

    data = json.loads(
        msg.payload.decode()
    )


    print("\nReceived sensor:")
    print(data)


    processed = process_data(data)


    send_to_iot_core(
        processed
    )


# -------------------------
# START FOG NODE
# -------------------------

if __name__ == "__main__":


    # Connect to AWS IoT Core once
    iot_client = connect_aws_iot()


    # Connect local MQTT broker

    client = mqtt.Client()


    client.on_message = on_message


    client.connect(
        MQTT_BROKER,
        MQTT_PORT
    )


    client.subscribe(
        MQTT_TOPIC
    )


    print(
        "Fog node waiting for MQTT data..."
    )


    client.loop_forever()
