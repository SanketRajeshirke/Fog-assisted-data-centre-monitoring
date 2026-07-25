let powerChart;
let temperatureChart;
let humidityChart;


// ===============================
// LOAD SENSOR DATA
// ===============================

function loadSensors() {


fetch("/api/sensors")


.then(response => response.json())


.then(data => {


console.log("Sensor Data:", data);



const sensorTable =
document.getElementById("sensorTable");



if(!sensorTable){

console.error("sensorTable missing");

return;

}



sensorTable.innerHTML = "";



data.forEach(sensor => {



let severity =
sensor.severity || "NORMAL";



let row = `

<tr>

<td>${sensor.sensor_id}</td>

<td>${sensor.type}</td>

<td>${sensor.value}</td>

<td>${sensor.anomaly}</td>

<td>${severity}</td>

<td>${sensor.processed_by}</td>

<td>${sensor.timestamp}</td>


</tr>

`;



sensorTable.innerHTML += row;



});



createCharts(data);



})


.catch(error=>{


console.error(
"Sensor API Error:",
error
);


});



}





// ===============================
// LOAD SUMMARY KPI
// ===============================


function loadSummary(){



fetch("/api/summary")


.then(response=>response.json())


.then(data=>{


console.log(
"Summary:",
data
);



updateCard(
"totalRecords",
data.total_records
);



updateCard(
"activeAlerts",
data.active_alerts
);



updateCard(
"criticalAlerts",
data.critical_alerts
);



updateCard(
"currentPower",
data.current_power + " W"
);



})



.catch(error=>{


console.error(
"Summary API Error:",
error
);


});


}







// ===============================
// LOAD BUSINESS ALERTS
// ===============================


function loadAlerts(){



fetch("/api/alerts")


.then(response=>response.json())


.then(data=>{


console.log(
"Alerts:",
data
);



const alertTable =
document.getElementById("alertTable");



if(!alertTable){

return;

}



alertTable.innerHTML="";



data.forEach(alert=>{


let row = `


<tr>

<td>${alert.sensor_id}</td>

<td>${alert.type}</td>

<td>${alert.value}</td>

<td>${alert.severity}</td>

<td>${alert.timestamp}</td>


</tr>


`;



alertTable.innerHTML += row;



});



})


.catch(error=>{


console.error(
"Alert API Error:",
error
);


});


}









// ===============================
// LOAD ANALYTICS
// ===============================


function loadAnalytics(){



fetch("/api/analytics")


.then(response=>response.json())


.then(data=>{


console.log(
"Analytics:",
data
);


})


.catch(error=>{


console.error(
"Analytics API Error:",
error
);


});



}









// ===============================
// UPDATE KPI CARD
// ===============================


function updateCard(id,value){


let element =
document.getElementById(id);



if(element){


element.innerHTML=value;


}


}









// ===============================
// CREATE CHARTS
// ===============================


function createCharts(data){



let powerLabels=[];
let powerValues=[];


let tempLabels=[];
let tempValues=[];


let humidityLabels=[];
let humidityValues=[];





data.forEach(sensor=>{


let value =
Number(sensor.value);




if(
sensor.type==="power"
&&
!isNaN(value)

){


powerLabels.push(sensor.timestamp);

powerValues.push(value);


}






if(
sensor.type==="temperature"
&&
!isNaN(value)

){


tempLabels.push(sensor.timestamp);

tempValues.push(value);


}






if(
sensor.type==="humidity"
&&
!isNaN(value)

){


humidityLabels.push(sensor.timestamp);

humidityValues.push(value);


}



});






console.log(
"Power Chart:",
powerValues
);


console.log(
"Temperature Chart:",
tempValues
);


console.log(
"Humidity Chart:",
humidityValues
);







// POWER


if(powerChart){

powerChart.destroy();

}



let powerCanvas =
document.getElementById("powerChart");



if(powerCanvas){


powerChart = new Chart(
powerCanvas,
{


type:"line",


data:{


labels:powerLabels,


datasets:[{


label:"Power Consumption (W)",


data:powerValues


}]


}


});


}









// TEMPERATURE


if(temperatureChart){

temperatureChart.destroy();

}



let tempCanvas =
document.getElementById("temperatureChart");



if(tempCanvas){


temperatureChart = new Chart(
tempCanvas,
{


type:"line",


data:{


labels:tempLabels,


datasets:[{


label:"Temperature °C",


data:tempValues


}]


}


});


}









// HUMIDITY


if(humidityChart){

humidityChart.destroy();

}



let humidityCanvas =
document.getElementById("humidityChart");



if(humidityCanvas){



humidityChart = new Chart(
humidityCanvas,
{


type:"line",


data:{


labels:humidityLabels,


datasets:[{


label:"Humidity %",


data:humidityValues


}]


}


});


}



}








// ===============================
// INITIAL LOAD
// ===============================


loadSensors();

loadSummary();

loadAlerts();

loadAnalytics();





// Refresh every 10 seconds


setInterval(()=>{


loadSensors();

loadSummary();

loadAlerts();

loadAnalytics();


},10000);
