from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import filedialog
import serial
import time

# pip install pyserial

root = Tk()
root.title("Air Motor Simulator")

frame_motor = LabelFrame(root, text="Air Motor")
frame_controls = LabelFrame(root, text="Controls")
frame_translate = LabelFrame(root, text="Translate Code")
frame_serial_monitor = LabelFrame(root, text="Sim Serial Monitor")

frame_motor.grid(row=0, column=0)
frame_translate.grid(row=1, column=0)
frame_controls.grid(row=1, column=1)
frame_serial_monitor.grid(row=0,column=1)

Label(frame_controls, text="COM Port:").grid(row=1, column=0)
txtport = Entry(frame_controls)
txtport.grid(row=1, column=1)
Label(frame_controls, text="Number of Iterations to Run Motor for:").grid(row=2, column=0)
txtiteration = Entry(frame_controls)
txtiteration.insert(0,"10")
txtiteration.grid(row=2, column=1)

img_air_motor = Image.open("air motor.png")
activate = Image.open("activate cylinder.png")
deactivate = Image.open("deactivate cylinder.png")

num_iterations = 0
serial_count = 0
translated = False

def translate_digitalwrite(line):
    if line.startswith("digitalWrite"):
        components = line.split(",")
        pinvalue = components[0][(components[0].index("(") + 1):]
        signal = components[1][:(components[1].index(")"))]
        pinout = ""
        signalout = ""
        if pinvalue[0] in "0123456789":
            pinout = "\"" + pinvalue + "\""
        else:
            pinout = pinvalue
        return "Serial.println(" + pinout + "+\",\"+" + signal + ");"


def translate_code():
    global raw_code
    global trans_code
    global path
    global translated
    trans_code = []
    path = filedialog.askopenfilename(initialdir="D:/", title="Select A File",
                                      filetypes=(("ino files", "*.ino"), ("all files", "*.*")))
    if path == "":
        messagebox.showerror("No Valid Path", "There is no path for code entered!")
    else:
        ocode = open(path, "r")
        raw_code = ocode.readlines()
        ocode.close()
        for line in raw_code:
            try:
                if line.index("digitalWrite") >= 0:
                    trans_code.append(translate_digitalwrite(line.strip()) + "\n")
            except ValueError:
                trans_code.append(line)
        translated = True
        ocode = open(path, "w")
        ocode.writelines(trans_code)
        ocode.close()
        messagebox.showinfo("Translation Complete",
                            "Arduino Code has been translated. Please re-upload code to arduino.")


def print_to_serial_monitor(line):
    global serial_count
    serial_count += 1
    Label(frame_serial_monitor, text=line).grid(row=serial_count, column=0)



def start():
    if translated:
        if txtport.get() == "":
            messagebox.showerror("Invalid COM Port", "COM port must be entered")
        else:
            serial_count = 0
            port = "COM" + txtport.get()
            try:
                num_iterations = int(txtiteration.get())
            except:
                messagebox.showerror("Invalid Iteration", "Please put in an integer value for the number of "
                                                          "iterations to run the motor.")
            try:
                ser = serial.Serial(port, 9600)
                for i in range(0, num_iterations):
                    data = ser.readline()
                    data = data.decode('utf-8').strip()
                    print_to_serial_monitor(data)
            except:
                messagebox.showerror("Port Error", "Invalid Port")

    else:
        messagebox.showerror("Code Translation", "Code has not been translated")


def revert_code():
    if path != "":
        trans_code = []
        translated = False
        ocode = open(path, "w")
        ocode.writelines(raw_code)
        ocode.close()
        messagebox.showinfo("Code Reverted", "The Arduino Code has been changed back to the original code.")
    else:
        messagebox.showerror("No Code Path", "No code path has been declared")


def clear_code():
    path = ""
    raw_code = ""
    trans_code = ""
    translated = False


cmdtranslatecode = Button(frame_translate, text="Translate Code", command=translate_code)
cmdrevert = Button(frame_translate, text="Revert Code", command=revert_code)
cmdstart = Button(frame_controls, text="Start Motor", command=start)
cmdclear = Button(frame_translate, text="Clear Code Memory", command=clear_code)

cmdtranslatecode.grid(row=1, column=0)
cmdrevert.grid(row=2, column=0)
cmdstart.grid(row=0, column=0, columnspan=2)
cmdclear.grid(row=3, column=0)

root.mainloop()
