var revisar=0;
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

        const source = new EventSource("/chart-data1");

        source.onmessage = function (event) {
            const data = JSON.parse(event.data);

            if (config.data.labels.length === 20000) {
                config.data.labels.shift();
                config.data.datasets[0].data.shift();
            }
            config.data.labels.push(data.time);
            config.data.datasets[0].data.push(data.value);
            //document.write(" dato at index last   "+config.data.labels[config.data.labels.length-1]);
            //document.write(" dato at index 0   "+config.data.labels[0]+"    ");
            lineChart.update();
        }

    });
