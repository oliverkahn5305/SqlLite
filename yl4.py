import sqlite3
from tkinter import *
from ttkbootstrap import Style
from tkinter import ttk
import math
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *



# Ühendus andmebaasiga
connection = sqlite3.connect('epood_okahn.db')
cursor = connection.cursor()

# Loome stiili kasutades ttkbootstrap'i
style = Style()
style.theme_use('darkly')

# Loome akna
root = Tk()
root.title("Andmete kuvamine")
root.geometry("800x600")

# Funktsioon kõigi andmete kuvamiseks
def show_all_data():
    # Kustutame eelmised andmed tabelist
    for row in table.get_children():
        table.delete(row)
    # Küsime andmed andmebaasist
    cursor.execute("SELECT * FROM okahn")
    rows = cursor.fetchall()
    # Kuvame andmed tabelis
    for row in rows:
        table.insert("", END, values=row)

# Loome tabeli
table = ttk.Treeview(root)
table['columns'] = ('id', 'first_name', 'last_name', 'email', 'car_make', 'car_model', 'car_year', 'car_price')

# Määratleme veeru päised
table.column('#0', width=0, stretch=NO)
table.column('id', anchor=CENTER, width=50)
table.column('first_name', anchor=W, width=100)
table.column('last_name', anchor=W, width=100)
table.column('email', anchor=W, width=200)
table.column('car_make', anchor=W, width=100)
table.column('car_model', anchor=W, width=100)
table.column('car_year', anchor=CENTER, width=50)
table.column('car_price', anchor=E, width=100)

table.heading('#0', text='', anchor=CENTER)
table.heading('id', text='ID', anchor=CENTER)
table.heading('first_name', text='Eesnimi', anchor=W)
table.heading('last_name', text='Perenimi', anchor=W)
table.heading('email', text='E-mail', anchor=W)
table.heading('car_make', text='Auto mark', anchor=W)
table.heading('car_model', text='Auto mudel', anchor=W)
table.heading('car_year', text='Auto aasta', anchor=CENTER)
table.heading('car_price', text='Auto hind', anchor=E)

# Kuvame tabeli
table.pack(fill=BOTH, expand=YES)

# Loome nupu kõigi andmete kuvamiseks
show_all_data_button = ttk.Button(root, text="Kuva kõik andmed", command=show_all_data)
show_all_data_button.pack()

# Funktsioon andmete kuvamiseks valitud lehel
def show_data_page(page_number, page_size):
    # Kustutame eelmised andmed tabelist
    for row in table.get_children():
        table.delete(row)
    # Küsime andmed andmebaasist
    offset = (page_number - 1) * page_size
    cursor.execute("SELECT * FROM okahn LIMIT ? OFFSET ?", (page_size, offset))
    rows = cursor.fetchall()
    # Kuvame andmed tabelis
    for row in rows:
        table.insert("", END, values=row)

# Funktsioon lehekülgede loomiseks ja kuvamiseks
def show_paged_data(page_size):
    # Arvutame lehekülgede arvu
    cursor.execute("SELECT COUNT(*) FROM okahn")
    count = cursor.fetchone()[0]
    num_pages = math.ceil(count / page_size)
    # Kustutame eelmised andmed tabelist
    for row in table.get_children():
        table.delete(row)
    # Kuvame andmed esimesel lehel
    show_data_page(1, page_size)
    # Funktsioon lehekülgede vahetamiseks
    def change_page(event):
        page_number = int(event.widget.cget("text"))
        show_data_page(page_number, page_size)
    # Loome lehekülgede valiku
    page_frame = Frame(root)
    page_frame.pack(side=BOTTOM)
    for i in range(1, num_pages+1):
        page_button = Button(page_frame, text=str(i), width=2)
        page_button.pack(side=LEFT)
        page_button.bind("<Button-1>", change_page)

# Kuvame andmed lehekülgedena
show_paged_data(5)

# Funktsioon andmete otsimiseks
def search_data():
    # Kustutame eelmised andmed tabelist
    for row in table.get_children():
        table.delete(row)
    # Küsime otsitavad andmed andmebaasist
    search_term = search_entry.get()
    cursor.execute("SELECT * FROM okahn WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ? OR car_make LIKE ? OR car_model LIKE ? OR car_year LIKE ? OR car_price LIKE ?", ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
    rows = cursor.fetchall()
    # Kuvame otsitavad andmed tabelis
    for row in rows:
        table.insert("", END, values=row)

# Loome otsinguvälja ja otsimisnupu
search_frame = Frame(root)
search_frame.pack(side=TOP, padx=10, pady=10)
search_label = Label(search_frame, text="Otsi:")
search_label.pack(side=LEFT)
search_entry = Entry(search_frame)
search_entry.pack(side=LEFT)
search_button = Button(search_frame, text="Otsi", command=search_data)
search_button.pack(side=LEFT)

def add_data():
    # Loeme andmed väljadest
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()
    car_make = car_make_entry.get()
    car_model = car_model_entry.get()
    car_year = car_year_entry.get()
    car_price = car_price_entry.get()

    # Lisame andmed andmebaasi
    cursor.execute("INSERT INTO okahn (first_name, last_name, email, car_make, car_model, car_year, car_price) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (first_name, last_name, email, car_make, car_model, car_year, car_price))
    connection.commit()

    # Kuvame kõik andmed tabelis
    show_all_data()

# Loome väljad andmete sisestamiseks
first_name_label = ttk.Label(root, text="Eesnimi")
first_name_label.pack()
first_name_entry = ttk.Entry(root)
first_name_entry.pack()

last_name_label = ttk.Label(root, text="Perenimi")
last_name_label.pack()
last_name_entry = ttk.Entry(root)
last_name_entry.pack()

email_label = ttk.Label(root, text="E-mail")
email_label.pack()
email_entry = ttk.Entry(root)
email_entry.pack()

car_make_label = ttk.Label(root, text="Auto mark")
car_make_label.pack()
car_make_entry = ttk.Entry(root)
car_make_entry.pack()

car_model_label = ttk.Label(root, text="Auto mudel")
car_model_label.pack()
car_model_entry = ttk.Entry(root)
car_model_entry.pack()

car_year_label = ttk.Label(root, text="Auto aasta")
car_year_label.pack()
car_year_entry = ttk.Entry(root)
car_year_entry.pack()

car_price_label = ttk.Label(root, text="Auto hind")
car_price_label.pack()
car_price_entry = ttk.Entry(root)
car_price_entry.pack()

# Loome nupu andmete lisamiseks
add_data_button = ttk.Button(root, text="Lisa andmed", command=add_data)
add_data_button.pack()
    



root.mainloop()

# Sulgeme ühenduse andmebaasiga
connection.close()