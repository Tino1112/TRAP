import logging
from functions.log import Log
from database.database import Database
from functions.tcl import fix_tcL_error
from gui import LoginWindow, MainWindow
from database.database import Database

fix_tcL_error()
import customtkinter as ctk

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
 
class App:
    def __init__(self):
        self.database = Database('pstg', logger)
        self.username = None
        self.workflow()

    def workflow(self):
        # lw = LoginWindow(self.database)
        # lw.mainloop()
        # self.username = lw.username
        # print(self.username)
        mw = MainWindow(self.database)
        mw.mainloop()

if __name__ == '__main__':
    app = App()
