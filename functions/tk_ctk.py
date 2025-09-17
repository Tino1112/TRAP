import tkinter as tk
import customtkinter as ctk

def screen_dimensions():
    root = tk.Tk()
    root.withdraw()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    return screen_width, screen_height
