from tkinter import *

root = Tk()
root.title("Data Type Calculator")

DATATYPES = [
    ("Integer (int)", "int"),
    ("Decimal (float)", "float"),
    ("Text (String)", "string")
]

data1 = StringVar()
data2 = StringVar()
data3 = StringVar()
data1.set("int")
data2.set("int")
data3.set("int")

frame_num1 = LabelFrame(root, text="First Value", padx=5, pady=5)
frame_num2 = LabelFrame(root, text="Second Value", padx=5, pady=5)
frame_result = LabelFrame(root, text="Result", padx=5, pady=5)
frame_radio_num1 = LabelFrame(root, text="Value 1 Data Type", padx=5, pady=5)
frame_radio_num2 = LabelFrame(root, text="Value 2 Data Type", padx=5, pady=5)
frame_op = LabelFrame(root, text="Operations", padx=5, pady=5)
frame_radio_result = LabelFrame(root, text="Result Data Type", padx=5, pady=5)

frame_num1.grid(row=0, column=0)
frame_num2.grid(row=0, column=1)
frame_result.grid(row=0, column=2)
frame_radio_num1.grid(row=1, column=0)
frame_radio_num2.grid(row=1, column=1)
frame_op.grid(row=2, column=0, columnspan=3)
frame_radio_result.grid(row=1,column=2)

for text, mode in DATATYPES:
    Radiobutton(frame_radio_num1, text=text, variable=data1, value=mode).pack(anchor=W)
    Radiobutton(frame_radio_num2, text=text, variable=data2, value=mode).pack(anchor=W)
    Radiobutton(frame_radio_result, text=text, variable=data3, value=mode).pack(anchor=W)

txtnum1 = Entry(frame_num1)
txtnum1.pack()
txtnum2 = Entry(frame_num2)
txtnum2.pack()
lblresult = Label(frame_result, text=" ", width=15).grid(row=0, column=0)


def get_input():
    global val1
    global val2
    global error
    Label(frame_result, text="", width=15).grid(row=0, column=0)
    error = False
    try:
        if data1.get() == "int":
            val1 = int(txtnum1.get())
        elif data1.get() == "float":
            val1 = float(txtnum1.get())
        else:
            val1 = txtnum1.get()
        if data2.get() == "int":
            val2 = int(float(txtnum2.get()))
        elif data2.get() == "float":
            val2 = float(txtnum2.get())
        else:
            val2 = txtnum2.get()
    except ValueError:
        error = True


def add():
    get_input()
    if not error:
        if data3.get() == "int":
            result = str(int(val1 + val2))
        elif data3.get() == "float":
            result = str(float(val1 + val2))
        else:
            result = str(val1 + val2)
        Label(frame_result, text=result).grid(row=0, column=0)
    else:
        Label(frame_result, text="Error: Data Types are not compatible").grid(row=0,column=0)


def subtract():
    get_input()
    if not error:
        if data3.get() == "int":
            result = str(int(val1 - val2))
        elif data3.get() == "float":
            result = str(float(val1 - val2))
        else:
            result = str(val1 - val2)
        Label(frame_result, text=result).grid(row=0, column=0)
    else:
        Label(frame_result, text="Error: Data Types are not compatible").grid(row=0, column=0)


def multiply():
    get_input()
    if data1.get() == "string" or data2.get() == "string" or error:
        Label(frame_result, text="Error: Data Types are not compatible").grid(row=0, column=0)
    else:
        if data3.get() == "int":
            result = str(int(val1 * val2))
        elif data3.get() == "float":
            result = str(float(val1 * val2))
        else:
            result = str(val1 * val2)
        Label(frame_result, text=result).grid(row=0, column=0)


def divide():
    get_input()
    if data1.get() == "string" or data2.get() == "string" or error:
        Label(frame_result, text="Error: Data Types are not compatible").grid(row=0, column=0)
    else:
        try:
            if data3.get() == "int":
                result = str(int(val1 / val2))
            elif data3.get() == "float":
                result = str(float(val1 / val2))
            else:
                result = str(val1 / val2)
            Label(frame_result, text=result).grid(row=0, column=0)
        except ZeroDivisionError:
            Label(frame_result, text="Error: Divide by Zero").grid(row=0, column=0)


cmdadd = Button(frame_op, text="+", command=add, width = 5, height=2).grid(row=0,column=0)
cmdsubtract = Button(frame_op, text="-", command=subtract, width = 5, height=2).grid(row=0,column=1)
cmdmultiply = Button(frame_op, text="*", command=multiply, width = 5, height=2).grid(row=0,column=2)
cmddivide = Button(frame_op, text="/", command=divide, width = 5, height=2).grid(row=0,column=3)

root.mainloop()
