import serial
import time

ser = serial.Serial('COM3', 9600)
time.sleep(2)
for i in range(0,100):
    b = ser.readline()
    b = b.decode('utf-8').strip()
    pindisp = int(b.split(",")[0][1:])
    signaldisp = b.split(",")[1]
    print(pindisp)
ser.close()