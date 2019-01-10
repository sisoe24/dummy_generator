from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from dummy_generator import DummyGenerator


root = Tk()
root.title('Dummy Generator')
root.geometry('640x290-500+500')
root.resizable(width=False, height=False)

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

main_frame = ttk.Frame(root, borderwidth=5,
                       relief='sunken', width=640, height=290)
main_frame.grid(column=0, row=0)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_propagate(False)

divisor_top = ttk.Separator(main_frame, orient=VERTICAL)
divisor_top.grid(column=0, row=0, rowspan=2, columnspan=2, sticky=(W, E))

# TOP WIDGETS ----
upper_frame = ttk.Frame(main_frame, width=630, height=139)

upper_frame.grid(column=0, row=0)
upper_frame.grid_propagate(False)

sx_upper_frame = ttk.Frame(upper_frame, width=200, height=139)
sx_upper_frame.grid(column=1, row=0, sticky=E)

class RunMain(object):
    def __init__(self):
        pass

    def get_directory(self):
        self.directory = filedialog.askdirectory()
        lista = ttk.Label(dx_upper_frame, text=self.directory,
                          relief='sunken', wraplength=400)
        lista.grid(column=1, row=2, padx=5, pady=20, sticky=W)

    def run(self):
        dummy = DummyGenerator(main_path=self.directory,
                               sample_file='',
                               invisible_files=INVISIBLE_VAR.get())
        if ZIP_VAR.get():
            dummy.make_zip_dummy_directory()
        else:
            dummy.make_dummy_directory()


def get_directory():
    global directory
    directory = filedialog.askdirectory()
    d = StringVar()
    d.set(directory)
    lista = ttk.Label(dx_upper_frame, text=directory,
                      relief='sunken', wraplength=400)
    lista.grid(column=1, row=2, padx=5, pady=20, sticky=W)


def enable_combobox():
    # if SAMPLE_VAR.get() == '0':
    #     a = 'disabled'
    # elif SAMPLE_VAR.get() == '1':
    #     a = 'readonly'
    sample_combobox = ttk.Combobox(
        lower_frame_dx, values=mp3_files, state=activate(), width=28)
    sample_combobox.grid(column=6, row=1, padx=30, pady=5, sticky=E)


def activate():
    activate_selection = 'readonly'
    if SAMPLE_VAR.get() != '1':
        activate_selection = 'disable'
    else:
        activate_selection = 'readonly'
    return activate_selection


def run_main():
    dummy = DummyGenerator(main_path=directory,
                           sample_file='',
                           invisible_files=INVISIBLE_VAR.get())
    if ZIP_VAR.get():
        dummy.make_zip_dummy_directory()
    else:
        dummy.make_dummy_directory()

a = RunMain()
ask_directory = ttk.Button(sx_upper_frame, text='Select directory',
                           command=a.get_directory, width=18)
ask_directory.grid(column=0, pady=10, padx=15)

confirm = ttk.Button(sx_upper_frame, text='Confirm and proceed',
                     command=a.run, width=18,)
confirm.grid(column=0, row=1, pady=25, sticky=S)

dx_upper_frame = ttk.Frame(upper_frame, width=440, height=140,
                           borderwidth=2)
dx_upper_frame.grid(column=3, row=0, sticky=E)
dx_upper_frame.grid_propagate(False)

file_label = ttk.Label(dx_upper_frame, text='Selected Directory:')
file_label.grid(column=1, row=0, padx=5, pady=5, sticky=W)


# ---- LOWER WIDGETS ----
lower_frame = ttk.Frame(main_frame, width=630, height=135)
lower_frame.grid(column=0, row=1)
lower_frame.grid_propagate(False)

# LOWER FRAME LEFT
lower_frame_sx = ttk.Frame(lower_frame, width=310, height=145)
lower_frame_sx.grid(column=0, row=0)
lower_frame_sx.grid_propagate(False)

divisor_middle = ttk.Separator(main_frame, orient=HORIZONTAL)
divisor_middle.grid(column=0, row=1, columnspan=2, sticky=(N, S))

option_label = ttk.Label(lower_frame_sx, text='Options',
                         font=('TkDefaultFont', 20))
option_label.grid(column=3, row=0, pady=5, sticky=N)

ZIP_VAR = BooleanVar()
zip_checkbox = ttk.Checkbutton(
    lower_frame_sx, text='Zip Dummy folder', variable=ZIP_VAR)
zip_checkbox.grid(column=3, row=1, padx=5, pady=5, sticky=W)

INVISIBLE_VAR = BooleanVar()
invisbile_checkbox = ttk.Checkbutton(
    lower_frame_sx, text='Include invisibile files', variable=INVISIBLE_VAR)
invisbile_checkbox.grid(column=3, row=2, padx=5, pady=5, sticky=W)

delete_var = StringVar()
delete_checkbox = ttk.Checkbutton(
    lower_frame_sx, text='Delete copy after', variable=delete_var)
delete_checkbox.grid(column=3, row=3, padx=5, pady=5, sticky=W)


# LOWER FRAME RIGHT
lower_frame_dx = ttk.Frame(lower_frame, width=320, height=145)
lower_frame_dx.grid(column=3, row=0)
lower_frame_dx.grid_propagate(False)

SAMPLE_VAR = StringVar()
sample_checkbox = ttk.Checkbutton(
    lower_frame_dx, text='Select sample file', variable=SAMPLE_VAR,
    command=enable_combobox)
sample_checkbox.grid(column=6, row=0, padx=30, pady=10, sticky=W)


mp3_files = ['madonna - jesus.mp3', 'stefano cardinale - ho visto.mp3']
sample_combobox = ttk.Combobox(
    lower_frame_dx, values=mp3_files, state='disabled', width=28)
sample_combobox.grid(column=6, row=1, padx=30, pady=5, sticky=E)
# ---

if __name__ == '__main__':
    root.mainloop()
