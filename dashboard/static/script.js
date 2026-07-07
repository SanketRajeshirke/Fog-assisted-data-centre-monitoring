Xfunction loadSensors() {

    fetch("/api/sensors")
    .then(response => response.json())
    .then(data => {


        let sensorTable =
        document.getElementById("sensorTable");


        let alertTable =
        document.getElementById("alertTable");


        // Clear old data before refreshing
        sensorTable.innerHTML = "";
        alertTable.innerHTML = "";


        let alerts = 0;


        document.getElementById("totalSensors").innerHTML = data.length;



        data.forEach(sensor => {


            let row = `

            <tr>
            <td>${sensor.sensor_id}</td>
            <td>${sensor.type}</td>
            <td>${sensor.value}</td>
            <td>${sensor.anomaly}</td>
            <td>${sensor.processed_by}</td>
            </tr>

            `;


            sensorTable.innerHTML += row;



            if(sensor.anomaly === true){


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


    })

    .catch(error => {

        console.error(
            "Error loading sensor data:",
            error
        );

    });


}


// Initial dashboard load
loadSensors();


// Refresh every 5 seconds
setInterval(loadSensors, 5000);
