import os
import platform
import subprocess

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

from dummy_generator import DummyGenerator


def calc_size(file):
    """Convert file size."""
    file_size = os.stat(file).st_size
    if file_size > 1_000_000:
        size = f'{file_size // 1_000_000} mb'
    elif file_size > 1000:
        size = f'{file_size // 1000} kbytes'
    elif file_size < 1000:
        size = f'{file_size} bytes'
    return size


def end_message():
    """Show end msg and open directory."""
    dummy_home = f'{os.path.expanduser("~")}/Dummy_Folder'
    messagebox.showinfo(title='Complete', message='Done!')
    if platform.system() == 'Darwin':
        subprocess.run(['open', dummy_home])
    elif platform.system() == 'Linux':
        subprocess.run(['xdg-open', dummy_home])


class MainCore(ttk.Frame):
    directory = ''
    sample_file = ''

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.grid_propagate(False)

        ttk.Button(self, text='Select directory',
                   command=self.get_directory).place(x=300, y=115)

        self.button_confirm = ttk.Button(self, text='Confirm and proceed',
                                         command=self.generate_dummy,
                                         state='disabled')
        self.button_confirm.place(x=450, y=115)

        self.text_box = tk.Text(self, width=60, height=5,
                                font=('TkDefaultFont', 15))
        self.text_box.place(x=15, y=10)

        self.options_label = ttk.LabelFrame(self, text='Optional')
        self.options_label.place(x=10, y=150)

        self.zip_var = tk.BooleanVar()
        zip_checkbox = ttk.Checkbutton(
            self.options_label, text='Zip Dummy folder', variable=self.zip_var)
        zip_checkbox.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)

        self.invisible_var = tk.BooleanVar()
        invisbile_checkbox = ttk.Checkbutton(
            self.options_label, text='Include invisibile files',
            variable=self.invisible_var)
        invisbile_checkbox.grid(column=0, row=1, padx=5, pady=5, sticky=tk.NW)

        # ----- sample file -----
        sample_file_btn = ttk.Button(self.options_label, command=self.set_sample,
                                     text='Select sample file')
        sample_file_btn.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)

        self.status = ttk.Label(self.options_label, text='Status:')
        self.status.place(x=0, y=75)

        self.status_var = tk.StringVar()
        self.status_var.set('waitinig for user input...')
        self.status = ttk.Label(
            self.options_label, textvariable=self.status_var)
        self.status.grid(column=0, row=2, sticky=tk.SW)

        self.treeview = ttk.Treeview(
            self.options_label, columns=('name', 'size'), height=3)
        self.treeview.grid(column=1, row=1, rowspan=2,
                           padx=5, pady=5, sticky=tk.W)
        self.treeview['show'] = 'headings'

        self.treeview.heading('name', text='Name')
        self.treeview.column('name', width=320)

        self.treeview.heading('size', text='Size')
        self.treeview.column('size', width=100)

    def set_directory(self):
        """Set directory from button selection and insert in text box."""
        self.directory = filedialog.askdirectory(
            initialdir='/Users/virgilsisoe/.venvs/PodcastTool/other/linux all files')
        self.text_box.insert(tk.INSERT, self.directory + '\n')
        return self.directory

    def get_directory(self):
        """Get directory path name."""
        self.directory = self.set_directory()
        self.button_confirm['state'] = 'normal'
        return self.directory

    def set_sample(self):
        self.sample_file = filedialog.askopenfilename()
        self.treeview.insert('', 'end', 'tree',)
        self.treeview.set('tree', 'name', os.path.basename(self.sample_file))
        self.treeview.set('tree', 'size', calc_size(self.sample_file))
        return self.sample_file

    @property
    def toggle_zip(self):
        """Compress folder after copy."""
        zip_folder = self.zip_var.get()
        return zip_folder

    @property
    def toggle_invisible(self):
        """Include invisibile files in the copy."""
        toggle_invisibile = self.invisible_var.get()
        return toggle_invisibile

    def generate_dummy(self):
        """Main call for generating dummy folder."""
        self.status_var.set('generating in progress...')
        self.update()
        for dir_path in self.text_box.get('1.0', 'end').splitlines():
            if dir_path:
                DummyGenerator(dir_path,
                               self.sample_file,
                               self.toggle_invisible,
                               self.toggle_zip)
        self.status_var.set('finish')
        end_message()


class MainFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Dummy Generator')
        app_x = 640
        app_y = 300
        position_width = self.winfo_screenwidth() // 2 - (app_x // 2)
        position_height = self.winfo_screenheight() // 2 - (app_y // 2)
        self.geometry(f'{app_x}x{app_y}-{position_width}+{position_height}')
        self.resizable(width=False, height=False)

        MainCore(self, width=640, height=300).grid(column=0, row=0)

        ttk.Separator(self, orient='horizontal').place(x=0, y=145, relwidth=1)
        # ttk.Separator(self, orient='vertical').place(x=185, y=145, relheight=1)


if __name__ == '__main__':
    GUI = MainFrame()
    GUI.mainloop()
