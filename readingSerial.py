import serial
from datetime import datetime
ser = serial.Serial('/dev/cu.usbserial', timeout=None, baudrate=9600, xonxoff=False, rtscts=False, dsrdtr=False)
ser.flushInput()


while True:
  f=open("datalogReceptor.txt", "a+")
  info = ser.readline()
  now = datetime.now()
  print(now)
  f.write("\n"+str(now)+"\n")
  f.write(str(info))
  print(str(info))
