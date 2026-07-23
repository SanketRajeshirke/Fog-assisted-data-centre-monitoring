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



# Get complete DynamoDB data with pagination

def get_all_data():

    items = []

    response = table.scan()

    items.extend(
        response.get("Items", [])
    )


    while "LastEvaluatedKey" in response:

        response = table.scan(
            ExclusiveStartKey=
            response["LastEvaluatedKey"]
        )

        items.extend(
            response.get("Items", [])
        )


    return items




# Latest sensor monitoring API

@app.route("/api/sensors")
def sensors():

    items = get_all_data()


    items.sort(
        key=lambda x:x.get(
            "timestamp",
            ""
        ),
        reverse=True
    )


    return jsonify(
        items[:500]
    )




# Business alert API

@app.route("/api/alerts")
def alerts():


    items = get_all_data()


    alert_data=[]


    for item in items:


        if item.get("anomaly") in [
            True,
            "true"
        ]:


            severity = item.get(
                "severity",
                "WARNING"
            )


            alert_data.append({

                "sensor_id":
                    item.get("sensor_id"),

                "type":
                    item.get("type"),

                "value":
                    item.get("value"),

                "severity":
                    severity,

                "timestamp":
                    item.get("timestamp")

            })



    alert_data.sort(
        key=lambda x:x["timestamp"],
        reverse=True
    )


    return jsonify(
        alert_data[:100]
    )





# Dashboard KPI summary

@app.route("/api/summary")
def summary():


    items = get_all_data()



    total = len(items)



    active_alerts = sum(

        1 for x in items

        if x.get("anomaly")
        in [
            True,
            "true"
        ]

    )



    critical_alerts = sum(

        1 for x in items

        if x.get("severity")
        ==
        "CRITICAL"

    )



    power_values=[]



    for x in items:


        if x.get("type")=="power":

            try:

                power_values.append(
                    float(
                        x.get("value")
                    )
                )

            except:

                pass



    current_power = (

        power_values[-1]

        if power_values

        else 0

    )



    return jsonify({

        "total_records":
            total,


        "active_alerts":
            active_alerts,


        "critical_alerts":
            critical_alerts,


        "current_power":
            current_power

    })





# Sensor status API

@app.route("/api/status")
def status():


    items=get_all_data()


    sensors={}



    for item in items:


        sid=item.get(
            "sensor_id"
        )


        sensors[sid]={

            "sensor_id":
                sid,


            "type":
                item.get("type"),


            "last_seen":
                item.get("timestamp"),


            "status":
                "ONLINE"

        }



    return jsonify(
        list(
            sensors.values()
        )
    )






# Analytics API for charts

@app.route("/api/analytics")
def analytics():


    items=get_all_data()


    result={}



    for sensor_type in [

        "power",
        "temperature",
        "humidity"

    ]:


        values=[]



        for item in items:


            if item.get("type")==sensor_type:


                try:

                    values.append(
                        float(
                            item.get("value")
                        )
                    )


                except:

                    pass




        if values:


            result[sensor_type]={


                "average":
                    round(
                        sum(values)
                        /
                        len(values),
                        2
                    ),


                "maximum":
                    max(values),


                "minimum":
                    min(values)

            }




    return jsonify(result)






if __name__=="__main__":


    app.run(

        host="0.0.0.0",

        port=8000,

        debug=False

    )
