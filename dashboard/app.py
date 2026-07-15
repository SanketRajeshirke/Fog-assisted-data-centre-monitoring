from flask import Flask, jsonify, render_template
import boto3
from collections import Counter


app = Flask(__name__)


# DynamoDB

dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1"
)

table = dynamodb.Table(
    "SensorData"
)





@app.route("/")
def home():

    return render_template(
        "index.html"
    )







def get_all_data():

    response = table.scan()

    items = response.get(
        "Items",
        []
    )

    return items







# 1. Latest sensor monitoring API

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
        items[:100]
    )








# 2. Business alert API

@app.route("/api/alerts")
def alerts():


    items = get_all_data()


    alert_data=[]



    for item in items:


        if item.get(
            "anomaly",
            False
        ) in [True,"true"]:


            severity="WARNING"



            if item.get(
                "type"
            ) in [
                "smoke",
                "door"
            ]:

                severity="CRITICAL"



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
        alert_data[:50]
    )









# 3. Dashboard KPI summary API

@app.route("/api/summary")
def summary():


    items=get_all_data()



    total=len(items)



    alerts=sum(

        1 for x in items

        if x.get("anomaly")
        in [True,"true"]

    )



    critical=sum(

        1 for x in items

        if x.get("anomaly")
        in [True,"true"]

        and x.get("type")
        in [
            "smoke",
            "door"
        ]

    )



    power=[]


    for x in items:

        if x.get("type")=="power":

            try:

                power.append(
                    float(
                        x.get("value")
                    )
                )

            except:

                pass




    current_power = (
        power[0]
        if power
        else 0
    )



    return jsonify({

        "total_records":total,

        "active_alerts":alerts,

        "critical_alerts":critical,

        "current_power":current_power

    })









# 4. Sensor health API

@app.route("/api/status")
def status():


    items=get_all_data()


    sensors={}



    for item in items:


        sid=item.get(
            "sensor_id"
        )


        sensors[sid]={

            "sensor_id":sid,

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









# 5. Analytics API

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


            if item.get(
                "type"
            )==sensor_type:


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




    return jsonify(
        result
    )









if __name__=="__main__":


    app.run(

        host="0.0.0.0",

        port=8000,

        debug=False

    )

