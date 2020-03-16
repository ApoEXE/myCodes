#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __license__ = "MIT"
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import json
import serial
import threading
import time
import os
from datetime import datetime
from flask import Flask, Response, render_template, request, session
import csv
import csvData
app = Flask(__name__)


#DECLARATIONS
#path = '/home/ubuntu/'
path = '/home/jav/'
device = '/dev/ttyUSB0'


downloaded = False

_date = []
_temp = []

increment = 0

_report = {
    "Sensor":0,
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



@app.route('/', methods=['GET'])
def index():
    global _report
    return render_template('index.html',data=_report)


@app.route('/chart-data1')
def chart_data1():

    def generate_random_data():
        global _date,_temp, increment
        #_report, _data_temp = reporting()
        data1 = {'report': _report}
        #print('time: ', _date[0][x], 'value: ', _temp[0][x])
        #json_data = json.dumps({'time': _date[0][x], 'value': _temp[0][x]})
        #time.sleep(0.005)
        if increment<len(_date):
            json_data = json.dumps({'time': _date[0][increment], 'value': _temp[0][increment]})
            increment += 1
            yield f"data:{json_data}\n\n"  # like a return
            print(increment)



    return Response(generate_random_data(), mimetype='text/event-stream')


def Download_Csv():
    while True:
        os.system('scp -i ' + path + 'system_key root@192.168.3.250:/sdcard/tpms* ' + path + 'myCodes/')
        time.sleep(120)

        
@app.route("/extract_data")
def reporting():
    global _date, _temp, _report
    csvData.extract_all(path)
    _report,_date,_temp =csvData.getData()




def serialCom():
    ser = serial.Serial(device, timeout=None, baudrate=9600, xonxoff=False, rtscts=False, dsrdtr=False)
    ser.flushInput()

    while True:
        f = open("datalogReceptor.txt", "a+")

        info = ser.readline()
        f.write(info.decode("utf-8"))
        print(info.decode("utf-8"))
    f.close()

if __name__ == '__main__':
    reporting()
    #x = threading.Thread(target=reporting)
    #x.start()
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)



