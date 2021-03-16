function extractCsv(){
    const source = new EventSource("/extract_data");
}

function viewData(){
    const source = new EventSource("/");
    data1 = {1,2,3,4,5,6,7};

    document.getElementById("sensor1").innerHTML =
        "<td>   1   </td>" +
        "<td>" + data1[1] + "</td>" +
        "<td>" + data1[2] + "</td>" +
        "<td>" + data1[3] + "</td>" +
        "<td>" + data1[4] + "</td>" +
        "<td>" + data1[5] + "</td>" +
        "<td>" + data1[6] + "</td>" +
        "<td>" + data1[7] + "</td>";
 }
setInterval(viewData, 2000);

setInterval(extractCsv, 10000);