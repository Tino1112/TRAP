import psycopg2
import customtkinter
from CTkTable import *
import tkinter.messagebox as messagebox
from psycopg2 import errors, Error
from datetime import date
import tkinter as tk
from tkinter import filedialog
import os
import subprocess
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


def create_database():
    c, conn = connection()
    # Create the users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT,
                surname TEXT,
                oib TEXT,
                putovnica TEXT,
                id_broj TEXT,
                dat_rodenja DATE,
                mjesto_rodenja TEXT,
                prebivaliste TEXT,
                boraviste TEXT,
                kontakt TEXT
                )''')

    # Commit changes and close connection
    conn.commit()
    conn.close()


def add_user(name, surname, oib, putovnica, id_broj, dat_rodenja, mjesto_rodenja, prebivaliste, boraviste, kontakt):
    try:
        c, conn = connection()
        c.execute('''INSERT INTO users (name, surname, oib, putovnica, id_broj, dat_rodenja, mjesto_rodenja, 
                        prebivaliste, boraviste, kontakt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                  (name, surname, oib, putovnica, id_broj, dat_rodenja, mjesto_rodenja, prebivaliste, boraviste,
                   kontakt))

        conn.commit()
        conn.close()
    except (psycopg2.Error, psycopg2.DatabaseError) as e:
        messagebox.showerror("Database Error", f"Error adding user: {e}")


def update_user(name, surname, oib, putovnica, id_broj, dat_rodenja, mjesto_rodenja, prebivaliste, boraviste,
                kontakt, row):
    c, conn = connection()
    c.execute('''UPDATE users SET name = %s, surname = %s, oib = %s, putovnica = %s, id_broj = %s,
                 dat_rodenja = %s, mjesto_rodenja = %s, prebivaliste = %s, boraviste = %s, kontakt = %s
                 WHERE id = %s''',
              (name, surname, oib, putovnica, id_broj, dat_rodenja, mjesto_rodenja, prebivaliste, boraviste,
               kontakt, row))

    conn.commit()
    conn.close()


def fetch_all_users():
    try:
        c, conn = connection()
        c.execute("SELECT * FROM users ORDER BY id")
        rows = c.fetchall()
        conn.close()
        return rows
    except psycopg2.errors.UndefinedTable as e:
        messagebox.showerror("Error occurred", f"Database is empty: {e}")
    except Error as e:
        messagebox.showerror("Error occurred", f"Database error: {e}")
        return []


def create_user_details_table():
    c, conn = connection()
    # Create the user_details table
    c.execute('''CREATE TABLE IF NOT EXISTS user_details (
                user_id SERIAL PRIMARY KEY,
                agencija TEXT,
                agent TEXT,
                krajnji_korisnik TEXT,
                policijska_postaja TEXT,
                datum_apliciranja DATE,
                datum_hzz DATE,
                datum_dozvole DATE,
                datum_istek_dozvole DATE,
                datum_vize DATE,
                datum_dolaska DATE, 
                datum_lijecnickog DATE,
                datum_ID DATE,
                datum_istek_ID DATE,
                datum_prijave DATE,
                datum_referentni_broj DATE,
                referentni_broj TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
                )''')

    # Commit changes and close connection
    conn.commit()
    conn.close()


def add_user_details(user_id, agencija, agent, krajnji_korisnik, datum_apliciranja, policijska_postaja, datum_hzz,
                     datum_dozvole, datum_istek_dozvole, datum_vize, datum_dolaska, datum_lijecnickog,
                     datum_ID, datum_istek_ID, datum_prijave, datum_referentni_broj, referentni_broj):
    c, conn = connection()

    c.execute('''INSERT INTO user_details (user_id, agencija, agent, krajnji_korisnik, policijska_postaja, 
                    datum_apliciranja, datum_hzz, datum_dozvole, datum_istek_dozvole, datum_vize, datum_dolaska, 
                    datum_lijecnickog, datum_ID, datum_istek_ID, datum_prijave, datum_referentni_broj, referentni_broj) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (user_id) DO UPDATE
                    SET agencija = excluded.agencija,
                        agent = excluded.agent,
                        krajnji_korisnik = excluded.krajnji_korisnik,
                        policijska_postaja = excluded.policijska_postaja,
                        datum_apliciranja = excluded.datum_apliciranja,
                        datum_hzz = excluded.datum_hzz,
                        datum_dozvole = excluded.datum_dozvole,
                        datum_istek_dozvole = excluded.datum_istek_dozvole,
                        datum_vize = excluded.datum_vize,
                        datum_dolaska = excluded.datum_dolaska,
                        datum_lijecnickog = excluded.datum_lijecnickog,
                        datum_ID = excluded.datum_ID,
                        datum_istek_ID = excluded.datum_istek_ID,
                        datum_prijave = excluded.datum_prijave,
                        datum_referentni_broj = excluded.datum_referentni_broj,
                        referentni_broj = excluded.referentni_broj''',
              (user_id, agencija, agent, krajnji_korisnik, datum_apliciranja, policijska_postaja, datum_hzz,
               datum_dozvole, datum_istek_dozvole, datum_vize, datum_dolaska, datum_lijecnickog,
               datum_ID, datum_istek_ID, datum_prijave, datum_referentni_broj, referentni_broj))

    conn.commit()
    conn.close()


def create_work_history_table():
    c, conn = connection()
    # Create the user_details table
    c.execute('''CREATE TABLE IF NOT EXISTS work_history (
                        id SERIAL PRIMARY KEY,
                        user_id INT,
                        partner TEXT, 
                        datum_pocetka DATE, 
                        datum_zavrsetka DATE, 
                        radni_sati INT,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                        )''')

    # Commit changes and close connection
    conn.commit()
    conn.close()


def add_work_history(user_id, partner, datum_pocetka, datum_zavrsetka, radni_sati):
    c, conn = connection()
    c.execute('''INSERT INTO work_history (user_id, partner, datum_pocetka, datum_zavrsetka, radni_sati) 
                 VALUES (%s, %s, %s, %s, %s)''',
              (user_id, partner, datum_pocetka, datum_zavrsetka, radni_sati))
    conn.commit()
    conn.close()


# Searches for the last row with the users id
def update_wh_row(user_id, partner, datum_pocetka, datum_zavrsetka, radni_sati):
    c, conn = connection()
    # Find the last row with the given user_id
    c.execute('''SELECT id FROM work_history WHERE user_id = %s ORDER BY id DESC LIMIT 1''', (user_id,))
    row = c.fetchone()
    if row:
        row_id = row[0]
        # Update the last row with the new values
        c.execute('''UPDATE work_history 
                         SET user_id = %s, partner = %s, datum_pocetka = %s, datum_zavrsetka = %s, radni_sati = %s
                         WHERE id = %s''',
                  (user_id, partner, datum_pocetka, datum_zavrsetka, radni_sati, row_id))
        conn.commit()
    else:
        messagebox.showerror("Error", "No history found for the specified user_id.")
    conn.close()


def create_files_table():
    c, conn = connection()
    # Create the users table
    c.execute('''CREATE TABLE IF NOT EXISTS files (
                id SERIAL PRIMARY KEY,
                user_id INTEGER,
                file_path TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
                )''')

    # Commit changes and close connection
    conn.commit()
    conn.close()


def label_to_entry(label, master, entry_list):
    info = label.grid_info()
    row = info["row"]
    column = info["column"]
    width = label.cget("width")
    text = label.cget("text")
    label.destroy()

    entry = customtkinter.CTkEntry(master=master, width=width, placeholder_text=text)
    entry.grid(row=row, column=column)

    entry_list[row] = entry


def create_db_gui():
    create_user_details_table()

    db_window = customtkinter.CTk()
    db_window.title("BAZA PODATAKA")

    # Get screen dimensions
    screen_width = db_window.winfo_screenwidth()
    screen_height = db_window.winfo_screenheight()

    # Calculate window width and height
    db_window_width = int(screen_width * 0.9)
    db_window_height = int(screen_height * 0.9)

    # Calculate window position to center it on the screen
    x_position = (screen_width - db_window_width) // 2
    y_position = (screen_height - db_window_height) // 2

    # Set window size and position
    db_window.geometry(f"{db_window_width}x{db_window_height}+{x_position}+{y_position}")

    frame_width = int(db_window_width * 1)
    frame_height = int(db_window_height * 1)

    users = fetch_all_users()

    # Adding headers for the table
    headers = ["REDNI BROJ", "IME", "PREZIME", "OIB", "BROJ PUTOVNICE", "ID BROJ", "DATUM ROĐENJA", "MJESTO ROĐENJA",
               "PREBIVALIŠTE", "MATIČNA ZEMLJA", "KONTAKT"]

    # Convert fetched data into suitable format for the table
    table_data = []
    for user in users:
        table_data.append(list(user))

    def get_agencija_by_user_id(user_id):
        c, conn = connection()
        c.execute('SELECT agencija FROM user_details WHERE user_id = %s', (user_id,))
        result = c.fetchone()
        conn.close()
        if result:
            return result[0]

    def get_initials(name):
        # Split the name into words
        words = name.split()
        # Take the first letter of each word and join them
        initials = ''.join([word[0].upper() for word in words])

        return initials

    table_data.insert(0, headers)
    for tb in table_data[1:]:
        agencija = get_agencija_by_user_id(tb[0])

        # Format tb[0] with leading zeros
        if tb[0] <= 9:
            tb[0] = f"00{tb[0]}"
        elif 10 <= tb[0] < 100:
            tb[0] = f"0{tb[0]}"
        else:
            tb[0] = str(tb[0])

        if agencija is not None:
            initials = get_initials(agencija)
            tb[0] = f"{initials}{tb[0]}"

    def row_clicked(row_data):
        global i
        user_id = row_data["row"]
        selected_user = users[user_id - 1]  # Adjust for zero-based index
        selected_user_id = selected_user[0]  # Get the user_id

        ud_window = customtkinter.CTk()
        ud_window.title("USER DETAILS")

        ud_window_width = int(db_window_width * 0.5)
        ud_window_height = int(db_window_height * 0.8)

        x_pos = (screen_width - ud_window_width) // 2
        y_pos = (screen_height - ud_window_height) // 2

        ud_window.geometry(f"{ud_window_width}x{ud_window_height}+{x_pos}+{y_pos}")

        tabs = customtkinter.CTkTabview(ud_window, width=ud_window_width, height=ud_window_height, corner_radius=30,
                                        anchor="n", segmented_button_fg_color="white")
        tabs.pack(padx=0, pady=0)

        tabs.add("OSOBNI PODATCI")
        frame_op = customtkinter.CTkFrame(master=tabs.tab("OSOBNI PODATCI"))
        frame_op.pack(fill="both", padx=20, pady=10)

        entry_fields4 = []

        for i, (header, value) in enumerate(zip(headers, selected_user)):
            label = customtkinter.CTkLabel(master=frame_op, text=header, anchor="w", width=200,
                                           corner_radius=30, fg_color="lightblue", text_color="black")
            label.grid(row=i, column=0, padx=5, pady=5)
            if value is not None:
                label_value = customtkinter.CTkLabel(master=frame_op, text=value, anchor="w", width=300,
                                                     corner_radius=30, fg_color="white", text_color="black")
                label_value.grid(row=i, column=1, padx=5, pady=5)
                entry_fields4.append(label_value)
                label_value.bind("<Double-Button-1>", lambda event, oznaka=label_value,
                                                             master=frame_op, unos=entry_fields4:
                label_to_entry(oznaka, master, unos))
            else:
                entry = customtkinter.CTkEntry(master=frame_op, width=300)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entry_fields4.append(entry)

        def save_all_data():
            try:
                save_user_updates()
                save_data()
                save_wh_data()
                messagebox.showinfo("Spremljene izmjene", "Uspješno spremljene izmjene")
                ud_window.destroy()
                new_table_data = []
                new_users = fetch_all_users()
                for new_user in new_users:
                    new_table_data.append(list(new_user))
                new_table_data.insert(0, headers)
                for ntb in new_table_data[1:]:
                    a = get_agencija_by_user_id(ntb[0])
                    # Format tb[0] with leading zeros
                    if ntb[0] <= 9:
                        ntb[0] = f"00{ntb[0]}"
                    elif 10 <= ntb[0] < 100:
                        ntb[0] = f"0{ntb[0]}"
                    else:
                        ntb[0] = str(ntb[0])
                    if a is not None:
                        initial = get_initials(a)
                        ntb[0] = f"{initial}{ntb[0]}"
                table.update_values(new_table_data)
                db_window.lift()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving data: {e}")

        def save_user_updates():
            try:
                data = []
                for vals in entry_fields4:
                    if isinstance(vals, customtkinter.CTkLabel):
                        v = vals.cget("text")
                    elif isinstance(vals, customtkinter.CTkEntry):
                        v = vals.get()
                        if not v:  # Check if v is an empty string
                            v = None
                    else:
                        return

                    data.append(v)

                update_user(*data[1:], selected_user_id)

            except (psycopg2.Error, psycopg2.DatabaseError) as e:
                messagebox.showerror("Database Error", f"Error adding user details: {e}")
                ud_window.lift()

            except errors.InvalidDatetimeFormat:
                messagebox.showerror(title="Error", message="Wrong date format!\nSave date like this : YYYY.MM.DD."
                                                            "\nexample : 1896.04.21.")
                ud_window.lift()

            except errors.DatetimeFieldOverflow:
                messagebox.showerror(title="Error", message="Date out of range!")
                ud_window.lift()

        save_user_button = customtkinter.CTkButton(master=frame_op, text="Save", width=200, height=40,
                                                   command=save_all_data)
        save_user_button.grid(row=i + 1, column=1, padx=5, pady=5)

        # Fetch user details from user_details table
        c, conn = connection()
        c.execute("SELECT * FROM user_details WHERE user_id = %s", (selected_user[0],))
        user_details = c.fetchone()
        conn.close()

        tabs.add("AGENCIJA")
        frame_agencija = customtkinter.CTkScrollableFrame(master=tabs.tab("AGENCIJA"), width=ud_window_width,
                                                          height=ud_window_height)
        frame_agencija.pack(fill="both", padx=20, pady=10)
        # Populate the second table with headers and corresponding values
        headers2 = ["agencija", "agent", "krajnji_korisnik", "policijska_postaja", "datum_apliciranja",
                    "datum_hzz", "datum_dozvole", "datum_istek_dozvole", "datum_vize",
                    "datum_dolaska", "datum_lijecnickog", "datum_ID", "datum_istek_ID", "datum_prijave",
                    "datum_referentni_broj", "referentni_broj"]

        entry_fields = []
        if user_details is not None:
            for i, (header, value) in enumerate(zip(headers2, user_details[1:])):
                label = customtkinter.CTkLabel(master=frame_agencija, text=header, anchor="w", width=200,
                                               corner_radius=30, fg_color="lightblue", text_color="black")
                label.grid(row=i, column=0, padx=5, pady=5)
                if value is not None:
                    label_value = customtkinter.CTkLabel(master=frame_agencija, text=value, anchor="w", width=300,
                                                         corner_radius=30, fg_color="white", text_color="black")
                    label_value.grid(row=i, column=1, padx=5, pady=5)
                    entry_fields.append(label_value)
                    label_value.bind("<Double-Button-1>", lambda event, oznaka=label_value,
                                                                 master=frame_agencija, unos=entry_fields:
                    label_to_entry(oznaka, master, unos))

                else:
                    entry = customtkinter.CTkEntry(master=frame_agencija, width=300)
                    entry.grid(row=i, column=1, padx=5, pady=5)
                    entry_fields.append(entry)
        else:
            # If user_details is None, display entry fields for all headers
            for i, header in enumerate(headers2):
                label = customtkinter.CTkLabel(master=frame_agencija, text=header, anchor="w", width=200,
                                               corner_radius=30, fg_color="lightblue", text_color="black")
                label.grid(row=i, column=0, padx=5, pady=5)
                entry = customtkinter.CTkEntry(master=frame_agencija, width=300)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entry_fields.append(entry)

        # Function to save data
        def save_data():
            try:
                data = []
                for vals in entry_fields:
                    if isinstance(vals, customtkinter.CTkLabel):
                        v = vals.cget("text")
                    elif isinstance(vals, customtkinter.CTkEntry):
                        v = vals.get()
                        if not v:  # Check if v is an empty string
                            v = None
                    else:
                        return

                    data.append(v)

                add_user_details(selected_user_id, *data)

            except (psycopg2.Error, psycopg2.DatabaseError) as e:
                messagebox.showerror("Database Error", f"Error adding user details: {e}")
                ud_window.lift()

            except errors.InvalidDatetimeFormat:
                messagebox.showerror(title="Error", message="Wrong date format!\nSave date like this : YYYY.MM.DD."
                                                            "\nexample : 1896.04.21.")
                ud_window.lift()

            except errors.DatetimeFieldOverflow:
                messagebox.showerror(title="Error", message="Date out of range!")
                ud_window.lift()

        # Add a button to save the data
        save_button = customtkinter.CTkButton(master=frame_agencija, text="Save", width=200, height=40,
                                              command=save_all_data)
        save_button.grid(row=i + 1, column=1, padx=5, pady=5)

        tabs.add("POVIJEST RADA")
        create_work_history_table()
        c, conn = connection()
        c.execute("SELECT * FROM work_history WHERE user_id = %s", (selected_user[0],))
        work_history = c.fetchall()
        conn.close()

        frame_wh = customtkinter.CTkFrame(master=tabs.tab("POVIJEST RADA"))
        frame_wh.pack(fill="both", padx=40, pady=0)
        headers4 = ["Partner", "Početak rada", "Završetak rada", "Radni sati"]

        b = 0
        n_start = 2  # Choose the starting row index

        def add_entry_fields(ns, bs, e_list):
            try:
                entries_counter = 0

                for vals in entry_fields3[-4:]:
                    if isinstance(vals, customtkinter.CTkEntry):
                        entries_counter += 1
                    if entries_counter > 1:
                        raise ImportError("Can not add more fields")

                entry_fields_row = []
                for _ in headers4:
                    e = customtkinter.CTkEntry(master=frame_wh, width=int(ud_window_width / 5.5), corner_radius=30)
                    e.grid(row=ns, column=bs, padx=5, pady=5)
                    entry_fields_row.append(e)
                    bs += 1
                ns += 1
                e_list.extend(entry_fields_row)

            except ImportError as e:
                messagebox.showerror("Import error", str(e))
                ud_window.lift()

        def save_wh_data():
            try:
                data = []
                entries_counter = 0
                for vals in entry_fields3:
                    if isinstance(vals, customtkinter.CTkLabel):
                        v = vals.cget("text")
                    elif isinstance(vals, customtkinter.CTkEntry):
                        v = vals.get()
                        entries_counter += 1
                        if not v:  # Check if v is an empty string
                            v = None
                    else:
                        return

                    data.append(v)

                if entries_counter > 4:
                    raise ValueError("Trying to save too much data")

                if len(work_history) == 0:
                    add_work_history(selected_user_id, *data[-4:])
                else:
                    none_count = 0
                    for whd in work_history[-1]:
                        if whd is None:
                            none_count += 1
                    if none_count == 0:
                        add_work_history(selected_user_id, *data[-4:])
                    else:
                        update_wh_row(selected_user_id, *data[-4:])

            except ValueError as e:
                messagebox.showerror("Data error", str(e))
                ud_window.lift()

            except (psycopg2.Error, psycopg2.DatabaseError) as e:
                messagebox.showerror("Database Error", f"Error adding user details: {e}")
                ud_window.lift()

            except errors.InvalidDatetimeFormat:
                messagebox.showerror(title="Error", message="Wrong date format!\nSave date like this : YYYY.MM.DD."
                                                            "\nexample : 1896.04.21.")
                ud_window.lift()

            except errors.DatetimeFieldOverflow:
                messagebox.showerror(title="Error", message="Date out of range!")
                ud_window.lift()

        entry_fields3 = []

        entries_button = customtkinter.CTkButton(frame_wh, width=int((ud_window_width / 5.5) * 2), text="ADD DATA",
                                                 anchor="center", fg_color="blue", text_color="black",
                                                 corner_radius=30, command=lambda: add_entry_fields(n_start, b,
                                                                                                    entry_fields3))
        entries_button.grid(row=0, column=0, columnspan=2)

        save_wh_data_button = customtkinter.CTkButton(frame_wh, width=int((ud_window_width / 5.5) * 2),
                                                      text="SAVE DATA", anchor="center", fg_color="blue",
                                                      text_color="black", corner_radius=30, command=save_all_data)
        save_wh_data_button.grid(row=0, column=2, columnspan=2)

        if work_history:
            for w in work_history:
                for n, (h, wh) in enumerate(zip(headers4, w[2:]), start=n_start):
                    label = customtkinter.CTkLabel(master=frame_wh, text=h, width=int(ud_window_width / 5.5),
                                                   anchor="w",
                                                   fg_color="lightblue", text_color="black", corner_radius=30)
                    label.grid(row=1, column=b, padx=5, pady=5)
                    if wh is not None:
                        label = customtkinter.CTkLabel(master=frame_wh, text=wh, width=int(ud_window_width / 5.5),
                                                       anchor="w", fg_color="white", text_color="black",
                                                       corner_radius=30)
                        label.grid(row=n_start, column=b, padx=5, pady=5)
                        entry_fields3.append(label)
                        b += 1
                    else:
                        entry = customtkinter.CTkEntry(master=frame_wh, width=int(ud_window_width / 5.5),
                                                       corner_radius=30)
                        entry.grid(row=n_start, column=b, padx=5, pady=5)
                        b += 1
                        entry_fields3.append(entry)
                n_start += 1
                b = 0
        else:
            for h in headers4:
                label = customtkinter.CTkLabel(master=frame_wh, text=h, width=int(ud_window_width / 5.5), anchor="w",
                                               fg_color="lightblue", text_color="black", corner_radius=30)
                label.grid(row=1, column=b, padx=5, pady=5)
                entry = customtkinter.CTkEntry(master=frame_wh, width=int(ud_window_width / 5.5), corner_radius=30)
                entry.grid(row=n_start, column=b, padx=5, pady=5)
                entry_fields3.append(entry)
                b += 1

        tabs.add("DOKUMENTI")

        def convert_tuples_to_strings(tuple_list):
            return [item[0] for item in tuple_list]

        def open_pdf(line_content):
            global pdf_file_path  # Make sure pdf_file_path is defined elsewhere
            file_paths = update_textbox()  # Assuming this function updates the textbox with file paths
            file_paths = convert_tuples_to_strings(file_paths)  # Convert to a list of strings

            found_path = None

            for path in file_paths:
                if line_content.lower() in os.path.basename(path).lower():
                    found_path = path
                    break

            if found_path:
                if os.path.exists(found_path):
                    try:
                        # Use subprocess.Popen to open the PDF file
                        subprocess.Popen([found_path], shell=True)
                        print(f"Opened: {found_path}")
                    except Exception as e:
                        print(f"Failed to open file: {e}")
                else:
                    print("File not found.")
            else:
                print(f"File with name '{line_content}' not found in any of the paths.")

        # Example usage
        def on_click(event):
            index = textbox.index(tk.INSERT)
            line, _ = map(int, index.split('.'))
            line_content = textbox.get(f"{line}.0", f"{line}.end").strip()
            open_pdf(line_content)

        def save_pdf_path():
            global pdf_file_path
            pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if pdf_file_path:
                c, conn = connection()
                c.execute("INSERT INTO files (user_id, file_path) VALUES (%s, %s)", (user_id, pdf_file_path))
                conn.commit()
                conn.close()
                update_textbox()
                print(f"PDF file path saved successfully: {pdf_file_path}")

        # Function to update the text box with file paths from the database
        def update_textbox():
            c, conn = connection()
            c.execute("SELECT file_path FROM files WHERE user_id = %s", (user_id,))
            file_paths = c.fetchall()
            textbox.delete('1.0', tk.END)  # Clear the existing content
            for path in file_paths:
                filename = os.path.basename(path[0])
                textbox.insert(tk.END, filename + '\n')
            conn.close()

            return file_paths

        textbox = customtkinter.CTkTextbox(tabs.tab("DOKUMENTI"), wrap=tk.WORD, height=int(ud_window_height * 0.6),
                                           width=int(ud_window_width * 0.8), font=("Ariel", 20), corner_radius=30,
                                           border_width=2, border_color="blue")
        textbox.pack(pady=10)
        update_textbox()
        textbox.bind("<Double-Button-1>", on_click)
        # Create a button to save PDF file path
        save_button = customtkinter.CTkButton(tabs.tab("DOKUMENTI"), text="Save PDF Path", corner_radius=30,
                                              width=int(ud_window_width * 0.5), command=save_pdf_path)
        save_button.pack(pady=10)

        tabs.set("OSOBNI PODATCI")

        def on_close():
            response = messagebox.askyesnocancel("Save Data", "Do you want to save data before closing?")
            if response is True:
                save_all_data()
            elif response is False:
                ud_window.destroy()
                db_window.lift()
            else:
                db_window.lift()
                ud_window.lift()
                return

        ud_window.protocol("WM_DELETE_WINDOW", on_close)

        ud_window.mainloop()

    tabs2 = customtkinter.CTkTabview(master=db_window, width=db_window_width, height=db_window_height, corner_radius=30,
                                     anchor="n", segmented_button_fg_color="white")
    tabs2.pack(padx=0, pady=0)

    tabs2.add("BAZA PODATAKA")

    frame = customtkinter.CTkScrollableFrame(master=tabs2.tab("BAZA PODATAKA"), width=frame_width, height=frame_height,
                                             scrollbar_button_color="white")
    frame.pack()

    rows = []

    def find_user_row_number(user_id):
        c, conn = connection()
        cursor = conn.cursor()

        # Execute a SQL query to find the row number of the user
        # Execute a SQL query to count the number of rows before the user
        cursor.execute("SELECT COUNT(*) FROM users WHERE id < %s", (user_id,))
        position = cursor.fetchone()[0] + 1  # Add 1 to account for 0-based indexing

        if position > 0:
            rows.append(position)
            return position
        else:
            print(f"No user found with ID {user_id}")

        # Close cursor and connection
        cursor.close()
        conn.close()

    def search_table_data():
        if len(rows) > 0:
            for p in rows:
                table.deselect_row(p)
                rows.remove(p)
        search_data = search_entry.get()
        data_found = False
        for td in table_data:
            if search_data == str(td[0]):
                row_num = find_user_row_number(td[0])
                table.select_row(row_num)
                data_found = True
            else:
                if search_data in td:
                    row_id = td[0]
                    row_num = find_user_row_number(row_id)
                    try:
                        table.select_row(row_num)
                        data_found = True  # Set to True if data is found

                    except KeyError:
                        print("Row", row_num, "does not exist in the table.")

        if not data_found:
            messagebox.showinfo("Not found", "There is no data matching the entry\nCheck the entered data")
            db_window.lift()

    search_frame = customtkinter.CTkFrame(master=frame, width=frame_width)
    search_frame.pack()

    search_entry = customtkinter.CTkEntry(master=search_frame, width=400, placeholder_text="UNESI POJAM ZA PRETRAGU")
    search_entry.pack(side="left")

    search_button = customtkinter.CTkButton(master=search_frame, width=150, text="TRAŽI", command=search_table_data,
                                            text_color="black")
    search_button.pack(side="left")

    table_frame = customtkinter.CTkFrame(master=frame, width=frame_width)
    table_frame.pack()

    table = CTkTable(master=table_frame, row=len(table_data), column=len(headers), values=table_data,
                     colors=["white", "white"], text_color="black", header_color="lightblue", command=row_clicked,
                     hover_color="lightblue")
    table.pack(expand=True, fill="both", padx=0, pady=int(frame_width / 138), side="right")

    tabs2.add("SLOBODNI")

    frame_slobodni = customtkinter.CTkScrollableFrame(tabs2.tab("SLOBODNI"), width=frame_width,
                                                      height=frame_height, scrollbar_button_color="white")
    frame_slobodni.pack()

    c, conn = connection()
    c.execute('''SELECT u.id, u.name, u.surname, u.putovnica 
                 FROM users u 
                 WHERE u.id NOT IN 
                 (SELECT ud.user_id FROM user_details ud 
                 WHERE ud.datum_apliciranja IS NOT NULL 
                 AND ud.krajnji_korisnik IS NOT NULL)''')
    free_users = c.fetchall()
    conn.close()

    free_users_counted = len(free_users)

    slobodni_ljudi_label = customtkinter.CTkLabel(master=frame_slobodni,
                                                  text=f"BROJ SLOBODNIH LJUDI: {free_users_counted}", corner_radius=30,
                                                  fg_color="white", text_color="black", font=("Ariel", 25))
    slobodni_ljudi_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=int(frame_width / 69))

    headers_slobodni = ["REDNI BROJ", "IME", "PREZIME", "BROJ PUTOVNICE"]
    column = 0
    for hs in headers_slobodni:
        labels = customtkinter.CTkLabel(master=frame_slobodni, text=hs, anchor="w", width=int(frame_width / 5),
                                        corner_radius=30, fg_color="lightblue", text_color="black")
        labels.grid(row=1, column=column, padx=int(frame_width / 69), pady=int(frame_width / 138))
        column += 1

    row = 2
    for fs in free_users:
        column = 0
        for s in fs:
            fs_label = customtkinter.CTkLabel(master=frame_slobodni, text=s, anchor="w", width=int(frame_width / 5),
                                              corner_radius=30, fg_color="white", text_color="black")
            fs_label.grid(row=row, column=column, padx=int(frame_width / 69), pady=int(frame_width / 138))
            column += 1
        row += 1

    tabs2.add("APLICIRANI")

    frame_aplicirani = customtkinter.CTkScrollableFrame(master=tabs2.tab("APLICIRANI"), width=frame_width,
                                                        height=frame_height, scrollbar_button_color="white")
    frame_aplicirani.pack()

    c, conn = connection()
    c.execute('''SELECT users.id, users.name, users.surname, users.putovnica
                 FROM users
                 INNER JOIN user_details ON users.id = user_details.user_id
                 WHERE user_details.datum_apliciranja IS NOT NULL 
                 AND user_details.krajnji_korisnik IS NOT NULL
                 AND users.oib IS NULL''')
    not_free_users = c.fetchall()
    conn.close()

    c, conn = connection()
    today = date.today().strftime('%Y-%m-%d')
    c.execute('''SELECT COUNT(*)
                         FROM users
                         INNER JOIN user_details ON users.id = user_details.user_id
                         WHERE users.oib IS NULL
                         AND datum_apliciranja = %s''', (today,))
    aplicirani_danas_count = c.fetchone()[0]

    not_free_users_count = len(not_free_users)
    aplicirani_count_label = customtkinter.CTkLabel(master=frame_aplicirani,
                                                    text=f"BROJ APLICIRANIH LJUDI: {not_free_users_count}    "
                                                         f"BROJ APLICIRANIH DANAS: {aplicirani_danas_count}",
                                                    corner_radius=30, fg_color="white", text_color="black",
                                                    font=("Ariel", 25))
    aplicirani_count_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=int(frame_width / 69))

    column = 0
    for ha in headers_slobodni:
        labels = customtkinter.CTkLabel(master=frame_aplicirani, text=ha, anchor="w", width=int(frame_width / 5),
                                        corner_radius=30, fg_color="lightblue", text_color="black")
        labels.grid(row=1, column=column, padx=int(frame_width / 69), pady=int(frame_width / 138))
        column += 1

    row = 2
    for nfs in not_free_users:
        column = 0
        for nf in nfs:
            nfs_label = customtkinter.CTkLabel(master=frame_aplicirani, text=nf, anchor="w", width=int(frame_width / 5),
                                               corner_radius=30, fg_color="white", text_color="black")
            nfs_label.grid(row=row, column=column, padx=int(frame_width / 69), pady=int(frame_width / 138))
            column += 1
        row += 1

    tabs2.add("Na putu za HR")

    c, conn = connection()
    c.execute('''SELECT users.id, users.name, users.surname, users.putovnica
                 FROM users
                 INNER JOIN user_details ON users.id = user_details.user_id
                 WHERE users.oib IS NULL 
                 AND user_details.datum_vize IS NOT NULL''')
    on_the_way = c.fetchall()
    conn.close()

    ow_frame = customtkinter.CTkScrollableFrame(master=tabs2.tab("Na putu za HR"), width=frame_width,
                                                height=frame_height, scrollbar_button_color="white")
    ow_frame.pack()

    column = 0
    for ha in headers_slobodni:
        labels = customtkinter.CTkLabel(master=ow_frame, text=ha, anchor="w", width=int(frame_width / 5),
                                        corner_radius=30, fg_color="lightblue", text_color="black")
        labels.grid(row=0, column=column, padx=int(frame_width / 69), pady=int(frame_width / 138))
        column += 1

    row = 1
    for ow in on_the_way:
        column = 0
        for o in ow:
            nfs_label = customtkinter.CTkLabel(master=ow_frame, text=o, anchor="w", width=int(frame_width / 5),
                                               corner_radius=30, fg_color="white", text_color="black")
            nfs_label.grid(row=row, column=column, padx=int(frame_width / 69), pady=int(frame_width / 138))
            column += 1
        row += 1

    tabs2.add("U Hrvatskoj")

    c, conn = connection()
    c.execute('''SELECT users.id, users.name, users.surname, users.putovnica
                 FROM users
                 INNER JOIN user_details ON users.id = user_details.user_id
                 WHERE users.oib IS NOT NULL 
                 AND user_details.datum_vize IS NOT NULL''')
    users_here = c.fetchall()
    conn.close()

    uh_frame = customtkinter.CTkScrollableFrame(master=tabs2.tab("U Hrvatskoj"), width=frame_width,
                                                height=frame_height, scrollbar_button_color="white")
    uh_frame.pack()

    column = 0
    for ha in headers_slobodni:
        labels = customtkinter.CTkLabel(master=uh_frame, text=ha, anchor="w", width=int(frame_width / 5),
                                        corner_radius=30, fg_color="lightblue", text_color="black")
        labels.grid(row=0, column=column, padx=int(frame_width / 69), pady=int(frame_width / 138))
        column += 1

    row = 1
    for uh in users_here:
        column = 0
        for u in uh:
            nfs_label = customtkinter.CTkLabel(master=uh_frame, text=u, anchor="w", width=int(frame_width / 5),
                                               corner_radius=30, fg_color="white", text_color="black")
            nfs_label.grid(row=row, column=column, padx=int(frame_width / 69), pady=int(frame_width / 138))
            column += 1
        row += 1

    db_window.mainloop()
