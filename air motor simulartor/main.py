from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

# pip install pyserial

root = Tk()

frame_motor = LabelFrame(root, text="Air Motor")
frame_controls = LabelFrame(root, text="Controls")
frame_translate = LabelFrame(root, text="Translate Code")
frame_serial_monitor = LabelFrame(root, text="Sim Serial Monitor")

frame_motor.grid(row=0,column=0,columnspan=2)
frame_translate.grid(row=1,column=0)
frame_controls.grid(row=1,column=1)

activate_cylinders = []
deactivate_cylinders = []

for i in range(1,6):
    activate_cylinders.append(Image.open("cylinder "+ str(i)+" activate.png"))
    deactivate_cylinders.append(Image.open("cylinder "+str(i)+" deactivate.png"))

def translate_code():
    global raw_code
    global trans_code
    global path
    path = messagebox.askquestion("Path for Code","What is the path for the code?")
    ocode = open(path,"r")
    raw_code = ocode.readlines()
    ocode.close()

    ocode = open(path,"w")
    ocode.writelines(trans_code)
    ocode.close()

def start():
    return

def revert_code():
    ocode = open(path,"w")
    ocode.writelines(raw_code)
    ocode.close()

def clear_code():
    path = ""
    raw_code = ""

cmdtranslatecode = Button(frame_translate,text="Translate Code", command=translate_code)
cmdrevert = Button(frame_translate,text="Revert Code", command=revert_code)
cmdstart = Button(frame_controls,text="Start Motor", command=start)
cmdclear = Button(frame_translate,text="Clear Code Memory", command=clear_code)

root.mainloop()