import serial
from serial import Serial
from datetime import datetime, timedelta
import time
import threading
import csv
from os import path as fileExist

#		ID date time temp pres vol timeDelta
all_IDs = [[],[],[],[],[],[],[]]
dev_path = ''

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

def cleanRaw(raw_msg):
  msg = ''
  raw_msg = raw_msg[2:]
  #print(len(raw_msg))
  for x in range(len(raw_msg)):
  	if(raw_msg[x]!='\\' and raw_msg[x+1]!='r'): 
  		msg+=raw_msg[x]
  	else :
  	  	break; 
  return msg;

def voltage(code):
	vConst = 0.01
	value = vConst*code + 1.22
	return value

def temperature(code):
	vConst = 1
	value = vConst*code - 55
	return value

def pressure(Mcode, Lcode):
	code = Mcode<<8 | int(Lcode)
	vConst = 2.75
	psiConst = 0.145038
	value = vConst*code + 97.75
	value = value*psiConst
	return value

def extract(msg):
	global all_IDs
	if(msg[0]=='$' and len(msg) > 5):
	  	tmp = msg[13:];
	  	ID = tmp[0:2]+tmp[3:5]+tmp[6:8]+tmp[9:11]
	  	#print(ID)
	  	TCODE = "0x"+tmp[14:16]
	  	VCODE = "0x"+tmp[17:19]
	  	PM	= 	"0x"+tmp[20:22]
	  	PL	=	"0x"+tmp[23:25]
	  	tHex = int(TCODE,16)
	  	vHex = int(VCODE,16)
	  	pmHex = int(PM,16)
	  	if(pmHex==0xff):
	  		pmHex = 0x00
	  	plHex= int(PL,16)
	  	if(plHex==0x00):
	  	    plHex = 0x01;
	  	volt = round(voltage(vHex),2)
	  	temp = round(temperature(tHex),2)
	  	pres = round(pressure(pmHex,plHex),2)
	  	all_IDs[0].append(ID)
	  	now = datetime.now()
	  	now=now.strftime("%y-%m-%d %H:%M:%S")
	  	date,time = str(now).split()
	  	all_IDs[1].append(date)
	  	all_IDs[2].append(time)
	  	all_IDs[3].append(temp)
	  	all_IDs[4].append(pres)
	  	all_IDs[5].append(volt)
	  	#print(len(all_IDs[0]))
	  	minutes=0.
	  	if(len(all_IDs[0])==1):
	  		all_IDs[6].append(minutes)
	  		saveCSV()
	  		print("ID: ", ID, "T: ", temp, "V: ", volt, "P: ", pres, "DELTA: ", minutes)
	  	elif(len(all_IDs[0])>1):
	  		minutes=timeDiff(time,all_IDs[2][-2])
	  		if(minutes>=1):	
	  			all_IDs[6].append(minutes)
	  			saveCSV()
	  			print("ID: ", ID, "T: ", temp, "V: ", volt, "P: ", pres, "DELTA: ", minutes)
	  		

def saveCSV():
  global all_IDs
  with open(str(all_IDs[0][-1])+'.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["ID", str(all_IDs[0][-1]),"DATE", str(all_IDs[1][-1]),"TIME", str(all_IDs[2][-1]),"TEMPERATURE", str(all_IDs[3][-1]),"PRESSURE", str(all_IDs[4][-1]),"VOLTAGE", str(all_IDs[5][-1]),"deltaTime:", str(all_IDs[6][-1])])

def serialRead():
    ser = serial.Serial(dev_path, timeout=None, baudrate=9600, xonxoff=False, rtscts=False, dsrdtr=False)
    ser.flushInput()
    while True:
      info = ser.readline()
      msg = cleanRaw(str(info));
      extract(msg) 

def setEnv():
	global dev_path
	arg = []
	clean = ''
	if fileExist.exists("env.txt"):
		with open("env.txt", 'r') as csvfile:
			plots = csv.reader(csvfile, delimiter='\n')
			for row in plots:
				arg.append(str(row))
			arg[0]=arg[0][2:]
			for x in arg[0]:
				if x=="'":
					break
				else:
					clean+=x
			print(clean)
			dev_path=clean
		return True
	else :
		return False

if __name__ == '__main__':
	value = setEnv()
	print(value)
	if(value):
		serialReading = threading.Thread(target=serialRead)
		serialReading.start()