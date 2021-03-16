
$(document).ready(function () {
        const config = {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: "Temperature 1",
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 99, 132)',
                    data: [],
                    fill: false,
                }],
            },
            options: {
                responsive: true,
                animation: {
                    duration: 0 // general animation time
                },
                title: {
                    display: true,
                    text: 'TPMS'
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                },
                hover: {
                    mode: 'nearest',
                    intersect: true
                },
                scales: {
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Time'
                        }
                    }],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Value'
                        }
                    }]
                }
            }
        };

        const context = document.getElementById('canvas1').getContext('2d');

        const lineChart = new Chart(context, config);

        const source = new EventSource("/_sensor1");

        source.onmessage = function (event) {
            const data = JSON.parse(event.data);
            if(data.reset==1){
                config.data.labels=[];
                config.data.datasets[0].data=[];
            }
            if (config.data.labels.length === 200) {
                config.data.labels.shift();
                config.data.datasets[0].data.shift();
            }
        
            /*
            for (let index = 0; index < data.date.length; index++) {
                config.data.labels.push(data.date[index]);
                config.data.datasets[0].data.push(data.temp[index]);
                lineChart.update();
                
            }
            */
           config.data.labels.push(data.date);
           config.data.datasets[0].data.push(data.temp);
           lineChart.update();
        }
        

    });