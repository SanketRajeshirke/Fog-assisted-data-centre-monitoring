from flask import Flask, jsonify, render_template
import boto3

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

    response = table.scan()

    return jsonify(response["Items"])


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )
