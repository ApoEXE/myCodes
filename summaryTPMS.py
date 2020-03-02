#!/usr/bin/python

# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import csv
import os
import sys
import time
import datetime
from datetime import datetime, timedelta
from drawnow import drawnow
import os.path
from os import path as fileExist
plt.ion()  # tell matplotlib you want interactive mode to plot data

path = '/Users/jav/'
file = ''
date = []
time = []
temp = []
diff = []
points = []
string = ''
hour = []
prom = [0,0,0,0]
inc = 0
events = []

timeEvents = []
diffEvents = []


report = {
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



def makeFig():
    global time,temp,diff,points,prom
    wspace1 = 0.8
    hspace1 = 0.8
    plt.subplot(2,1,1)
    plt.xticks(fontsize=5)
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.3)
    plt.subplots_adjust(wspace=wspace1)
    plt.subplots_adjust(hspace=hspace1)
    plt.plot(time, temp, "o")
    plt.title('Sensor '+file)
    plt.ylabel('Temperature')

    plt.subplot(2,1,2)
    plt.xticks(fontsize=5)
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.subplots_adjust(wspace=wspace1)
    plt.subplots_adjust(hspace=hspace1)
    plt.plot(diff, points, "o")
    plt.title('diff distribution')
    plt.ylabel('points')
    plt.xlabel('Time Diff')


def Download_Csv():
    os.system('scp -i ' + path + 'system_key root@192.168.3.250:/sdcard/tpms* ' + path + 'myCodes/')

def Extract_data():
    global date,time,temp,diff,points, inc
    subdate = []
    subtime = []
    subtemp = []
    subdiff = []
    subpoints = []
    with open(path +'Downloads/tpms'+str(report["Sensor"])+'.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            string = row[0]
            txt = string.split()

            subdate.append(txt[0])
            subtime.append(txt[1])
            subtemp.append(int(row[1]))

            if (inc >= 1):
                minutes = timeDiff(subtime[-1],subtime[-2])
                subdiff.append(minutes)
                subdiff.sort()
                subpoints.append(inc)

            inc += 1

    date = subdate
    time = subtime
    temp = subtemp
    diff = subdiff
    points = subpoints


def processData():
    global points, diff
    prom=0
    for x in range(len(diff)):
        prom+=diff[x];
    prom=prom/len(diff)
    cntDead = 0
    timebf=0
    for x in range(len(temp)):
        if temp[x]< 0:
            cntDead+=1
            timebf+=timeDiff(time[x],time[x-1])

    report["difftimeSensor"]=prom
    report["totalpointsSensor"]=len(diff)
    report["biggestTimeSensor"]=max(diff)
    report["smallestTimeSensor"]=min(diff)
    report["totalpointsDead"]=cntDead
    if cntDead > 0:
        report["difftimeDead"] = (timebf/cntDead)




def extractEvents():
    global events
    with open(path + 'Downloads/tpmsEvent.txt', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter='\n')
        for row in plots:
            if(len(row)>0):
                events.append(row)
                #print(row)

def processEvents():
    global events,timeEvents,diffEvents
    z = 0#count TXFailed
    y = 0#clean Events
    prom = 0.
    for x in range(len(events)):
        aux = str(events[x])
        aux = aux[2:7]
        #print(aux)
        if aux == 'CLEAN':
            string = str(events[x-1]).split()
            aux = str(string[1])
            aux=aux[:8]
            timeEvents.append(aux)

            if y > 1:
                minutes = timeDiff(timeEvents[-1],timeEvents[-2])

                diffEvents.append(minutes)
                prom+= minutes
            y += 1
        if aux == 'TXFAI':
            z+=1
    promedio = 0;
    if (y-2) > 0:
        promedio = (prom/(y-2))
    timeEvents = timeEvents[2:]
    report["difftimeClean"]=promedio
    report["totalpointsClean"]=y
    report["totalpointsTxFail"]=z

def timeDiff(newtime, oldtime):
    newdate = datetime.strptime(newtime, '%H:%M:%S')
    olddate = datetime.strptime(oldtime, '%H:%M:%S')
    hour = newdate - olddate
    if (hour.total_seconds() < 0):
        string = str(hour)
        t = datetime.strptime('1900/01/01 00:00:00', "%Y/%m/%d %H:%M:%S")
        u = datetime.strptime(string[8:], "%H:%M:%S")
        hour = u - t
    seconds = hour.total_seconds()
    minutes = (seconds / 60.)
    return minutes

def reportSensor():
    print("Sensor: ",report["Sensor"])
    print("diff average S.: ", report["difftimeSensor"])
    print("Total points S.: ", report["totalpointsSensor"])
    print("Biggest diff S.: ", report["biggestTimeSensor"])
    print("Smallest diff S.: ", report["smallestTimeSensor"])
    print("Total dead S.: ", report["totalpointsDead"])
    print("diff average Dead S.: ", report["difftimeDead"])
    print("Total points Clean: ", report["totalpointsClean"])
    print("diff average Clean: ", report["difftimeClean"])
    print("Total points TxFail: ", report["totalpointsTxFail"])




def main():
    global inc,file
    file = sys.argv[1]
    print("######Reading: ",file)
    if len(sys.argv) > 1 :
        inc = 0
        Download_Csv()
        report["Sensor"]= int(file)
        print('############Process temperature files')

        Extract_data()
        processData()

            #drawnow(makeFig)
        print('###########Event File summary')
        if fileExist.exists(path+"Downloads/tpmsEvent.txt"):
            extractEvents()
            processEvents()

        reportSensor()
        makeFig()
        plt.show()
        plt.pause(120)
    else :
        print('missing tpms file')


if __name__ == '__main__':
    main()