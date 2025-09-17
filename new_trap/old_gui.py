import os
import logging
import tkinter as tk
from PIL import Image, ImageTk
from database.database import Database

from new_trap.buttons_functions import open_window, submit_new_user
from functions.tk_ctk import screen_dimensions, center_window, create_frame
from functions.tcl import fix_tcL_error

fix_tcL_error()
import customtkinter as ctk

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (default), "green", "dark-blue"

screen_width, screen_height = screen_dimensions()

# Main window
class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.database = Database('pstg', logger)

        self.title('Database management system')

        self.width = int(screen_width * 0.85)
        self.height = int(screen_height * 0.85)

        center_window(self, screen_width, screen_height, self.width, self.height)

        # main window frame
        self.main_frame = create_frame(self)

        # configure rows and columns
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=2)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.add_widgets()

    def add_widgets(self):
        bg_image = Image.open("ekko.jpg")
        bg_photo = ctk.CTkImage(dark_image=bg_image, size=(self.width, self.height))

        bg_label = ctk.CTkLabel(self.main_frame, image=bg_photo, text="")
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        button_width = self.width // 4
        button_height = self.height // 5

        buttons_args = [{'text': 'New user', 'x_pos': 0, 'y_pos': 0, 'command': lambda: open_window(self, NewUserWindow,
                                                                                                    database=self.database)},
                        {'text': 'Workers', 'x_pos': 1, 'y_pos': 0, 'command': self.button_func},
                        {'text': 'Partners', 'x_pos': 0, 'y_pos': 2, 'command': self.button_func},
                        {'text': 'Else', 'x_pos': 1, 'y_pos': 2, 'command': self.button_func}]
        for button in buttons_args:
            btn = ctk.CTkButton(self.main_frame, width=button_width, height=button_height, corner_radius=30,
                                   font=("Times", 40), text=button['text'], command=button['command'])
            btn.grid(column=button['x_pos'], row=button['y_pos'])

        label = ctk.CTkLabel(master=self.main_frame, text='Company database management',font=('Century Gothic', 50),
                                  width=self.width // 2)
        label.grid(column=0, row=1, columnspan=2)

    def button_func(self):
        pass

class NewUserWindow(ctk.CTkToplevel):
    def __init__(self, master=None, database=None):
        super().__init__(master)

        self.database = database

        self.title('New user')

        self.width = screen_width // 3
        self.height = screen_height // 2

        center_window(self, screen_width, screen_height, self.width, self.height)

        self.frame = create_frame(self)

        # place it over main window
        self.attributes("-topmost", True)

        self.frame.grid_columnconfigure(0, weight=1)
        for row in range(6):
            self.frame.grid_rowconfigure(row, weight=1)

        self.add_widgets()

    def add_widgets(self):
        entry_fields = ['Name', 'Surname', 'Username', 'Password']
        widget_width = int(self.width * 0.8)
        widget_height = int(self.height * 0.14)
        for i in range(6):
            widget = None
            if i < 4:
                widget = ctk.CTkEntry(self.frame, width=widget_width, height=widget_height,
                                  placeholder_text=entry_fields[i], corner_radius=40)

            if i == 4:
                switch_var = ctk.BooleanVar(value=False)
                widget = ctk.CTkSwitch(self.frame, text='Admin rights off/on', variable=switch_var,
                                       width=widget_width, font=("Times", 20), switch_width=50, switch_height=20)

            if i == 5:1
                widget = ctk.CTkButton(self.frame, text='Create user', width=int(widget_width * 0.8), height=widget_height,
                                       font=("Times", 20), corner_radius=30, command=lambda: submit_new_user(self.frame, self.database))

            widget.grid(row=i, padx=10, pady=10)

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
