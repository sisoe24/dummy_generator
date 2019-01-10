import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import time

mp3 = ['virgil.mp3', 'lara.mp3']

root = tk.Tk()
root.geometry('640x290-500+500')

frame = ttk.Frame(root)
frame.pack()


def get_dir():
    dirs = filedialog.askopenfile()


def value():
    print('button state: ', check_var.get())
    button['state'] = check_var.get()


def get():
    print('combobox get: ', button.cget())


def increment_start():
    p.start(100)


def increment_stop():
    p.stop()


def message():
    m = messagebox.showinfo(title='Calculating', message='ciao')
    p = ttk.Progressbar(parent=m, orient=tk.HORIZONTAL,
                        length=200, mode='determinate')
    p.pack()


def progress():
    p.start()
    for i in range(50):
        print(i)
        root.update()
        time.sleep(0.1)
    p.stop()


def new_window():
    new_wi = tk.Toplevel(root, width=20, height=20)
    new_wi.geometry('230x90-700+700')


def run():
    for i in range(50):
        print(i)
        time.sleep(0.1)


check_var = tk.StringVar()
checkbox = ttk.Checkbutton(
    frame, text='Activate combobox', variable=check_var,
    onvalue='readonly', offvalue='disabled', command=value)
checkbox.pack()
print('check_var: ', check_var.get())

button = ttk.Button(frame, text='sample file',
                    state='disabled', command=get_dir)
button.pack()

get_combo = ttk.Button(frame, text='see selection', command=get)
get_combo.pack()

p = ttk.Progressbar(frame, orient=tk.HORIZONTAL,
                    length=200, mode='indeterminate')
p.pack()

start = ttk.Button(frame, text='start progress', command=increment_start)
start.pack()
stop = ttk.Button(frame, text='stop progress', command=increment_stop)
stop.pack()
show_message = ttk.Button(frame, text='show msg', command=message)
show_message.pack()
call_window = ttk.Button(frame, text='create new window', command=new_window)
call_window.pack()

new_wi = tk.Toplevel(root, width=20, height=20)
new_wi.geometry('640x290-500+500')


root.mainloop()
