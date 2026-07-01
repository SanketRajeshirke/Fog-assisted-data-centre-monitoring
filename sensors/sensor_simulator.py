import time
import random
import json
import yaml
from datetime import datetime

# Load config
with open("config/sensors_config.yaml", "r") as f:
    config = yaml.safe_load(f)

state = {
    "temperature": 25.0,
    "humidity": 50.0,
    "power": 1500
}

def gen_temperature():
    state["temperature"] += random.uniform(-0.5, 0.7)

    if random.random() < config["temperature"]["anomaly_rate"]:
        state["temperature"] += random.uniform(5, 8)

    return round(state["temperature"], 2)

def gen_humidity():
    state["humidity"] += random.uniform(-1, 1)
    state["humidity"] = max(30, min(80, state["humidity"]))
    return round(state["humidity"], 2)

def gen_power():
    state["power"] += random.uniform(-50, 50)

    if random.random() < config["power"]["anomaly_rate"]:
        state["power"] += random.uniform(500, 1000)

    return round(state["power"], 2)

def gen_smoke():
    return "ALERT" if random.random() < config["smoke"]["anomaly_rate"] else "NORMAL"

def gen_door():
    return random.choice(["OPEN", "CLOSED"])

def payload(sensor_type, value):
    return {
        "sensor_id": f"{sensor_type.upper()}_01",
        "type": sensor_type,
        "value": value,
        "timestamp": datetime.utcnow().isoformat()
    }

def run():
    print("Sensor simulation started...\n")

    while True:
        data = [
            payload("temperature", gen_temperature()),
            payload("humidity", gen_humidity()),
            payload("power", gen_power()),
            payload("smoke", gen_smoke()),
            payload("door", gen_door())
        ]

        for d in data:
            print(json.dumps(d))

        time.sleep(2)

if __name__ == "__main__":
    run()
