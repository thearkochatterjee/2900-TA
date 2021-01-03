import serial
import time

ser = serial.Serial('COM3', 9600)
time.sleep(2)

motor_state = list()
for i in range(0, 14):
    motor_state.append(False)


def cylinder_state_detection(intake_pin, exhaust_pin):
    if motor_state[intake_pin] and not motor_state[exhaust_pin]:
        return True
    else:
        return False


def update_pins(pin, signal):
    global motor_state
    if signal == "1":
        motor_state[pin] = True
    else:
        motor_state[pin] = False


startcylinder = 1

for i in range(0, 100):
    b = ser.readline()
    b = b.decode('utf-8').strip()
    if b.startswith("%"):
        pindisp = int(b.split(",")[0][1:])
        signaldisp = b.split(",")[1]
        update_pins(pindisp, signaldisp)
        if cylinder_state_detection(startcylinder * 2, startcylinder * 2 + 1):
            ser.write('1'.encode('utf-8'))
            ser.flush()
            startcylinder += 1
            if startcylinder == 7:
                startcylinder = 1
            print(startcylinder)
    # print(b)
ser.close()
