from PIL.ImageChops import add_modulo

from exceptions.exceptions import NewUserError, LoginError
from new_trap.parser import new_user_parser
from new_trap.tables import Users
from sqlalchemy.sql._elements_constructors import and_
import customtkinter as ctk

def open_window(master, window_class, **kwargs):
    """
    Opens a new window of the given class.
    :param master: The main/root window
    :param window_class: a class that inherits from ctk.CTkToplevel
    """
    window_class(master, **kwargs)

def submit_new_user(master, database):
    with database.start_session() as pstg_session:
        children = master.winfo_children()
        data = list(child.get() for child in children if isinstance(child, ctk.CTkEntry) or isinstance(child, ctk.CTkSwitch))

        keys = ['name', 'surname', 'username', 'password', 'admin']

        data_dict = dict(zip(keys, data))

        data_dict = new_user_parser(data_dict)
        username = data_dict.get('username')
        db_records = pstg_session.query(Users).filter(Users.username == username).all()
        if db_records:
            raise NewUserError(f"User {username} already exists.")

        keys_order = ['name', 'surname', 'username', 'password', 'admin']
        stats = database.merge(data_dict, Users, Users.archived.is_(None), pstg_session, keys_order, 'username',stats=True)
        print(stats.inserted)

def login(master, database):
    with database.start_session() as pstg_session:
        window = master.master
        children = master.winfo_children()
        entry_data = [child.get() for child in children if isinstance(child, ctk.CTkEntry)]
        username = entry_data[0]
        password = entry_data[1]

        filters = and_(Users.username==username, Users.password ==password, Users.archived.is_(None))
        db_record = pstg_session.query(Users).filter(filters).first()

        if db_record:
            window.destroy()
            return db_record

        raise LoginError