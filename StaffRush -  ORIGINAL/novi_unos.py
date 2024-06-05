import customtkinter
import tkinter
from database import add_user, create_database
from tkinter import messagebox as messagebox


def create_novi_unos_window():
    novi_unos_window = customtkinter.CTk()
    novi_unos_window.title("NOVI UNOS")

    # Get screen dimensions
    screen_width = novi_unos_window.winfo_screenwidth()
    screen_height = novi_unos_window.winfo_screenheight()

    # Calculate window width and height
    novi_unos_window_width = int(screen_width * 0.9)
    novi_unos_window_height = int(screen_height * 0.9)

    # Calculate window position to center it on the screen
    x_position = (screen_width - novi_unos_window_width) // 2
    y_position = (screen_height - novi_unos_window_height) // 2

    # Set window size and position
    novi_unos_window.geometry(f"{novi_unos_window_width}x{novi_unos_window_height}+{x_position}+{y_position}")

    frame3_width = int(novi_unos_window_width * 1)
    frame3_height = int(novi_unos_window_height * 1)

    frame3 = customtkinter.CTkFrame(master=novi_unos_window, width=frame3_width,
                                    height=frame3_height, corner_radius=30)
    frame3.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    entries = []

    unos_ime = customtkinter.CTkEntry(master=frame3, width=int(frame3_width * 0.6), height=40, placeholder_text='IME')
    unos_ime.place(x=int(frame3_width * 0.2), y=int(frame3_height * 0.07))
    entries.append(unos_ime)

    unos_prezime = customtkinter.CTkEntry(master=frame3, width=int(frame3_width * 0.6), height=40,
                                          placeholder_text='PREZIME')
    unos_prezime.place(x=int(frame3_width * 0.2), y=int(frame3_height * 0.14))
    entries.append(unos_prezime)

    unos_oib = customtkinter.CTkEntry(master=frame3, width=int(frame3_width * 0.6), height=40,
                                      placeholder_text='OIB')
    unos_oib.place(x=int(frame3_width * 0.2), y=int(frame3_height * 0.21))
    entries.append(unos_oib)

    unos_putovnica = customtkinter.CTkEntry(master=frame3, width=int(frame3_width * 0.6), height=40,
                                            placeholder_text="BROJ PUTOVNICE")
    unos_putovnica.place(x=int(frame3_width * 0.2), y=int(frame3_height * 0.28))
    entries.append(unos_putovnica)

    unos_id = customtkinter.CTkEntry(master=frame3, width=int(frame3_width * 0.6), height=40,
                                     placeholder_text='ID BROJ')
    unos_id.place(x=int(frame3_width * 0.2), y=int(frame3_height * 0.35))
    entries.append(unos_id)

    unos_dat_rodenja = customtkinter.CTkEntry(master=frame3, width=int(frame3_width * 0.6), height=40,
                                              placeholder_text='DATUM ROĐENJA')
    unos_dat_rodenja.place(x=int(frame3_width * 0.2), y=int(frame3_height * 0.42))
    entries.append(unos_dat_rodenja)

    unos_mjesto_rodenja = customtkinter.CTkEntry(master=frame3, width=int(frame3_width * 0.6), height=40,
                                                 placeholder_text='MJESTO ROĐENJA')
    unos_mjesto_rodenja.place(x=int(frame3_width * 0.2), y=int(frame3_height * 0.49))
    entries.append(unos_mjesto_rodenja)

    unos_prebivaliste = customtkinter.CTkEntry(master=frame3, width=int(frame3_width * 0.6), height=40,
                                               placeholder_text='ADRESA PREBIVALIŠTA')
    unos_prebivaliste.place(x=int(frame3_width * 0.2), y=int(frame3_height * 0.56))
    entries.append(unos_prebivaliste)

    unos_boraviste = customtkinter.CTkEntry(master=frame3, width=int(frame3_width * 0.6), height=40,
                                            placeholder_text='ADRESA MATIČNE ZEMLJE')
    unos_boraviste.place(x=int(frame3_width * 0.2), y=int(frame3_height * 0.63))
    entries.append(unos_boraviste)

    unos_kontakt = customtkinter.CTkEntry(master=frame3, width=int(frame3_width * 0.6), height=40,
                                          placeholder_text='KONTAKT')
    unos_kontakt.place(x=int(frame3_width * 0.2), y=int(frame3_height * 0.7))
    entries.append(unos_kontakt)

    def save_user_data():
        oib = unos_oib.get()
        if len(oib) != 11 and len(oib) != 0:
            messagebox.showerror("Error", "Netočan broj znamenki za OIB")
            novi_unos_window.lift()
        else:
            data = []
            for values in entries:
                d = values.get()
                if not d:  # Check if v is an empty string
                    d = None

                data.append(d)

            add_user(*data)
            messagebox.showinfo("", "Uspješno dodano")
            novi_unos_window.destroy()

    def save_button_command():
        create_database()
        save_user_data()

    save_button = customtkinter.CTkButton(master=frame3, width=int(frame3_width / 4), height=int(frame3_height / 8),
                                          text="SPREMI", font=("Times", 33), corner_radius=30,
                                          command=save_button_command)
    save_button.place(x=int(frame3_width / 2 - (frame3_width / 8)), y=int(frame3_height * 0.77))

    novi_unos_window.after(100, unos_ime.focus)

    novi_unos_window.mainloop()
