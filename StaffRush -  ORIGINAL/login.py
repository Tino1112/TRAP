import psycopg2
import customtkinter
import tkinter as tk
from tkinter import messagebox
from main_window import create_main_window
import json


def connection():
    CONFIG_FILE = 'db_config.json'
    with open(CONFIG_FILE, 'r') as config_file:
        config = json.load(config_file)

    conn = psycopg2.connect(
        host=config['host'],
        database=config['database'],
        user=config['user'],
        password=config['password']
    )
    c = conn.cursor()
    return c, conn


def create_login_window():
    connection()
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    app = customtkinter.CTk()
    app.geometry("800x600")
    app.title('Login')

    # Get screen dimensions
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    # Calculate window width and height
    window_width = int(screen_width * 0.8)
    window_height = int(screen_height * 0.8)

    # Calculate window position to center it on the screen
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    # Set window size and position
    app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    def login(event=None):
        _ = event  # Use '_' to indicate that the 'event' parameter is not used explicitly

        entered_username = entry1.get()
        entered_password = entry2.get()

        # Admin login
        if entered_username == "ADMIN" and entered_password == "ADMIN":
            app.destroy()
            create_main_window()
            return

        # Connect to PostgreSQL database
        try:
            c, conn = connection()
            cursor = c

            # Retrieve user login information from the database
            cursor.execute("SELECT * FROM login WHERE username = %s AND password = %s",
                           (entered_username, entered_password))
            user_data = cursor.fetchone()

            conn.close()

            # If user_data is not None, the login is successful
            if user_data:
                app.destroy()
                create_main_window()
                return
            else:
                messagebox.showerror("Error", "Invalid username or password. Please try again.")

        except psycopg2.Error as e:
            print("Error connecting to PostgreSQL:", e)
            messagebox.showerror("Error", "Failed to connect to the database.")

    frame = customtkinter.CTkFrame(master=app, width=500, height=400, corner_radius=30)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    l1 = customtkinter.CTkLabel(master=frame, text="Log into your account", font=('Century Gothic', 40))
    l1.place(x=45, y=45)

    entry1 = customtkinter.CTkEntry(master=frame, width=400, height=40, placeholder_text='Username')
    entry1.place(x=45, y=130)

    entry2 = customtkinter.CTkEntry(master=frame, width=400, height=40, placeholder_text='Password', show="*")
    entry2.place(x=45, y=215)

    button1 = customtkinter.CTkButton(master=frame, width=200, height=50, text="Login", command=login, corner_radius=6)
    button1.place(x=150, y=300)

    app.bind('<Return>', login)

    # Set focus to the username entry widget after a short delay
    app.after(100, entry1.focus)

    app.mainloop()
