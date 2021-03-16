import serial

with serial.Serial('/dev/ttyUSB0', 9600, timeout=120) as ser:
 print(ser.readline())
