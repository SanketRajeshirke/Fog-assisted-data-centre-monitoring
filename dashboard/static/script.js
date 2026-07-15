let powerChart;
let temperatureChart;
let humidityChart;


function loadSensors() {


fetch("/api/sensors")


.then(response => response.json())


.then(data => {


console.log("API DATA:", data);



const sensorTable = document.getElementById("sensorTable");
const alertTable = document.getElementById("alertTable");



if(!sensorTable || !alertTable){
    console.error("Table elements missing");
    return;
}



sensorTable.innerHTML = "";
alertTable.innerHTML = "";



let activeAlerts = 0;
let criticalAlerts = 0;
let warningAlerts = 0;

let currentPower = 0;




const totalSensors =
document.getElementById("totalSensors");

if(totalSensors){
    totalSensors.innerHTML = data.length;
}





data.forEach(sensor => {



let severity = "NORMAL";



let value = sensor.value;


// convert numeric strings to numbers

let numericValue = Number(value);



if(sensor.anomaly === true || sensor.anomaly === "true"){


activeAlerts++;

severity="WARNING";



if(
sensor.type === "smoke" ||
sensor.type === "door"
){

severity="CRITICAL";

criticalAlerts++;


}
else{

warningAlerts++;

}



let alertRow = `

<tr>

<td>${sensor.sensor_id}</td>

<td>${sensor.type}</td>

<td>${sensor.value}</td>

<td>${severity}</td>

<td>OPEN</td>

</tr>

`;


alertTable.innerHTML += alertRow;


}





if(
sensor.type === "power" &&
!isNaN(numericValue)
){

currentPower = numericValue;

}





let row = `


<tr>

<td>${sensor.sensor_id}</td>

<td>${sensor.type}</td>

<td>${sensor.value}</td>

<td>${sensor.anomaly}</td>

<td>${severity}</td>

<td>${sensor.processed_by}</td>


</tr>


`;



sensorTable.innerHTML += row;



});






updateCard(
"totalAlerts",
activeAlerts
);


updateCard(
"criticalAlerts",
criticalAlerts
);



updateCard(
"warningAlerts",
warningAlerts
);



updateCard(
"currentPower",
currentPower + " W"
);




createCharts(data);



})


.catch(error=>{

console.error(
"Dashboard Error:",
error
);

});


}







function updateCard(id,value){

let element =
document.getElementById(id);


if(element){

element.innerHTML=value;

}

}









function createCharts(data){


let powerLabels=[];
let powerValues=[];


let tempLabels=[];
let tempValues=[];


let humidityLabels=[];
let humidityValues=[];





data.forEach(sensor=>{


let value = Number(sensor.value);



if(
sensor.type==="power" &&
!isNaN(value)
){

powerLabels.push(sensor.timestamp);

powerValues.push(value);


}




if(
sensor.type==="temperature" &&
!isNaN(value)
){

tempLabels.push(sensor.timestamp);

tempValues.push(value);


}




if(
sensor.type==="humidity" &&
!isNaN(value)
){

humidityLabels.push(sensor.timestamp);

humidityValues.push(value);


}



});





console.log(
"Power chart data:",
powerValues
);


console.log(
"Temperature chart data:",
tempValues
);


console.log(
"Humidity chart data:",
humidityValues
);







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







loadSensors();



setInterval(
loadSensors,
10000
);
