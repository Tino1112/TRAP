import tkinter

from PIL import Image
from tkinter.messagebox import showerror
from exceptions.exceptions import LoginError
from functions.tk_ctk import screen_dimensions
from functions.alcheamy import db_records_to_dicts
from functions.tcl import fix_tcL_error
from buttons_functions import login, open_window, submit_new_user
from sqlalchemy.sql._elements_constructors import and_
from new_trap.tables import Workers, WorkerDetails, WorkHistory, WorkersDocuments, WorkersBasicInfo
from sqlalchemy import select
from parser import workers_parser

fix_tcL_error()

import customtkinter as ctk

screen_width, screen_height = screen_dimensions()

class BaseWindow:
    def __init__(self, container, title: str, width: float, height: float, n_rows: int, n_cols: int,
                 widgets_expandable: bool, scrollable=False, create_frame=True):
        """
        Base creator for CTk windows, super class to Window and TopLevelWindow classes

        params:
            :param container: master
            :param title: ctk title
            :param width: percentage shown as a float of how much of a screen width should a window take
            :param height: percentage shown as a float of how much of a screen height should a window take
            :param n_rows: number of rows on that window
            :param n_cols: number of columns on that window
            :param widgets_expandable: are widgets expandable?
        """
        # container basic settings
        self.container = container
        self.container.title(title)
        self.width = int(screen_width * width)
        self.height = int(screen_height * height)
        self.x_pos = (screen_width - self.width) // 2
        self.y_pos = (screen_height - self.height) // 2
        # center the window
        geo_string = f'{self.width}x{self.height}+{self.x_pos}+{self.y_pos}'
        self.container.geometry(geo_string)

        # widget settings
        self.corner_radius = 40
        self.padx, self.pady = 10, 10

        self.frame = None
        if create_frame:
            if scrollable:
                self.frame = ctk.CTkScrollableFrame(self.container, corner_radius=self.corner_radius)
            else:
                self.frame = ctk.CTkFrame(self.container, corner_radius=self.corner_radius)
            self.frame.pack(fill="both", expand=True)

            weight = 1 if widgets_expandable else 0
            self.grid_config(n_rows, n_cols, weight)

            self.add_widgets()

    # determine how much rows and cols does a frame have
    def grid_config(self, n_rows, n_cols, weight):
        for i in range(n_rows):
            self.frame.grid_rowconfigure(i, weight=weight)
        for i in range(n_cols):
            self.frame.grid_columnconfigure(i, weight=weight)

    def add_widgets(self):
        # placeholder, overwrite it when creating subclass
        pass

    def grid_widget(self, widget_class, row: int, col: int, columnspan=1, master=None, padx=None, pady=None,
                    corner_radius=None, sticky=False, **kwargs):
        if not issubclass(widget_class, ctk.CTkBaseClass):
            raise TypeError('widget_class must be a CTk Widget class')

        corner_radius = corner_radius or self.corner_radius
        padx = padx or self.padx
        pady = pady or self.pady
        sticky = 'nsew' if sticky else None
        master = master or self.frame

        widget = widget_class(master, corner_radius=corner_radius, **kwargs)
        widget.grid(row=row, column=col, sticky=sticky, padx=padx, pady=pady, columnspan=columnspan)

        return widget

class Window(ctk.CTk, BaseWindow):
    def __init__(self, title, width, height, n_rows, n_cols, widgets_expandable, scrollable=False, create_frame=True):
        ctk.CTk.__init__(self)
        BaseWindow.__init__(self, self, title, width, height, n_rows, n_cols, widgets_expandable, scrollable, create_frame)

class TopLevelWindow(ctk.CTkToplevel, BaseWindow):
    def __init__(self, title, width, height, n_rows, n_cols, widgets_expandable, scrollable=False, create_frame=True):
        ctk.CTkToplevel.__init__(self)
        BaseWindow.__init__(self, self, title, width, height, n_rows, n_cols, widgets_expandable, scrollable, create_frame)

        self.attributes('-topmost', True)

class LoginWindow(Window):
    def __init__(self, database):
        Window.__init__(self, 'Login', 0.4, 0.6, 4, 1, True)

        self.database = database
        self.bind('<Return>', lambda event: self.button_func())

        self.success = False
        self.username = None

    def add_widgets(self):
        width = self.width * 0.9
        height = self.height * 0.15
        font = ("Yu Gothic UI Semibold", 40)
        widgets = [{'class': ctk.CTkLabel, 'row': 0, 'col': 0, 'kwargs':{'width': width, 'height': height, 'text': 'Login to your account', 'font': font}},
                   {'class': ctk.CTkEntry, 'row': 1, 'col': 0, 'kwargs':{'width': width, 'height': height, 'placeholder_text': 'Username'}},
                   {'class': ctk.CTkEntry, 'row': 2, 'col': 0, 'kwargs':{'width': width, 'height': height, 'placeholder_text': 'Password'}},
                   {'class': ctk.CTkButton, 'row': 3, 'col': 0, 'kwargs':{'width': width, 'height': height, 'text': 'Login',
                                                                          'font': font, 'command': self.button_func}},]

        for widget in widgets:
            self.grid_widget(widget['class'], row=widget['row'], col=widget['col'], **widget['kwargs'])

    def button_func(self):
        try:
            db_record = login(self.frame, self.database)
            self.success = True
            self.username = db_record.username
            self.destroy()
        except LoginError as e:
            tkinter.messagebox.showerror('Login Error', str(e))

class MainWindow(Window):
    def __init__(self, database):
        Window.__init__(self, 'Database management system', 0.85, 0.85, 3, 2, True)

        self.database = database

    def add_widgets(self):
        button_width = self.width // 3
        button_height = self.height // 5
        font = ("Yu Gothic UI Semibold", 40)
        bg_image = Image.open(r'C:\Users\User\Documents\GitHub\my_projects\photos\db_bg.jpg')
        bg_photo = ctk.CTkImage(dark_image=bg_image, size=(self.width, self.height))
        bg = ctk.CTkLabel(self.frame, image=bg_photo, text="")
        bg.place(relx=0, rely=0, relwidth=1, relheight=1)

        widgets = [{'class': ctk.CTkButton, 'row': 0, 'col': 0, 'kwargs':
            {'width': button_width, 'height': button_height, 'command': lambda: open_window(NewUserWindow, database=self.database), 'text': 'New User', 'font': font}},
                   {'class': ctk.CTkButton, 'row': 0, 'col': 1, 'kwargs':
            {'width': button_width, 'height': button_height, 'command': lambda: open_window(WorkersWindow, database=self.database), 'text': 'Workers', 'font': font}},
                   {'class': ctk.CTkButton, 'row': 2, 'col': 0, 'kwargs':
            {'width': button_width, 'height': button_height, 'command': self.button_func, 'text': 'Partners', 'font': font}},
                   {'class': ctk.CTkButton, 'row': 2, 'col': 1, 'kwargs':
            {'width': button_width, 'height': button_height, 'command': self.button_func, 'text': 'Documents', 'font': font}},
                   {'class': ctk.CTkLabel, 'row': 1, 'col': 0, 'kwargs':
            {'width': button_width, 'height': button_height, 'text': 'Database Management System', 'columnspan': 2, 'font': font}}]

        for widget in widgets:
            self.grid_widget(widget['class'], row=widget['row'], col=widget['col'], padx=0, **widget['kwargs'])

    def button_func(self):
        pass

class NewUserWindow(TopLevelWindow):
    def __init__(self, database):
        TopLevelWindow.__init__(self, 'Create New User', 0.4, 0.6, 6, 1, True)

        self.database = database

    def add_widgets(self):
        width = self.width * 0.8
        height = self.height * 0.13
        font = ("Yu Gothic UI Semibold", 40)
        widgets = [{'class': ctk.CTkEntry, 'row': 0, 'col': 0, 'kwargs':{'width': width, 'height': height, 'placeholder_text': 'Name'}},
                   {'class': ctk.CTkEntry, 'row': 1, 'col': 0, 'kwargs':{'width': width, 'height': height, 'placeholder_text': 'Surname'}},
                   {'class': ctk.CTkEntry, 'row': 2, 'col': 0, 'kwargs':{'width': width, 'height': height, 'placeholder_text': 'Username'}},
                   {'class': ctk.CTkEntry, 'row': 3, 'col': 0, 'kwargs':{'width': width, 'height': height, 'placeholder_text': 'Password'}},
                   {'class': ctk.CTkSwitch, 'row': 4, 'col': 0, 'kwargs':{'width': width, 'text': 'Admin rights off/on', 'switch_width': 50,
                                                                          'switch_height': 20, 'variable': ctk.BooleanVar(value=False)}},
                   {'class': ctk.CTkButton, 'row': 5, 'col': 0, 'kwargs':{'width': width, 'height': height, 'text': 'Submit', 'font': font,
                                                                          'command': self.button_func}},]

        for widget in widgets:
            self.grid_widget(widget['class'], row=widget['row'], col=widget['col'], **widget['kwargs'])

    def button_func(self):
        try:
            submit_new_user(self.frame, self.database)
            tkinter.messagebox.showinfo('success', 'New was successfully submited')
        except Exception as e:
            tkinter.messagebox.showerror('Error', str(e))

class WorkersWindow(TopLevelWindow):
    def __init__(self, database):

        self.database = database
        with self.database.start_session() as pstg_session:
            db_records = pstg_session.scalars(select(Workers).filter(Workers.archived.is_(None))).all()

        if db_records:
            db_data = [workers_parser(data_dict) for data_dict in db_records_to_dicts(db_records)]
            columns = list(db_data[0].keys())[2:][:-1]
            records_data = [list(data.values())[1:][:-1] for data in db_data]

        else:
            columns = [c.name for c in Workers.__table__.columns]
            records_data = list()

        self.table_data = [columns] + records_data

        self.n_rows = len(records_data) + 1  # add headers to grid
        self.n_cols = len(columns)
        TopLevelWindow.__init__(self, 'Workers', 0.8, 0.8, self.n_rows, self.n_cols, True, scrollable=True)

    def add_widgets(self):
        btn_width = int(screen_width / self.n_cols)
        btn_height = 40
        for row, data in enumerate(self.table_data):
            user_id = None
            if row != 0:
                user_id = data[0]
                data = data[1:]
            for col, value in enumerate(data):
                kwargs = {'text': value, 'text_color': 'black', 'fg_color': 'white', 'border_width': 1, 'border_color': 'grey',
                          'hover_color': 'light blue', 'width': btn_width, 'height': btn_height}
                widget = self.grid_widget(ctk.CTkButton, row, col, **kwargs)
                if row != 0:
                    widget.user_id = user_id
                widget.configure(command=lambda b=widget: self.btn_func(b))
                if row == 0:
                    widget.configure(state='disabled', fg_color='light blue', text_color_disabled='black')

    def btn_func(self, widget):
        user_id = widget.user_id
        open_window(DetailsWindow, database= self.database, user_id=user_id)

class DetailsWindow(TopLevelWindow):
    def __init__(self, database, user_id):
        self.database = database
        self.user_id = user_id
        TopLevelWindow.__init__(self, 'Worker Details', 0.5, 0.6, 6, 1, True, create_frame=False)

        self.frame = ctk.CTkTabview(self)
        self.frame.pack(fill="both", expand=True)
        # tabs
        self.basic_info = self.frame.add('Basic Info')
        self.details = self.frame.add('Details')
        self.work_history = self.frame.add('Work History')
        self.documents = self.frame.add('Documents')
        # tabs frames
        self.bi_frame = ctk.CTkScrollableFrame(self.basic_info)
        self.d_frame = ctk.CTkScrollableFrame(self.details)
        self.wh_frame = ctk.CTkScrollableFrame(self.work_history)
        self.doc_frame = ctk.CTkScrollableFrame(self.documents)
        tabs_frames = [self.bi_frame, self.d_frame, self.wh_frame, self.doc_frame]
        for t_frame in tabs_frames:
            t_frame.pack(fill="both", expand=True)
        self.add_widgets()

        self.lift()
        self.focus_force()
        self.grab_set()

    def add_widgets(self):
        with self.database.start_session() as pstg_session:
            table_objs = {WorkersBasicInfo: self.bi_frame,
                          WorkerDetails: self.d_frame,
                          WorkHistory: self.wh_frame,
                          WorkersDocuments: self.doc_frame}
            for table_obj, tab in table_objs.items():
                filters = and_(table_obj.archived.is_(None), table_obj.user_id == self.user_id)
                db_record = pstg_session.execute(select(table_obj).filter(filters)).all()

                data_dict = db_records_to_dicts(db_record)
                data_dict = data_dict[0] if data_dict else data_dict
                keys = list(data_dict.keys())[2:-2] if data_dict else [c.name for c in table_obj.__table__.columns][2:-2]
                values = list(data_dict.values())[2:-2] if data_dict else ['None' for _ in keys]
                new_data_dict = dict(zip(keys, values))

                for i in range(2):
                    tab.grid_columnconfigure(i, weight=1)
                for i in range(len(keys)):
                    tab.grid_rowconfigure(i, weight=1)

                widget_kwargs = {'text_color': 'black', 'width': int(screen_width * 0.2)}
                for i, (header, value) in enumerate(new_data_dict.items()):
                    self.grid_widget(ctk.CTkLabel, i, 0, master=tab, text=header, fg_color='light blue', **widget_kwargs)
                    self.grid_widget(ctk.CTkButton, i, 1, master=tab, text=value, fg_color='white', **widget_kwargs)