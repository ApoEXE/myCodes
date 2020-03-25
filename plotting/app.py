#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __license__ = "MIT"
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
# FLASK_APP=app.py
# FLASK_ENV=development
# flask run
import json
import threading
import time
import os
from datetime import datetime
from flask import Flask, Response, render_template, request, session, jsonify
import csv
import csvData
app = Flask(__name__)


# DECLARATIONS
#path = '/home/ubuntu/'
#path = '/home/jav/'
path = ''
#path = '/mnt/c/Users/Logistica/mss/'
device = '/dev/ttyUSB0'


downloaded = False

_date = []
_temp = []

increment = 1
lastSize = 0
reset = 0
_report = []
report = {
    "Sensor": 1,
    "difftimeSensor": 0,
    "totalpointsSensor": 0,
    "biggestTimeSensor": 0,
    "smallestTimeSensor": 0,
    "totalpointsDead": 0,
    "difftimeDead": 0,
    "difftimeClean": 0,
    "totalpointsClean": 0,
    "totalpointsTxFail": 0
}

report1 = {
    "Sensor": 1,
    "difftimeSensor": 0,
    "totalpointsSensor": 0,
    "biggestTimeSensor": 0,
    "smallestTimeSensor": 0,
    "totalpointsDead": 0,
    "difftimeDead": 0,
    "difftimeClean": 0,
    "totalpointsClean": 0,
    "totalpointsTxFail": 0
}
report2 = {
    "Sensor": 2,
    "difftimeSensor": 0,
    "totalpointsSensor": 0,
    "biggestTimeSensor": 0,
    "smallestTimeSensor": 0,
    "totalpointsDead": 0,
    "difftimeDead": 0,
    "difftimeClean": 0,
    "totalpointsClean": 0,
    "totalpointsTxFail": 0
}
report3 = {
    "Sensor": 3,
    "difftimeSensor": 0,
    "totalpointsSensor": 0,
    "biggestTimeSensor": 0,
    "smallestTimeSensor": 0,
    "totalpointsDead": 0,
    "difftimeDead": 0,
    "difftimeClean": 0,
    "totalpointsClean": 0,
    "totalpointsTxFail": 0
}
report4 = {
    "Sensor": 4,
    "difftimeSensor": 0,
    "totalpointsSensor": 0,
    "biggestTimeSensor": 0,
    "smallestTimeSensor": 0,
    "totalpointsDead": 0,
    "difftimeDead": 0,
    "difftimeClean": 0,
    "totalpointsClean": 0,
    "totalpointsTxFail": 0
}
report5 = {
    "Sensor": 5,
    "difftimeSensor": 0,
    "totalpointsSensor": 0,
    "biggestTimeSensor": 0,
    "smallestTimeSensor": 0,
    "totalpointsDead": 0,
    "difftimeDead": 0,
    "difftimeClean": 0,
    "totalpointsClean": 0,
    "totalpointsTxFail": 0
}
report6 = {
    "Sensor": 6,
    "difftimeSensor": 0,
    "totalpointsSensor": 0,
    "biggestTimeSensor": 0,
    "smallestTimeSensor": 0,
    "totalpointsDead": 0,
    "difftimeDead": 0,
    "difftimeClean": 0,
    "totalpointsClean": 0,
    "totalpointsTxFail": 0
}

cnt = 0
@app.route('/')
def index():
    global cnt
    cnt=0
    return render_template('index.html', title='Sensor1', max=30)


@app.route('/_sensor', methods=['GET'])
def sensorData():
    global _date, _temp
    size = len(_date[0])
    newdate = [_date[0][(size-20):]]
    newtemp = [_temp[0][(size-20):]]
    return jsonify({'date': newdate[0], 'temp': newtemp[0]})


@app.route('/_sensor1', methods=['GET'])
def sensorLive():
    
    def generate_random_data():
        global lastSize, reset, cnt
        with app.app_context(): 
            global _date, _temp
            size = len(_date[0])
            newdate = [_date[0][(size-20):]]
            newtemp = [_temp[0][(size-20):]]
            size2 = len(newdate[0])
            if cnt < size2:
                lastSize = len(_date[0])
                json_data = json.dumps({'date': newdate[0][cnt], 'temp': newtemp[0][cnt], 'reset':reset})
                yield f"data:{json_data}\n\n"
                cnt+=1
                reset=0
            elif (size-lastSize)==1:
                lastSize = len(_date[0])
                json_data = json.dumps({'date': newdate[0][-1], 'temp': newtemp[0][-1], 'reset':reset})
                yield f"data:{json_data}\n\n"
            elif abs(size-lastSize)>1:
                cnt=0
                reset=1
            time.sleep(0.005)

    return Response(generate_random_data(), mimetype='text/event-stream')



def reporting():
    global _date, _temp, _report
    csvData.extract_all(path)
    _date = []
    _temp = []

    _report, _date, _temp = csvData.getData()
    createDic(_report)
    print("UPDATED")


@app.route("/extract_data", methods=['POST'])
def extractData():
    with app.app_context():
        global report1, report2, report3, report4, report5, report6, increment, report

        reporting()
        if increment == 1:
            report = report1
            increment += 1
        elif increment == 2:
            report = report2
            increment += 1
        elif increment == 3:
            report = report3
            increment += 1
        elif increment == 4:
            report = report4
            increment += 1
        elif increment == 5:
            report = report5
            increment += 1
        elif increment == 6:
            report = report6
            increment += 1
        else:
            increment = 1

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
    global report1, report2, report3, report4, report5, report6
    for x in range(10):
        #print(x, end=" ")
        report1[x] = reportArray[0][x]
        report2[x] = reportArray[1][x]
        report3[x] = reportArray[2][x]
        report4[x] = reportArray[3][x]
        report5[x] = reportArray[4][x]
        report6[x] = reportArray[5][x]
        # print("")
    # for x in range(10):
        # print("x:",x,"value:",report1[x])
    # print(reportArray[0])


if __name__ == '__main__':

    #x = threading.Thread(target=Download_Csv)
    # x.start()
    reporting()
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)

