import tkinter as tk
from tkinter import filedialog


def show_dialog_directory():
    root = tk.Tk()
    root.withdraw()
    dir_path = filedialog.askdirectory()
    root.destroy()
    return dir_path


def show_dialog_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()
    return file_path
