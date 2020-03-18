let data1 = {};
function extractCsv() {
    const source = new EventSource("/extract_data");
}

function viewData(value) {
    //let source = new EventSource("/");
    
    console.log(data1[0]);
    //data1 = {{data[1]}};
    //data2 = {{data[2]}};
    //data3 = {{data[3]}};
    //data4 = {{data[4]}};
    //data5 = {{data[5]}};
    //data6 = {{data[6]}};

    document.getElementById("sensor1").innerHTML =
        "<td>   1   </td>" +
        "<td>" + data1[1] + "</td>" +
        "<td>" + data1[2] + "</td>" +
        "<td>" + data1[3] + "</td>" +
        "<td>" + data1[4] + "</td>" +
        "<td>" + data1[5] + "</td>" +
        "<td>" + data1[6] + "</td>" +
        "<td>" + data1[7] + "</td>";
    /*
    document.getElementById("sensor2").innerHTML =
        "<td>   2   </td>" +
        "<td>" + data2[1] + "</td>" +
        "<td>" + data2[2] + "</td>" +
        "<td>" + data2[3] + "</td>" +
        "<td>" + data2[4] + "</td>" +
        "<td>" + data2[5] + "</td>" +
        "<td>" + data2[6] + "</td>" +
        "<td>" + data2[7] + "</td>";
    
                document.getElementById("sensor3").innerHTML = 
                    "<td>   3   </td>" +
                    "<td>" + data3[1] + "</td>" +
                    "<td>" + data3[2] + "</td>" +
                    "<td>" + data3[3] + "</td>" +
                    "<td>" + data3[4] + "</td>" +
                    "<td>" + data3[5]+ "</td>" +
                    "<td>" + data3[6] + "</td>" +
                    "<td>" + data3[7] + "</td>"+;
                    
                document.getElementById("sensor4").innerHTML = 
                    "<td>   4   </td>" +
                    "<td>" + data4[1] + "</td>" +
                    "<td>" + data4[2] + "</td>" +
                    "<td>" + data4[3] + "</td>" +
                    "<td>" + data4[4] + "</td>" +
                    "<td>" + data4[5]+ "</td>" +
                    "<td>" + data4[6] + "</td>" +
                    "<td>" + data4[7] + "</td>";
                document.getElementById("sensor5").innerHTML = 
                    "<td>   5   </td>" +
                    "<td>" + data5[1] + "</td>" +
                    "<td>" + data5[2] + "</td>" +
                    "<td>" + data5[3] + "</td>" +
                    "<td>" + data5[4] + "</td>" +
                    "<td>" + data5[5]+ "</td>" +
                    "<td>" + data5[6] + "</td>" +
                    "<td>" + data5[7] + "</td>";
                document.getElementById("sensor6").innerHTML = 
                    "<td>   6   </td>" +
                    "<td>" + data6[1] + "</td>" +
                    "<td>" + data6[2] + "</td>" +
                    "<td>" + data6[3] + "</td>" +
                    "<td>" + data6[4] + "</td>" +
                    "<td>" + data6[5]+ "</td>" +
                    "<td>" + data6[6] + "</td>" +
                    "<td>" + data6[7] + "</td>";
                    */
}

function setValue(value){
    data1 = value;
    console.log(data1);
}

setInterval(viewData, 2000);

//setInterval(extractCsv, 10000);
