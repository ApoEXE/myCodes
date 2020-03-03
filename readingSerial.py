import serial
ser = serial.Serial('/dev/cu.usbserial', timeout=None, baudrate=9600, xonxoff=False, rtscts=False, dsrdtr=False)
ser.flushInput()


while True:
  f=open("datalogReceptor.txt", "a+")
  info = ser.readline()
  f.write(info.decode("utf-8"))
  print(info.decode("utf-8"))
