import json
import paho.mqtt.client as mqtt

from datetime import datetime


# -------------------------
# THRESHOLDS
# -------------------------

TEMP_THRESHOLD = 50

POWER_THRESHOLD = 3000



# -------------------------
# MQTT CONFIG
# -------------------------

MQTT_BROKER="localhost"

MQTT_PORT=1883

MQTT_TOPIC="sensors/data"




# -------------------------
# ANOMALY DETECTION
# -------------------------


def detect_anomaly(data):


    if data["type"]=="temperature" and data["value"] > TEMP_THRESHOLD:

        return True



    if data["type"]=="power" and data["value"] > POWER_THRESHOLD:

        return True



    if data["type"]=="smoke" and data["value"]=="ALERT":

        return True



    if data["type"]=="door" and data["value"]=="OPEN":

        return True



    return False




# -------------------------
# FOG PROCESSING
# -------------------------


def process_data(data):


    enriched=data.copy()



    enriched["processed_by"]="fog_node"


    enriched["processed_time"]=datetime.utcnow().isoformat()



    anomaly=detect_anomaly(data)



    enriched["anomaly"]=anomaly



    if anomaly:


        enriched["fog_action"]="alert_generated"


    else:

        enriched["fog_action"]="normal_forward"



    enriched["fog_status"]="processed"



    return enriched




# -------------------------
# AWS IoT CORE PLACEHOLDER
# -------------------------


def send_to_iot_core(data):


    print(
        "Sending to AWS IoT Core:"
    )

    print(data)


    # later replace this
    # with AWS IoT MQTT publish



# -------------------------
# MQTT CALLBACK
# -------------------------


def on_message(client,userdata,msg):


    data=json.loads(
        msg.payload.decode()
    )


    print(
        "\nReceived sensor:"
    )

    print(data)



    processed=process_data(data)



    send_to_iot_core(
        processed
    )





# -------------------------
# START FOG NODE
# -------------------------


client=mqtt.Client()


client.on_message=on_message



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
