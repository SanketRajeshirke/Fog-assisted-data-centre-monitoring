let powerChart;
let temperatureChart;
let humidityChart;


function loadSensors() {

    console.log("Loading sensor data...");

    fetch("/api/sensors")

        .then(response => response.json())

        .then(data => {

            console.log("Received data:", data);


            let sensorTable = document.getElementById("sensorTable");
            let alertTable = document.getElementById("alertTable");


            sensorTable.innerHTML = "";
            alertTable.innerHTML = "";


            let alerts = 0;


            document.getElementById("totalSensors").innerHTML = data.length;



            data.forEach(sensor => {


                console.log("Processing:", sensor);


                // Sensor table

                let row = `
                    <tr>
                        <td>${sensor.sensor_id}</td>
                        <td>${sensor.type}</td>
                        <td>${sensor.value}</td>
                        <td>
                            ${sensor.anomaly ? "🚨 TRUE" : "NORMAL"}
                        </td>
                        <td>${sensor.processed_by}</td>
                    </tr>
                `;


                sensorTable.innerHTML += row;



                // Alert table

                if(sensor.anomaly === true || sensor.anomaly === "true") {


                    alerts++;


                    let alertRow = `
                        <tr>
                            <td>${sensor.sensor_id}</td>
                            <td>${sensor.type}</td>
                            <td>${sensor.value}</td>
                            <td>🚨 ALERT</td>
                        </tr>
                    `;


                    alertTable.innerHTML += alertRow;

                }


            });



            document.getElementById("totalAlerts").innerHTML = alerts;



            createCharts(data);


        })


        .catch(error => {

            console.error(
                "Error loading sensor data:",
                error
            );

        });


}






function createCharts(data){


    let powerLabels = [];
    let powerValues = [];

    let tempLabels = [];
    let tempValues = [];

    let humidityLabels = [];
    let humidityValues = [];



    data.forEach(sensor => {



        let value = Number(sensor.value);



        if(sensor.type === "power"){

            powerLabels.push(sensor.timestamp);
            powerValues.push(value);

        }



        if(sensor.type === "temperature"){

            tempLabels.push(sensor.timestamp);
            tempValues.push(value);

        }



        if(sensor.type === "humidity"){

            humidityLabels.push(sensor.timestamp);
            humidityValues.push(value);

        }


    });





    // Destroy old charts


    if(powerChart){
        powerChart.destroy();
    }


    if(temperatureChart){
        temperatureChart.destroy();
    }


    if(humidityChart){
        humidityChart.destroy();
    }






    // Temperature chart


    let tempCanvas = document.getElementById("temperatureChart");


    if(tempCanvas && tempValues.length > 0){


        temperatureChart = new Chart(
            tempCanvas,
            {

                type:"line",

                data:{

                    labels:tempLabels,

                    datasets:[{

                        label:"Temperature °C",

                        data:tempValues,

                        tension:0.3

                    }]

                }

            }

        );

    }






    // Power chart


    let powerCanvas = document.getElementById("powerChart");


    if(powerCanvas && powerValues.length > 0){


        powerChart = new Chart(

            powerCanvas,

            {

                type:"line",

                data:{

                    labels:powerLabels,

                    datasets:[{

                        label:"Power Consumption W",

                        data:powerValues,

                        tension:0.3

                    }]

                }

            }

        );

    }






    // Humidity chart


    let humidityCanvas = document.getElementById("humidityChart");


    if(humidityCanvas && humidityValues.length > 0){


        humidityChart = new Chart(

            humidityCanvas,

            {

                type:"line",

                data:{

                    labels:humidityLabels,

                    datasets:[{

                        label:"Humidity %",

                        data:humidityValues,

                        tension:0.3

                    }]

                }

            }

        );

    }



}






// Initial load

loadSensors();



// Refresh every 5 seconds
setInterval(loadSensors,10000);
