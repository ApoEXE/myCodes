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
path = '/home/ubuntu'
device = '/dev/ttyUSB0'
from datetime import datetime


from flask import Flask, Response, render_template, request, session
import csv
app = Flask(__name__)





date1 = []
date2 = []
date3 = []
date4 = []
date5 = []
date6 = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chart-data1')
def chart_data1():
    def generate_random_data():
        global date1

        with open(path+'myCodes/tpms' + str(1) + '.csv', 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')

            for row in plots:
                try:
                    if (date1.index(row[0])):
                        pass
                except:
                    date1.append(row[0])
                    json_data = json.dumps({'time': row[0], 'value': row[1]})
                    yield f"data:{json_data}\n\n"  # like a return
                    time.sleep(0.05)

    return Response(generate_random_data(), mimetype='text/event-stream')

@app.route('/chart-data2')
def chart_data2():
    def generate_random_data():
        global date2
        with open(path+'myCodes/tpms' + str(2) + '.csv', 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')

            for row in plots:
                try:
                    if (date2.index(row[0])):
                        pass
                except:
                    date2.append(row[0])
                    json_data = json.dumps({'time': row[0], 'value': row[1]})
                    yield f"data:{json_data}\n\n"  # like a return
                    time.sleep(0.05)

    return Response(generate_random_data(), mimetype='text/event-stream')

@app.route('/chart-data3')
def chart_data3():
    def generate_random_data():
        global date6
        with open(path+'myCodes/tpms' + str(3) + '.csv', 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')

            for row in plots:
                try:
                    if (date3.index(row[0])):
                        pass
                except:
                    date3.append(row[0])
                    json_data = json.dumps({'time': row[0], 'value': row[1]})
                    yield f"data:{json_data}\n\n"  # like a return
                    time.sleep(0.05)

    return Response(generate_random_data(), mimetype='text/event-stream')

@app.route('/chart-data4')
def chart_data4():
    def generate_random_data():
        global date4
        with open(path+'myCodes/tpms' + str(4) + '.csv', 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')

            for row in plots:
                try:
                    if (date4.index(row[0])):
                        pass
                except:
                    date4.append(row[0])
                    json_data = json.dumps({'time': row[0], 'value': row[1]})
                    yield f"data:{json_data}\n\n"  # like a return
                    time.sleep(0.05)

    return Response(generate_random_data(), mimetype='text/event-stream')

@app.route('/chart-data5')
def chart_data5():
    def generate_random_data():
        global date5
        with open(path+'myCodes/tpms' + str(5) + '.csv', 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')

            for row in plots:
                try:
                    if (date5.index(row[0])):
                        pass
                except:
                    date5.append(row[0])
                    json_data = json.dumps({'time': row[0], 'value': row[1]})
                    yield f"data:{json_data}\n\n"  # like a return
                    time.sleep(0.05)

    return Response(generate_random_data(), mimetype='text/event-stream')

@app.route('/chart-data6')
def chart_data6():
    def generate_random_data():
        global date6
        with open(path+'myCodes/tpms' + str(6) + '.csv', 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')

            for row in plots:
                try:
                    if (date6.index(row[0])):
                        pass
                except:
                    date6.append(row[0])
                    json_data = json.dumps({'time': row[0], 'value': row[1]})
                    yield f"data:{json_data}\n\n"  # like a return
                    time.sleep(0.05)

    return Response(generate_random_data(), mimetype='text/event-stream')



def Download_Csv():
    while True:
        os.system('scp -i ' + path + 'system_key root@192.168.3.250:/sdcard/tpms* ' + path + 'myCodes/')
        time.sleep(30)


def toThread():
    ser = serial.Serial(device, timeout=None, baudrate=9600, xonxoff=False, rtscts=False, dsrdtr=False)
    ser.flushInput()

    while True:
        f = open("datalogReceptor.txt", "a+")
        info = ser.readline()
        f.write(info.decode("utf-8"))
        print(info.decode("utf-8"))
    f.close()

if __name__ == '__main__':

    x = threading.Thread(target=toThread)
    x.start()
    y = threading.Thread(target=Download_Csv)
    y.start()
    app.run(debug=True, threaded=True, host= '0.0.0.0', port=80)
