from aws.iot_client import connect_aws_iot, publish_message
import time


client = connect_aws_iot()

payload = {
    "sensor_id": "TEST_01",
    "type": "temperature",
    "value": 25,
    "status": "hello from fog"
}

publish_message(client, payload)

time.sleep(2)

client.disconnect()
