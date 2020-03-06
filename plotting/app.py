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
from livereload import Server, shell
from flask import Flask, Response, render_template, request, session
from flask_caching import Cache
import csv
import csvData
app = Flask(__name__)


#DECLARATIONS
#path = '/home/ubuntu/'
path = '/Users/jav/'
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



@app.route('/')
def index():
    return render_template('index.html',report=_report)


@app.route('/chart-data1')
def chart_data1():
    print("DOWNLOADING")
    #os.system('scp -i ' + path + 'system_key root@192.168.3.250:/sdcard/tpms* ' + path + 'myCodes/')
    reporting()
    def generate_random_data():
        global _date,_temp, increment
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

def reporting():
    global _date, _temp, _report
    print("REPORTING")
    csvData.extract_all(path)
    _report,_date,_temp =csvData.getData()
        #print(len(_date[0]))
        #for x in range(6):
         #for y in range(len(_date[x])):
            #print('2 dimention list: ', _date[x][y], ' len(',x+1,'): ',len(_date[x]), ' temp: ',_temp[x][y])
    time.sleep(60)




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

    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)
    #server = Server(app.wsgi_app)
    #server.serve()

    #app.run(debug=True, threaded=True, host= '0.0.0.0', port=80)




