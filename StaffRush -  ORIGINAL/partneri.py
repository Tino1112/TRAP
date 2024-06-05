import customtkinter
import psycopg2
import tkinter
from tkinter import messagebox as messagebox
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


def create_partneri_table():
    c, conn = connection()
    c.execute("""
        CREATE TABLE IF NOT EXISTS partneri (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            address VARCHAR(255),
            zip_code VARCHAR(10),
            oib VARCHAR(11),
            iban VARCHAR(34),
            ko_ime VARCHAR(100),
            ko_email VARCHAR(255),
            ko_broj VARCHAR(20)
        )
    """)
    conn.commit()
    conn.close()


def get_current_workplaces():
    c, conn = connection()
    c = conn.cursor()

    c.execute('''SELECT u.id, u.name, u.surname, u.putovnica, w.partner 
                 FROM users u 
                 INNER JOIN work_history w ON u.id = w.user_id 
                 WHERE w.datum_zavrsetka IS NULL''')

    current_workplaces = c.fetchall()
    conn.close()

    return current_workplaces


def create_partneri_window():
    create_partneri_table()
    company_names = []

    p_window = customtkinter.CTk()
    p_window.title("PARTNERI")

    # Get screen dimensions
    screen_width = p_window.winfo_screenwidth()
    screen_height = p_window.winfo_screenheight()

    # Calculate window width and height
    p_window_width = int(screen_width * 0.9)
    p_window_height = int(screen_height * 0.9)

    # Calculate window position to center it on the screen
    x_position = (screen_width - p_window_width) // 2
    y_position = (screen_height - p_window_height) // 2

    # Set window size and position
    p_window.geometry(f"{p_window_width}x{p_window_height}+{x_position}+{y_position}")

    frame_width = int(p_window_width)
    frame_height = int(p_window_height)

    frame2 = customtkinter.CTkScrollableFrame(master=p_window, width=frame_width, height=frame_height, corner_radius=30)
    frame2.pack()

    def add_window():
        a_window = customtkinter.CTk()
        a_window.title("Dodaj novog partnera")

        a_window_width = 450
        a_window_height = 650

        x_pos = (p_window_width - a_window_width) // 2
        y_pos = (p_window_height - a_window_height) // 2

        a_window.geometry(f"{a_window_width}x{a_window_height}+{x_pos}+{y_pos}")

        frame = customtkinter.CTkFrame(master=a_window, width=a_window_width, height=a_window_height, corner_radius=30)
        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        entry_name = customtkinter.CTkEntry(master=frame, width=400, height=40, placeholder_text='NAZIV')
        entry_name.place(x=25, y=30)

        entry_address = customtkinter.CTkEntry(master=frame, width=400, height=40, placeholder_text='ADRESA')
        entry_address.place(x=25, y=100)

        entry_zipcode = customtkinter.CTkEntry(master=frame, width=400, height=40,
                                               placeholder_text='POŠTANSKI BROJ')
        entry_zipcode.place(x=25, y=170)

        entry_oib = customtkinter.CTkEntry(master=frame, width=400, height=40,
                                           placeholder_text='OIB')
        entry_oib.place(x=25, y=240)

        entry_iban = customtkinter.CTkEntry(master=frame, width=400, height=40,
                                            placeholder_text='IBAN')
        entry_iban.place(x=25, y=310)

        entry_ko_ime = customtkinter.CTkEntry(master=frame, width=400, height=40,
                                              placeholder_text='IME KONTAKT OSOBE')
        entry_ko_ime.place(x=25, y=390)

        entry_ko_email = customtkinter.CTkEntry(master=frame, width=400, height=40,
                                                placeholder_text='EMAIL KONTAKT')
        entry_ko_email.place(x=25, y=460)

        entry_ko_broj = customtkinter.CTkEntry(master=frame, width=400, height=40,
                                               placeholder_text='KONTAKT BROJ')
        entry_ko_broj.place(x=25, y=530)

        def save_button_command(name, address, zip_code, oib, iban, ko_ime, ko_email, ko_broj):
            try:
                c, conn = connection()

                c.execute("INSERT INTO partneri (name, address, zip_code, oib, iban, ko_ime, ko_email, ko_broj) "
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                          (name, address, zip_code, oib, iban, ko_ime, ko_email, ko_broj))

                # Commit the transaction
                conn.commit()

                # Close the cursor and connection
                c.close()
                conn.close()

                messagebox.showinfo(title="Data saved", message="Uspješno dodan partner")

                # Destroy the new user window after saving data
                a_window.destroy()
                p_window.destroy()
                create_partneri_window()

            except psycopg2.Error as e:
                messagebox.showerror("Error", "Failed to save user data to the database.")

        save_button = customtkinter.CTkButton(master=frame, width=200, height=40, fg_color="blue", text="DODAJ",
                                              font=("Times", 20), corner_radius=30, command=lambda: save_button_command
                                              (entry_name.get(), entry_address.get(), entry_zipcode.get(),
                                               entry_oib.get(), entry_iban.get(), entry_ko_ime.get(),
                                               entry_ko_email.get(), entry_ko_broj.get()))

        save_button.place(x=125, y=600)

        a_window.mainloop()

    add_button = customtkinter.CTkButton(master=frame2, width=int(p_window_width / 4 * 2), font=('Century Gothic', 30),
                                         height=int(p_window_width / 20),
                                         text="Dodaj novog partnera", corner_radius=30,
                                         fg_color="white", text_color="black", command=add_window)
    add_button.grid(row=0, column=1, columnspan=3, pady=10)

    headers = ["Naziv", "Adresa", "Poštanski broj", "OIB", "IBAN"]

    c = 0
    for h in headers:
        label = customtkinter.CTkLabel(master=frame2, text=h, width=int(p_window_width / 5.8), fg_color="lightblue",
                                       text_color="black", corner_radius=30)
        label.grid(row=1, column=c, padx=10, pady=10)
        c += 1

    c, conn = connection()
    c.execute("SELECT * FROM partneri")
    data = c.fetchall()
    conn.close()

    def workers_window(company_name):
        w_window = customtkinter.CTk()
        upercase_company_name = company_name.upper()
        w_window.title(f"{upercase_company_name} INFORMACIJE")

        w_window_width = 1100
        w_window_height = 700

        x_pos = (p_window_width - w_window_width) // 2
        y_pos = (p_window_height - w_window_height) // 2

        w_window.geometry(f"{w_window_width}x{w_window_height}+{x_pos}+{y_pos}")

        frame3 = customtkinter.CTkScrollableFrame(w_window, width=w_window_width, height=w_window_height,
                                                  corner_radius=30)
        frame3.pack()

        ko_label = customtkinter.CTkLabel(master=frame3, text="KONTAKT OSOBA", text_color="white", font=("Ariel", 20))
        ko_label.grid(row=0, column=0, pady=5, padx=15, sticky="w")

        ko_name_label = customtkinter.CTkLabel(master=frame3, text=f"IME: {d[6]}", fg_color="white", corner_radius=30,
                                               text_color="black", width=int(w_window_width / 4.5))
        ko_name_label.grid(row=1, column=0, pady=5, padx=10)

        ko_email_label = customtkinter.CTkLabel(master=frame3, text=f"EMAIL: {d[7]}", fg_color="white",
                                                corner_radius=30, text_color="black", width=int(w_window_width / 4.5))
        ko_email_label.grid(row=1, column=1, pady=5, padx=10)

        ko_number_label = customtkinter.CTkLabel(master=frame3, text=f"BROJ: {d[8]}", fg_color="white",
                                                 corner_radius=30, text_color="black", width=int(w_window_width / 4.5))
        ko_number_label.grid(row=1, column=2, pady=5, padx=10)

        tz_label = customtkinter.CTkLabel(master=frame3, text="TRENUTNO ZAPOSLENI", text_color="white",
                                          font=("Ariel", 20))
        tz_label.grid(row=2, column=0, pady=15, padx=15, sticky="w")

        headers2 = ["User ID", "Ime", "Prezime", "Broj putovnice"]
        col = 0
        for he in headers2:
            la = customtkinter.CTkLabel(master=frame3, text=he, width=int(w_window_width / 4.5), fg_color="lightblue",
                                        text_color="black", corner_radius=30)
            la.grid(row=3, column=col, padx=10, pady=5)
            col += 1

        # Create a dictionary to store users by their current workplace
        users_by_company = {}

        cw = get_current_workplaces()
        for cws in cw:
            if cws[-1] is None:
                pass
            else:
                comp_name = cws[-1].lower()
                if comp_name == company_name:
                    if comp_name not in users_by_company:
                        users_by_company[comp_name] = []
                    users_by_company[comp_name].append(cws)

        # Sort users by company name
        sorted_users = sorted(users_by_company.items())

        individual_users = []

        for company, users in sorted_users:
            for user in users:
                individual_users.append(user[:-1])

        ro = 4
        for iu in individual_users:
            col = 0
            for i in iu:
                labs = customtkinter.CTkLabel(master=frame3, text=i, width=int(w_window_width / 4.5),
                                              fg_color="white", text_color="black", corner_radius=30)
                labs.grid(row=ro, column=col, padx=5, pady=5)
                col += 1
            ro += 1

        w_window.mainloop()

    # Modify the button creation to pass the button text to the workers_window function
    r = 2
    for d in data:
        co = 0
        for da in d[1:6]:
            if co == 0:
                button = customtkinter.CTkButton(master=frame2, text=da, width=int(p_window_width / 5.8),
                                                 fg_color="white", text_color="black", corner_radius=30,
                                                 hover_color="grey", command=lambda txt=da: workers_window(txt))
                button.grid(row=r, column=co, padx=10, pady=5)
                co += 1
                company_names.append(button.cget("text").lower())
            else:
                labels = customtkinter.CTkLabel(master=frame2, text=da, width=int(p_window_width / 5.8),
                                                fg_color="white", text_color="black", corner_radius=30)
                labels.grid(row=r, column=co, padx=10, pady=5)
                co += 1
        r += 1

    p_window.mainloop()
