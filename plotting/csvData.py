import csv
from datetime import datetime, timedelta
from os import path as fileExist



path = ''
file = ''
date = []
datet = [[0],[0],[0],[0],[0],[0]]
tempt = [[0],[0],[0],[0],[0],[0]]
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

summary =[[0],[0],[0],[0],[0],[0]]

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

def getData():
    return summary, datet, tempt

def extract_all(_path):
    global path
    path= _path
    for x in range(1,7):
        report["Sensor"]=x
        Extract_data()
        processData()
        extractEvents()
        processEvents()
        reportSensor()
        print("-------------------------------")

def Extract_data():
    global date,time,temp,diff,points, inc, datet
    subdate = []
    subtime = []
    subtemp = []
    subdiff = []
    subpoints = []
    inc = 0
    print(
        report["Sensor"]
    )
    with open(path +'myCodes/tpms'+str(report["Sensor"])+'.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            string = row[0]

            datet[report["Sensor"]-1].append(row[0]);
            tempt[report["Sensor"]-1].append(row[1]);

            txt = string.split()

            subdate.append(txt[0])
            subtime.append(txt[1])

            subtemp.append(int(row[1]))

            if (inc >= 1):
                minutes = timeDiff(subtime[-1],subtime[-2])
                if(minutes > 2 and minutes < 120):
                    #print(subtime[-1],' ',subtime[-2], 'minutes ', minutes )
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
    if(len(diff)>0):
     prom=prom/len(diff)
    cntDead = 0
    timebf=0
    for x in range(len(temp)):
        if temp[x]< 0:
            cntDead+=1
            timebf+=timeDiff(time[x],time[x-1])

    report["difftimeSensor"]=prom
    report["totalpointsSensor"]=len(date)
    report["biggestTimeSensor"]=max(diff)
    report["smallestTimeSensor"]=min(diff)
    report["totalpointsDead"]=cntDead
    if cntDead > 0:
        report["difftimeDead"] = (timebf/cntDead)




def extractEvents():
    global events
    events=[]
    print('###########Event File summary')
    if fileExist.exists(path + "myCodes/tpmsEvent.txt"):
      with open(path + 'myCodes/tpmsEvent.txt', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter='\n')
        for row in plots:
            if(len(row)>0):
                events.append(row)


def processEvents():
    global events,timeEvents,diffEvents
    z = 0#count TXFailed
    y = 0#clean Events
    timeEvents= []
    diffEvents = []
    prom = 0.

    for x in range(len(events)):
        aux = str(events[x])
        aux = aux[2:7]
        if aux == 'CLEAN':
            string = str(events[x-1]).split()
            temp = str(string[1])
            temp=temp[:8]
            print(len(timeEvents))
            timeEvents.append(temp)

            if y > 1:
                print(timeEvents)
                minutes = timeDiff(timeEvents[-1],timeEvents[-2])
                print(minutes)
                if (minutes > 1 and minutes < 120):
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
    global summary, report
    #x= report["Sensor"]-1
    #for y in range(len(datet[x])):
        #print('2 dimention list: ', datet[x][y], ' len(',x+1,'): ',len(datet[x]))
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


    summary[report["Sensor"]-1].append(report["difftimeSensor"])#0
    summary[report["Sensor"] - 1].append(report["totalpointsSensor"])#1
    summary[report["Sensor"] - 1].append(report["biggestTimeSensor"])#2
    summary[report["Sensor"] - 1].append(report["smallestTimeSensor"])#3
    summary[report["Sensor"] - 1].append(report["totalpointsDead"])#4
    summary[report["Sensor"] - 1].append(report["difftimeDead"])#5
    summary[report["Sensor"] - 1].append(report["totalpointsClean"])#6
    summary[report["Sensor"] - 1].append(report["difftimeClean"])#7
    summary[report["Sensor"] - 1].append(report["totalpointsTxFail"])#8



