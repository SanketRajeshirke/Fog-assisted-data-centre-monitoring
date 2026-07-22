AWS_IOT_ENDPOINT = "a1unlpi6b9f0rh-ats.iot.us-east-1.amazonaws.com"
import ssl
import json
import time
import paho.mqtt.client as mqtt


AWS_IOT_ENDPOINT = "a1unlpi6b9f0rh-ats.iot.us-east-1.amazonaws.com"
PORT = 8883

# Certificates
CA_PATH = "aws/certificates/AmazonRootCA1.pem"
CERT_PATH = "aws/certificates/certificate.pem.crt"
KEY_PATH = "aws/certificates/private.pem.key"

# MQTT topic
TOPIC = "fog/data"


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to AWS IoT Core")
    else:
        print(f"Connection failed with code: {reason_code}")


def on_publish(client, userdata, mid, reason_code, properties):
    print("Message delivered to AWS IoT Core")


def connect_aws_iot():

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="FogNode01"
    )

    # Callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish

    # TLS configuration
    client.tls_set(
        ca_certs=CA_PATH,
        certfile=CERT_PATH,
        keyfile=KEY_PATH,
        tls_version=ssl.PROTOCOL_TLSv1_2
    )

    try:
        print("Connecting to AWS IoT Core...")

        client.connect(
            AWS_IOT_ENDPOINT,
            PORT
        )

        # Start MQTT network handling
        client.loop_start()

        # Give time for connection
        time.sleep(2)

        return client

    except Exception as e:
        print("Connection error:", e)
        raise


def publish_message(client, payload):

    try:

        message = json.dumps(payload)

        result = client.publish(
            TOPIC,
            message,
            qos=1
        )

        # Wait until AWS acknowledges
        result.wait_for_publish()

        print("Message published")

    except Exception as e:
        print("Publish error:", e)
        raise


if __name__ == "__main__":

    client = connect_aws_iot()

    test_message = {
        "sensor_id": "TEST_01",
        "type": "temperature",
        "value": 25,
        "status": "hello from fog"
    }

    publish_message(client, test_message)

    time.sleep(3)

    client.loop_stop()
    client.disconnect()

    print("Disconnected from AWS IoT Core")
