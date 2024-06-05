import datetime
from datetime import timedelta
import customtkinter
import psycopg2
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


alarm_list = []
alarms1 = []
alarms2 = []
alarms3 = []
alarms4 = []


def table_exists(table_name):
    try:
        c, conn = connection()
        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)", (table_name,))
        exists = c.fetchone()[0]
        conn.close()
        return exists
    except psycopg2.Error as e:
        print("Error checking table existence:", e)
        return False


def apliciranje_alarm():
    if table_exists('user_details'):
        c, conn = connection()
        c.execute("SELECT ud.user_id, ud.datum_apliciranja, ud.datum_hzz, u.name, u.surname, u.putovnica FROM "
                  "user_details ud JOIN users u ON ud.user_id = u.id")
        rows = c.fetchall()

        for row in rows:
            user_id, apliciranja_date, hzz_date, name, surname, putovnica = row
            if apliciranja_date and not hzz_date:
                fifteen_days_after = apliciranja_date + timedelta(days=15)
                if datetime.date.today() >= fifteen_days_after:
                    alarm_list.append(row)
                    alarms1.append(row)
        conn.close()
    else:
        pass


def dozvola_alarm():
    if table_exists('user_details'):
        c, conn = connection()
        c.execute("SELECT ud.user_id, u.name, u.surname, u.putovnica, ud.datum_istek_dozvole FROM user_details ud JOIN "
                  "users u ON ud.user_id = u.id")
        rows = c.fetchall()

        for row in rows:
            user_id, name, surname, putovnica, datum_istek_dozvole = row
            if datum_istek_dozvole:
                thirty_days_before = datum_istek_dozvole - timedelta(days=30)
                if datetime.date.today() >= thirty_days_before:
                    alarm_list.append(row)
                    alarms2.append(row)
        conn.close()
    else:
        pass


def id_alarm():
    if table_exists('user_details'):
        c, conn = connection()
        c.execute("SELECT ud.user_id, u.name, u.surname, u.putovnica, ud.datum_istek_ID FROM user_details ud JOIN "
                  "users u ON ud.user_id = u.id")

        rows = c.fetchall()

        for row in rows:
            user_id, name, surname, putovnica, datum_istek_ID = row
            if datum_istek_ID:
                thirty_days_before = datum_istek_ID - timedelta(days=30)
                if datetime.date.today() >= thirty_days_before:
                    alarm_list.append(row)
                    alarms3.append(row)
        conn.close()
    else:
        pass


def referentni_broj_alarm():
    if table_exists('user_details'):
        c, conn = connection()
        c.execute("SELECT ud.user_id, u.name, u.surname, u.putovnica, ud.datum_vize, ud.datum_referentni_broj FROM "
                  "user_details ud JOIN users u ON ud.user_id = u.id")
        rows = c.fetchall()

        for row in rows:
            user_id, name, surname, putovnica, datum_vize, datum_referentni_broj = row
            if datum_referentni_broj:
                thirty_five_days_ahead = datum_referentni_broj + timedelta(days=35)
                if datetime.date.today() >= thirty_five_days_ahead and not datum_vize:
                    alarm_list.append(row)
                    alarms4.append(row)
        conn.close()
    else:
        pass


def alarms():
    alarm_list.clear()
    alarms1.clear()
    alarms2.clear()
    alarms3.clear()
    alarms4.clear()
    apliciranje_alarm()
    dozvola_alarm()
    id_alarm()
    referentni_broj_alarm()


def create_alarmi_window():
    alarms()
    aw = customtkinter.CTk()
    aw.title("ALARMI")

    aw_width = 1250
    aw_height = 800

    # Get screen dimensions
    screen_width = aw.winfo_screenwidth()
    screen_height = aw.winfo_screenheight()

    aw_x_pos = (screen_width - aw_width) // 2
    aw_y_pos = (screen_height - aw_height) // 2
    aw.geometry(f"{aw_width}x{aw_height}+{aw_x_pos}+{aw_y_pos}")

    frame = customtkinter.CTkScrollableFrame(master=aw, width=1180, height=800, corner_radius=30)
    frame.pack()

    r = 0
    for alarm in alarm_list:
        if alarm in alarms1:
            label = customtkinter.CTkLabel(master=frame, fg_color="lightblue", text=f"User ID: {alarm[0]}",
                                           text_color="black", width=120, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=0, pady=10, padx=5)
            label = customtkinter.CTkLabel(master=frame, fg_color="white", text=f"Ime: {alarm[3]}",
                                           text_color="black", width=250, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=1, pady=10, padx=5)
            label = customtkinter.CTkLabel(master=frame, fg_color="white", text=f"Prezime: {alarm[4]}",
                                           text_color="black", width=250, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=2, pady=10, padx=5)
            label = customtkinter.CTkLabel(master=frame, fg_color="white", text=f"Broj putovnice: {alarm[5]}",
                                           text_color="black", width=250, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=3, pady=10, padx=5)
            label = customtkinter.CTkLabel(master=frame, fg_color="lightblue", text=f"Datum apliciranja: {alarm[1]}",
                                           text_color="black", width=250, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=4, pady=10, padx=5)

            r += 1

        if alarm in alarms2:
            label = customtkinter.CTkLabel(master=frame, fg_color="lightblue", text=f"User ID: {alarm[0]}",
                                           text_color="black", width=120, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=0, pady=10, padx=5)
            label = customtkinter.CTkLabel(master=frame, fg_color="white", text=f"Ime: {alarm[1]}",
                                           text_color="black", width=250, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=1, pady=10, padx=5)
            label = customtkinter.CTkLabel(master=frame, fg_color="white", text=f"Prezime: {alarm[2]}",
                                           text_color="black", width=250, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=2, pady=10, padx=5)
            label = customtkinter.CTkLabel(master=frame, fg_color="white", text=f"Broj putovnice: {alarm[3]}",
                                           text_color="black", width=250, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=3, pady=10, padx=5)
            label = customtkinter.CTkLabel(master=frame, fg_color="lightblue", text=f"Datum isteka dozvole: {alarm[4]}",
                                           text_color="black", width=250, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=4, pady=10, padx=5)

            r += 1
        if alarm in alarms3:
            label = customtkinter.CTkLabel(master=frame, fg_color="lightblue", text=f"User ID: {alarm[0]}",
                                           text_color="black", width=120, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=0, pady=10, padx=5)
            label = customtkinter.CTkLabel(master=frame, fg_color="white", text=f"Ime: {alarm[1]}",
                                           text_color="black", width=250, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=1, pady=10, padx=5)
            label = customtkinter.CTkLabel(master=frame, fg_color="white", text=f"Prezime: {alarm[2]}",
                                           text_color="black", width=250, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=2, pady=10, padx=5)
            label = customtkinter.CTkLabel(master=frame, fg_color="white", text=f"Broj putovnice: {alarm[3]}",
                                           text_color="black", width=250, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=3, pady=10, padx=5)
            label = customtkinter.CTkLabel(master=frame, fg_color="lightblue", text=f"Datum isteka ID: {alarm[4]}",
                                           text_color="black", width=250, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=4, pady=10, padx=5)

            r += 1
        if alarm in alarms4:
            label = customtkinter.CTkLabel(master=frame, fg_color="lightblue", text=f"User ID: {alarm[0]}",
                                           text_color="black", width=120, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=0, pady=10, padx=5)
            label = customtkinter.CTkLabel(master=frame, fg_color="white", text=f"Ime: {alarm[1]}",
                                           text_color="black", width=250, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=1, pady=10, padx=5)
            label = customtkinter.CTkLabel(master=frame, fg_color="white", text=f"Prezime: {alarm[2]}",
                                           text_color="black", width=250, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=2, pady=10, padx=5)
            label = customtkinter.CTkLabel(master=frame, fg_color="white", text=f"Broj putovnice: {alarm[3]}",
                                           text_color="black", width=250, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=3, pady=10, padx=5)
            label = customtkinter.CTkLabel(master=frame, fg_color="lightblue", text=f"Datum referentnog broja: "
                                                                                    f"{alarm[4]}",
                                           text_color="black", width=250, font=("Helvetica", 14), anchor="w",
                                           corner_radius=30)
            label.grid(row=r, column=4, pady=10, padx=5)

            r += 1
    aw.mainloop()
