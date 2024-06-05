# importing required modules
import customtkinter
import tkinter
import psycopg2
import tkinter.messagebox as messagebox
import re
from novi_unos import create_novi_unos_window
from database import create_db_gui
from partneri import create_partneri_window
from PIL import Image
from alarmi import create_alarmi_window, alarm_list
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


def create_main_window():
    create_alarmi_window()

    main_window = customtkinter.CTk()
    main_window.title("Staff Rush")

    # Get screen dimensions
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()

    # Calculate window width and height
    main_window_width = int(screen_width * 0.9)
    main_window_height = int(screen_height * 0.9)

    # Calculate window position to center it on the screen
    x_position = (screen_width - main_window_width) // 2
    y_position = (screen_height - main_window_height) // 2

    # Set window size and position
    main_window.geometry(f"{main_window_width}x{main_window_height}+{x_position}+{y_position}")

    def button_event():
        print("button pressed")

    frame2_width = int(main_window_width * 1)
    frame2_height = int(main_window_height * 1)

    frame2 = customtkinter.CTkFrame(master=main_window, width=frame2_width,
                                    height=frame2_height, corner_radius=30)
    frame2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    l1 = customtkinter.CTkLabel(master=frame2, text="FIVE STAR AGENCY", font=('Century Gothic', 50))
    l1.place(x=int(frame2_width // 2), y=int(main_window_height / 6), anchor="center")

    # button size
    button_width = main_window_width / 4
    button_height = main_window_height / 4

    # Calculate x-coordinate for the buttons
    x_left = button_width  # Distance from the left side of the screen to the left buttons
    x_right = frame2_width - button_width * 1.9  # Distance from the right side of the screen to the right buttons

    # Calculate y-coordinate for the buttons
    y_top = button_height  # Distance from the top side of the screen to the top buttons
    y_bottom = frame2_height - button_height * 1.9  # Distance from the bottom side of the screen to the bottom buttons

    button1 = customtkinter.CTkButton(master=frame2, width=int(button_width), height=int(button_height),
                                      text="NOVI UNOS", font=("Times", 33), command=create_novi_unos_window,
                                      corner_radius=30)
    button1.place(x=x_left, y=y_top)

    button2 = customtkinter.CTkButton(master=frame2, width=int(button_width), height=int(button_height),
                                      text="BAZA PODATAKA", font=("Times", 33), command=create_db_gui,
                                      corner_radius=30)
    button2.place(x=x_left, y=y_bottom)

    button3 = customtkinter.CTkButton(master=frame2, width=int(button_width), height=int(button_height),
                                      text="PARTNERI", font=("Times", 33), command=create_partneri_window,
                                      corner_radius=30)
    button3.place(x=x_right, y=y_top)

    button4 = customtkinter.CTkButton(master=frame2, width=int(button_width), height=int(button_height),
                                      text="OSTALO", font=("Times", 33), command=button_event, corner_radius=30)
    button4.place(x=x_right, y=y_bottom)

    def create_login_table():
        try:
            c, conn = connection()
            cursor = conn.cursor()

            create_table_query = '''
                CREATE TABLE IF NOT EXISTS login (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    surname VARCHAR(100),
                    username VARCHAR(100) UNIQUE,
                    password VARCHAR(100)
                )
            '''
            cursor.execute(create_table_query)

            conn.commit()

            cursor.close()
            conn.close()

        except psycopg2.Error as e:
            print("Error creating users table:", e)
            messagebox.showerror("Error", "Failed to create users table.")

    def save_user_data(name, surname, username, password, new_user_window):
        def contains_special_chars(text):
            # Define a regular expression pattern to match special characters
            pattern = re.compile(r'[^a-zA-Z0-9\s]', flags=re.UNICODE)
            # Check if the text contains any special characters
            return bool(pattern.search(text))

        if not all((name, surname, username, password)):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Check if any of the entries contain special characters
        if contains_special_chars(name) or contains_special_chars(surname) or \
                contains_special_chars(username) or contains_special_chars(password):
            messagebox.showerror("Error", "Entries cannot contain special characters.")
            return

        create_login_table()

        try:
            c, conn = connection()
            cursor = conn.cursor()

            # Execute SQL query to insert new user data into the database
            cursor.execute("INSERT INTO login (name, surname, username, password) VALUES (%s, %s, %s, %s)",
                           (name, surname, username, password))

            # Commit the transaction
            conn.commit()

            # Close the cursor and connection
            cursor.close()
            conn.close()

            messagebox.showinfo(title="Data saved", message="Uspješno dodan user")

            # Destroy the new user window after saving data
            new_user_window.destroy()

        except psycopg2.Error as e:
            print("Error saving user data to PostgreSQL:", e)
            messagebox.showerror("Error", "Failed to save user data to the database.")

    def create_new_user_window(event=None):

        _ = event  # Use '_' to indicate that the 'event' parameter is not used explicitly

        new_user_window = customtkinter.CTkToplevel(main_window)
        new_user_window_width = 450
        new_user_window_height = 600
        x_pos = (main_window_width - new_user_window_width) // 2
        y_pos = (main_window_height - new_user_window_height) // 2
        new_user_window.geometry(f"{new_user_window_width}x{new_user_window_height}+{x_pos}+{y_pos}")
        new_user_window.title("NOVI USER")

        # Set new user window as transient to the main window
        new_user_window.transient(main_window)

        entry_name = customtkinter.CTkEntry(master=new_user_window, width=400, height=40, placeholder_text='IME')
        entry_name.place(x=25, y=100)

        entry_surname = customtkinter.CTkEntry(master=new_user_window, width=400, height=40, placeholder_text='PREZIME')
        entry_surname.place(x=25, y=180)

        entry_username = customtkinter.CTkEntry(master=new_user_window, width=400, height=40,
                                                placeholder_text='USERNAME')
        entry_username.place(x=25, y=260)

        entry_password = customtkinter.CTkEntry(master=new_user_window, width=400, height=40,
                                                placeholder_text='PASSWORD')
        entry_password.place(x=25, y=340)

        def press_enter(event1=None):
            _ = event1  # Use '_' to indicate that the 'event' parameter is not used explicitly

            # Simulate a click event on the dodaj_button
            dodaj_button.invoke()

        dodaj_button = customtkinter.CTkButton(master=new_user_window, width=200, height=40, fg_color="blue",
                                               text="DODAJ", font=("Times", 20),
                                               command=lambda: save_user_data(entry_name.get(), entry_surname.get(),
                                                                              entry_username.get(),
                                                                              entry_password.get(), new_user_window),
                                               corner_radius=30)
        dodaj_button.place(x=25, y=420)

        # Bind the <Return> or <Enter> key event to the press_enter function
        new_user_window.bind('<Return>', press_enter)

        main_window.after(100, entry_name.focus)

    new_user_button = customtkinter.CTkButton(master=frame2, width=int(button_width / 2),
                                              height=int(button_height / 2),
                                              text="NOVI USER", font=("Times", 16), command=create_new_user_window,
                                              corner_radius=30)
    new_user_button.place(x=int(main_window_width / 8), y=int(main_window_height / 10))

    image = customtkinter.CTkImage(Image.open("alarm_image.png"), size=(int(button_width / 4), int(button_height / 2)))
    alarm_color = "transparent"
    if len(alarm_list) != 0:
        alarm_color = "red"

    alarm_button = customtkinter.CTkButton(master=frame2, width=int(button_width / 4),
                                           height=int(button_height / 2), fg_color=alarm_color, text="",
                                           image=image, font=("Times", 16), command=create_alarmi_window,
                                           corner_radius=30)
    alarm_button.place(x=int(main_window_width - button_width / 2.5), y=0)

    main_window.mainloop()
