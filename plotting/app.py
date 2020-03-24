#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __license__ = "MIT"
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
#FLASK_APP=app.py 
#FLASK_ENV=development 
#flask run
import json
import serial
import threading
import time
import os
from datetime import datetime
from flask import Flask, Response, render_template, request, session, jsonify
import csv
import csvData
app = Flask(__name__)


#DECLARATIONS
#path = '/home/ubuntu/'
#path = '/home/jav/'
path=''
#path = '/mnt/c/Users/Logistica/mss/'
device = '/dev/ttyUSB0'


downloaded = False

_date = []
_temp = []

increment = 1

_report = []
report = {
    "Sensor":1,
    "difftimeSensor": 0,
    "totalpointsSensor":0,
    "biggestTimeSensor":0,
    "smallestTimeSensor":0,
    "totalpointsDead":0,
    "difftimeDead":0,
    "difftimeClean":0,
    "totalpointsClean":0,
    "totalpointsTxFail":0
}

report1 = {
    "Sensor":1,
    "difftimeSensor": 0,
    "totalpointsSensor":0,
    "biggestTimeSensor":0,
    "smallestTimeSensor":0,
    "totalpointsDead":0,
    "difftimeDead":0,
    "difftimeClean":0,
    "totalpointsClean":0,
    "totalpointsTxFail":0
}
report2 = {
    "Sensor":2,
    "difftimeSensor": 0,
    "totalpointsSensor":0,
    "biggestTimeSensor":0,
    "smallestTimeSensor":0,
    "totalpointsDead":0,
    "difftimeDead":0,
    "difftimeClean":0,
    "totalpointsClean":0,
    "totalpointsTxFail":0
}
report3 = {
    "Sensor":3,
    "difftimeSensor": 0,
    "totalpointsSensor":0,
    "biggestTimeSensor":0,
    "smallestTimeSensor":0,
    "totalpointsDead":0,
    "difftimeDead":0,
    "difftimeClean":0,
    "totalpointsClean":0,
    "totalpointsTxFail":0
}
report4 = {
    "Sensor":4,
    "difftimeSensor": 0,
    "totalpointsSensor":0,
    "biggestTimeSensor":0,
    "smallestTimeSensor":0,
    "totalpointsDead":0,
    "difftimeDead":0,
    "difftimeClean":0,
    "totalpointsClean":0,
    "totalpointsTxFail":0
}
report5 = {
    "Sensor":5,
    "difftimeSensor": 0,
    "totalpointsSensor":0,
    "biggestTimeSensor":0,
    "smallestTimeSensor":0,
    "totalpointsDead":0,
    "difftimeDead":0,
    "difftimeClean":0,
    "totalpointsClean":0,
    "totalpointsTxFail":0
}
report6 = {
    "Sensor":6,
    "difftimeSensor": 0,
    "totalpointsSensor":0,
    "biggestTimeSensor":0,
    "smallestTimeSensor":0,
    "totalpointsDead":0,
    "difftimeDead":0,
    "difftimeClean":0,
    "totalpointsClean":0,
    "totalpointsTxFail":0
}

@app.route('/')
def index():
    global report1,report2,report3,report4,report5,report6
    #reporting()
    #return render_template('index.html',data1=json.dumps(report1),data2=json.dumps(report2),data3=json.dumps(report3),data4=json.dumps(report4),data5=json.dumps(report5),data6=json.dumps(report6))
    return render_template('index.html')

@app.route('/sensor1')
def chart_data1():
    global _date,_temp
    return render_template('sensor1.html',title='Sensor1', max=50, labels=_date[0], values=_temp[0])


def Download_Csv():
    while True:
        os.system('scp -i ' + path + 'system_key root@192.168.3.250:/sdcard/tpms* ' + path + 'data/')
        time.sleep(120)

        

def reporting():
    global _date, _temp, _report
    global report1, report2, report3, report4, report5, report6
    csvData.extract_all(path)
    _report,_date,_temp =csvData.getData()
    createDic(_report)
    print("UPDATED")


@app.route("/extract_data", methods=['POST'])
def extractData():
    with app.app_context():
        global report1, report2, report3, report4, report5, report6, increment,report

        reporting()
        if increment == 1:
            report=report1;
            increment+=1
        elif increment == 2:
            report=report2;
            increment+=1
        elif increment == 3:
            report=report3;
            increment+=1
        elif increment == 4:
            report=report4;
            increment+=1
        elif increment == 5:
            report=report5;
            increment+=1
        elif increment == 6:
            report=report6;
            increment+=1
        else:
            increment=1;

        return jsonify({'sensor': report[0],
                    'difftimeSensor': report[1],
                    'totalpointsSensor': report[2],
                    'biggestTimeSensor': report[3],
                    'smallestTimeSensor': report[4],
                    'totalpointsDead': report[5],
                    'difftimeDead': report[6],
                    'difftimeClean': report[7],
                    'totalpointsClean': report[8],
                    'totalpointsTxFail': report[9]})


def createDic(reportArray):
    global report1,report2, report3, report4, report5, report6
    for x in range(10):
        #print(x, end=" ")
        report1[x]=reportArray[0][x];
        report2[x]=reportArray[1][x];
        report3[x]=reportArray[2][x];
        report4[x]=reportArray[3][x];
        report5[x]=reportArray[4][x];
        report6[x]=reportArray[5][x];
        #print("")
    #for x in range(10):
        #print("x:",x,"value:",report1[x])
    #print(reportArray[0])


if __name__ == '__main__':

    #x = threading.Thread(target=Download_Csv)
    #x.start()
    reporting()
    app.run(debug=True, threaded=True, host='127.0.0.1', port=5000)



