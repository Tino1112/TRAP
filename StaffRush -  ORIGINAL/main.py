from login import create_login_window
import tkinter.messagebox as messagebox
import json
import os
from tkinter import simpledialog
import tkinter as tk


CONFIG_FILE = 'db_config.json'


def check_for_json():
    if not os.path.isfile(CONFIG_FILE):
        setup_db_config_gui()

    create_login_window()


def setup_db_config_gui():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    config = {
        "host": simpledialog.askstring("Database Host", "Enter the database host: "),
        "database": simpledialog.askstring("Database Name", "Enter the database name: "),
        "user": simpledialog.askstring("Database User", "Enter the database user: "),
        "password": simpledialog.askstring("Database Password", "Enter the database password: ", show='*')
    }

    if all(config.values()):
        with open(CONFIG_FILE, 'w') as config_file:
            json.dump(config, config_file)
        messagebox.showinfo("Success", "Database configuration saved successfully.")
    else:
        messagebox.showerror("Error", "All fields are required.")
        setup_db_config_gui()  # Retry configuration if failed


check_for_json()
