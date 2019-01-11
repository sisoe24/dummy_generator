import os
import platform
import subprocess

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

from dummy_generator import DummyGenerator


class DummyGui(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Dummy Generator')
        app_x = 640
        app_y = 290

        # position window in middle of the screen
        position_width = self.winfo_screenwidth() // 2 - (app_x // 2)
        position_height = self.winfo_screenheight() // 2 - (app_y // 2)
        self.geometry(f'{app_x}x{app_y}-{position_width}+{position_height}')
        self.resizable(width=False, height=False)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        main_frame = ttk.Frame(self, borderwidth=5,
                               relief='sunken', width=640, height=290)
        main_frame.grid(column=0, row=0)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_propagate(False)

        line_break_top = ttk.Separator(main_frame, orient=tk.VERTICAL)
        line_break_top.grid(column=0, row=0, rowspan=2,
                            columnspan=2, sticky=(tk.W, tk.E))

        #  --- TOP WIDGETS ----
        upper_frame = ttk.Frame(main_frame, width=630, height=139)

        upper_frame.grid(column=0, row=0)
        upper_frame.grid_propagate(False)

        sx_upper_frame = ttk.Frame(upper_frame, width=200, height=139)
        sx_upper_frame.grid(column=1, row=0, sticky=tk.E)

        button_directory = ttk.Button(sx_upper_frame, text='Select directory',
                                      command=self.get_directory, width=18)
        button_directory.grid(column=0, pady=10, padx=15)

        self.button_confirm = ttk.Button(sx_upper_frame,
                                         text='Confirm and proceed',
                                         command=self.generate_dummy, width=18,
                                         state='disabled')
        self.button_confirm.grid(column=0, row=1, pady=25, sticky=tk.S)

        self.dx_upper_frame = ttk.Frame(upper_frame, width=440, height=140,
                                        borderwidth=2)
        self.dx_upper_frame.grid(column=3, row=0, sticky=tk.E)
        self.dx_upper_frame.grid_propagate(False)

        directory_label = ttk.Label(
            self.dx_upper_frame, text='Selected Directory:')
        directory_label.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)

        self.text_box = tk.Frame(self.dx_upper_frame,
                                 relief='sunken', width=400, height=100,
                                 background='white', borderwidth=2)
        self.text_box.grid(column=1, row=1)
        self.text_box.grid_propagate(False)

        # ---- LOWER WIDGETS ----
        lower_frame = ttk.Frame(main_frame, width=630, height=135)
        lower_frame.grid(column=0, row=1)
        lower_frame.grid_propagate(False)

        # LOWER FRAME LEFT
        sx_lower_frame = ttk.Frame(lower_frame, width=310, height=145)
        sx_lower_frame.grid(column=0, row=0)
        sx_lower_frame.grid_propagate(False)

        line_break_middle = ttk.Separator(main_frame, orient=tk.HORIZONTAL)
        line_break_middle.grid(
            column=0, row=1, columnspan=2, sticky=(tk.N, tk.S))

        option_label = ttk.Label(sx_lower_frame, text='Options',
                                 font=('TkDefaultFont', 20))
        option_label.grid(column=0, row=0, pady=5, sticky=tk.N)

        self.zip_var = tk.BooleanVar()
        zip_checkbox = ttk.Checkbutton(
            sx_lower_frame, text='Zip Dummy folder', variable=self.zip_var)
        zip_checkbox.grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)

        self.invisible_var = tk.BooleanVar()
        invisbile_checkbox = ttk.Checkbutton(
            sx_lower_frame, text='Include invisibile files',
            variable=self.invisible_var)
        invisbile_checkbox.grid(column=0, row=2, padx=5, pady=5, sticky=tk.W)

        # self.p_bar = ttk.Progressbar(sx_lower_frame, orient=tk.HORIZONTAL,
        #                              length=200, mode='indeterminate')
        # self.p_bar.grid(column=0, row=3, padx=10, pady=10)

        # LOWER FRAME RIGHT
        self.dx_lower_frame = ttk.Frame(lower_frame, width=320, height=145)
        self.dx_lower_frame.grid(column=3, row=0)
        self.dx_lower_frame.grid_propagate(False)

        self.file_sample_var = tk.StringVar()
        self.file_sample_checkbox = ttk.Checkbutton(
            self.dx_lower_frame, text='Select sample file',
            onvalue='readonly', offvalue='disabled',
            variable=self.file_sample_var, command=self.enable_combobox)
        self.file_sample_checkbox.grid(
            column=6, row=0, padx=30, pady=10, sticky=tk.W)

        self.file_sample_button = ttk.Button(
            self.dx_lower_frame, width=28,
            command=self.get_sample, text='Select sample file',
            state='disabled')
        self.file_sample_button.grid(
            column=6, row=1, padx=30, pady=5, sticky=tk.E)

        self.file_box = tk.Frame(
            self.dx_lower_frame, background='white', borderwidth=2,
            relief='sunken', width=280, height=50)
        self.file_box.grid(column=6, row=4)
        self.file_box.grid_propagate(False)

    def get_directory(self):
        self.directory = filedialog.askdirectory()
        try:
            if self.selected_dir:
                self.selected_dir.destroy()
        except AttributeError:
            pass
        self.selected_dir = ttk.Label(self.text_box, text=self.directory,
                                      wraplength=400)
        self.selected_dir.grid(column=1, row=2, padx=5, pady=5, sticky=tk.W)
        self.button_confirm['state'] = 'normal'

    def get_sample(self):
        file_path = filedialog.askopenfilename()
        self.filename = os.path.basename(file_path)
        try:
            if self.selected_file:
                self.selected_file.destroy()
        except AttributeError:
            pass
        self.selected_file = ttk.Label(
            self.file_box, text=self.filename, wraplength=400)
        self.selected_file.grid(column=6, row=2)

    def enable_combobox(self):
        self.file_sample_button['state'] = self.file_sample_var.get()

    def generate_dummy(self):
        # self.p_bar.start()
        d = DummyGenerator(main_path=self.directory,
                           sample_file='',
                           invisible_files=self.invisible_var.get())
        if self.zip_var.get():
            d.make_zip_dummy_directory()
        else:
            d.make_dummy_directory()
        self.show_message()
        # self.p_bar.stop()

    def show_message(self):
        msg = messagebox.showinfo(
            title='Loading', message='Done!')
        if platform.system() == 'Darwin':
            subprocess.run(['open', '.'])
        elif platform.system() == 'Linux':
            subprocess.run(['xdg-open', '.'])


if __name__ == '__main__':
    gui = DummyGui()
    gui.mainloop()
