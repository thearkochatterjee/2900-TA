import os
import webbrowser
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import serial
from PIL import Image, ImageTk

# pip install pyserial

root = Tk()
root.title("Air Motor Simulator")
root.iconbitmap("icon.ico")

# Creating Subframes
frame_motor = LabelFrame(root, text="Air Motor")
frame_controls = LabelFrame(root, text="Controls")
frame_translate = LabelFrame(root, text="Translate Code")
frame_serial_monitor = LabelFrame(root, text="Sim Serial Monitor")

# Putting Frames in GUI
frame_motor.grid(row=0, column=0, rowspan=3)
frame_translate.grid(row=0, column=1)
frame_controls.grid(row=1, column=1)
frame_serial_monitor.grid(row=2, column=1)
Label(frame_serial_monitor).pack()

# COM Port Input
Label(frame_controls, text="COM Port:").grid(row=1, column=0)
txtport = Entry(frame_controls)
txtport.grid(row=1, column=1)

num_iterations = 300
translated = False
show_prompt = True

# Adding Cylinder Models
blank_cylinder = []
activate_cylinder = []
deactivate_cylinder = []

for i in range(1, 7):
    blank_cylinder.append(ImageTk.PhotoImage(Image.open("cylinder " + str(i) + " blank.jpg")))
    temp = Image.open("cylinder " + str(i) + " activate.jpg")
    temp = temp.resize((blank_cylinder[i - 1].width(), blank_cylinder[i - 1].height()))
    activate_cylinder.append(ImageTk.PhotoImage(temp))
    temp = Image.open("cylinder " + str(i) + " deactivate.jpg")
    temp = temp.resize((blank_cylinder[i - 1].width(), blank_cylinder[i - 1].height()))
    deactivate_cylinder.append(ImageTk.PhotoImage(temp))

global lblcylinder
lblcylinder = []
for i in range(0, 6):
    lblcylinder.append(Label(frame_motor, image=blank_cylinder[i]))
    if i < 3:
        lblcylinder[i].grid(row=i, column=0)
    else:
        lblcylinder[i].grid(row=5 - i, column=1)


def translate_digitalwrite(line):
    if line.startswith("digitalWrite"):
        components = line.split(",")
        pinvalue = components[0][(components[0].index("(") + 1):]
        signal = components[1][:(components[1].index(")"))]
        pinout = pinvalue
        return "Serial.println(\"%\"+String(" + pinout + ")+\",\"+String(" + signal + "));"
    if line.index("digitalRead") > -1:
        replacetext = line[line.index("digitalRead"):len(line)]
        temp = line.replace(replacetext, "atoi(Serial.read());")
        temp = "Serial.println(\"ping\");\nwhile(Serial.available()==0){}\n" + temp
        return temp


def translate_code():
    global raw_code
    global trans_code
    global path
    global translated
    global pathtrans
    trans_code = []
    path = filedialog.askopenfilename(initialdir="D:/", title="Select A File",
                                      filetypes=(("ino files", "*.ino"), ("all files", "*.*")))
    if path == "":
        messagebox.showerror("No Valid Path", "There is no path for code entered!")
    else:
        pathtrans = path[:(path.index(".ino"))] + "_temp.ino"
        # Reading Code from Arduino File
        ocode = open(path, "r")
        raw_code = ocode.readlines()
        raw_code_save = raw_code
        ocode.close()
        # Translating Code
        raw_code_edit = []
        for line in raw_code:
            raw_code_edit.append("// "+line)
            try:
                if line.index("digital") >= 0:
                    trans_code.append(translate_digitalwrite(line.strip()) + "\n")
            except ValueError:
                trans_code.append(line)
        translated = True
        # Writing Translated Code to Arduino File
        rcode = open(path,"w")
        rcode.writelines(raw_code_edit)
        rcode.close()
        ocode = open(pathtrans, "w")
        ocode.writelines(trans_code)
        ocode.close()
        if show_prompt:
            messagebox.showinfo("Translation Complete",
                                "Arduino Code has been translated. Please re-upload code to arduino.")
        webbrowser.open(pathtrans)


motor_state = list()
for i in range(0, 14):
    motor_state.append(False)


def cylinder_state_detection(intake_pin, exhaust_pin):
    if motor_state[intake_pin] and not motor_state[exhaust_pin]:
        return True
    else:
        return False


def cylinder_state(cylinder_num):
    return cylinder_state_detection(cylinder_num * 2, cylinder_num * 2 + 1)


def update_display():
    for i in range(1, 7):
        if cylinder_state(i):
            lblcylinder[i - 1].config(image=activate_cylinder[i - 1])
        else:
            lblcylinder[i - 1].config(image=deactivate_cylinder[i - 1])


def update_pins(pin, signal):
    global motor_state
    if signal == "1":
        motor_state[pin] = True
    else:
        motor_state[pin] = False
    for i in range(2, len(motor_state)):
        if motor_state[i]:
            lblpins[i - 2].config(bg="green")
        else:
            lblpins[i - 2].config(bg="red")
    update_display()


def print_to_serial_monitor(line):
    if line.startswith("%"):
        pindisp = int(line.split(",")[0][1:])
        signaldisp = line.split(",")[1]
        update_pins(pindisp, signaldisp)
    elif line != "ping":
        Label(frame_serial_monitor, text=line).pack()


def start():
    ready = False
    if translated:
        if txtport.get() == "":
            messagebox.showerror("Invalid COM Port", "COM port must be entered")
        else:
            serial_count = 0
            port = "COM" + txtport.get()
            try:
                startcylinder = 1
                ser = serial.Serial(port, 9600)
                for wid in frame_serial_monitor.winfo_children():
                    wid.destroy()
                for i in range(0, num_iterations):
                    data = ser.readline()
                    data = data.decode('utf-8').strip()
                    print_to_serial_monitor(data)
                    root.update()
                    if not cylinder_state(1) and not cylinder_state(2) and not cylinder_state(3) and not cylinder_state(
                            4) and not cylinder_state(5) and not cylinder_state(6) and not ready:
                        ready = True
                    if data == "ping":
                        if cylinder_state(startcylinder):
                            ser.write('1'.encode('utf-8'))
                            ser.flush()
                            startcylinder += 1
                            if startcylinder == 7:
                                startcylinder = 1
                        else:
                            messagebox.showerror("Stall", "The air motor has stalled must run in clockwise direction.")
                            print("stall")
                            break
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
        if os.path.exists(pathtrans):
            os.remove(pathtrans)
        if show_prompt:
            messagebox.showinfo("Code Reverted", "The Arduino Code has been changed back to the original code.")
    else:
        messagebox.showerror("No Code Path", "No code path has been declared")


def clear_code():
    path = ""
    raw_code = ""
    trans_code = ""
    translated = False
    if os.path.exists(pathtrans):
        os.remove(pathtrans)
    for wid in frame_serial_monitor.winfo_children():
        wid.destroy()
    for w in frame_motor.winfo_children():
        w.destroy()


# Need to change to check box
def prompt():
    global show_prompt
    global cmdprompt
    show_prompt = not show_prompt
    cmdprompt.destroy()
    if show_prompt:
        cmdprompt = Button(frame_translate, text="Hide Prompt Message", command=prompt)
    else:
        cmdprompt = Button(frame_translate, text="Show Prompt Message", command=prompt)
    cmdprompt.grid(row=4, column=0)


# Initializing Buttons
cmdtranslatecode = Button(frame_translate, text="Translate Code", command=translate_code)
cmdrevert = Button(frame_translate, text="Revert Code", command=revert_code)
cmdstart = Button(frame_controls, text="Start Motor", command=start)
cmdclear = Button(frame_translate, text="Clear Code Memory", command=clear_code)
cmdprompt = Button(frame_translate, text="Hide Prompt Message", command=prompt)

# Placing Buttons in Grid
cmdtranslatecode.grid(row=1, column=0)
cmdrevert.grid(row=2, column=0)
cmdstart.grid(row=0, column=0, columnspan=2)
cmdclear.grid(row=3, column=0)
cmdprompt.grid(row=4, column=0)

# Creating Pin Indicators
frame_pins = LabelFrame(frame_motor, text="Pin State")
frame_pins.grid(row=6, column=0, columnspan=2)
lblpins = []
for i in range(2, 14):
    lblpins.append(Label(frame_pins, text="Pin " + str(i)))
    if i > 7:
        lblpins[i - 2].grid(row=1, column=i - 8, padx=5, pady=5)
    else:
        lblpins[i - 2].grid(row=0, column=i - 2, padx=5, pady=5)

root.mainloop()
