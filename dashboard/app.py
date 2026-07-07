from flask import Flask, jsonify, render_template
import boto3
from boto3.dynamodb.conditions import Key

app = Flask(__name__)


# DynamoDB connection
dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1"
)

table = dynamodb.Table("SensorData")



@app.route("/")
def home():
    return render_template("index.html")



@app.route("/api/sensors")
def get_sensors():

    try:

        response = table.scan()

        sensors = response.get("Items", [])


        # Sort newest first
        sensors.sort(
            key=lambda x: x.get("timestamp", ""),
            reverse=True
        )


        # Take latest 100 records
        latest = sensors[:100]


        return jsonify(latest)


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )
