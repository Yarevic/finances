import tkinter as tk
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk # Bibliothek für die Arbeit mit Bildern

class Main(tk.Frame):
    def __init__ (self, root):
        super().__init__(root) #берем root из фрейма, root основа создания фрейма
        self.init_main()
        self.db =  db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg="white", bd=5) # bd = border
        toolbar.pack(side=tk.TOP, fill=tk.X) #erstellt die Toolbar oben, fill=tk.X bildet die Horiyontale Linie x, auf der die Elemente angeordnet werden




        self.add_img = tk.PhotoImage(file="add.gif")
        btn_add = tk.Button(toolbar, text="Add task", bg="white", activebackground="red", compound=tk.BOTTOM, image=self.add_img, width="100", command=self.open_popup_add)
        btn_add.pack(side=tk.LEFT)

        self.edit_img = tk.PhotoImage(file="edit.gif")
        btn_edit = tk.Button(toolbar, text="Edit task", bg="white", activebackground="red", compound=tk.BOTTOM, image=self.edit_img, width="100")
        btn_edit.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file="refresh.gif")
        btn_refresh = tk.Button(toolbar, text="Refresh task", bg="white", activebackground="red", compound=tk.BOTTOM, image=self.refresh_img, width="100")
        btn_refresh.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file="search.gif")
        btn_search = tk.Button(toolbar, text="Search task", bg="white", activebackground="red", compound=tk.BOTTOM, image=self.search_img, width="100")
        btn_search.pack(side=tk.LEFT)    
  
        self.delete_img = tk.PhotoImage(file="delete.gif")
        btn_delete = tk.Button(toolbar, text="Delete task", bg="white", activebackground="red", compound=tk.BOTTOM, image=self.delete_img, width="100")
        btn_delete.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=("ID", "date", "description", "transactions", "category", "sum"), height=20, show="headings")
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("date", width=100, anchor=tk.CENTER)
        self.tree.column("description", width=400, anchor=tk.W)
        self.tree.column("transactions", width=70, anchor=tk.W)
        self.tree.column("category", width=70, anchor=tk.W)
        self.tree.column("sum", width=70, anchor=tk.E)

        self.tree.heading("ID", text="ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("description", text="Description")
        self.tree.heading("transactions", text="Transactions")
        self.tree.heading("category", text="Category")
        self.tree.heading("sum", text="Sum")

        self.tree.pack(side=tk.LEFT)


        # Scrollbar
        scrollbar = tk.Scrollbar(self, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)

    def open_popup_add(self):
        Child()
    def record(self, date, description, transactions, category, summ): #die Namen der Paramter sind nur Labels. Wir koennen hier auch a,b,c,d... schreiben
        self.db.insert_data(date, description, transactions, category, summ)
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM todo''') # Wir erhalten die Daten durch die Methode c (Cursor)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.c.fetchall()] 

class Child(tk.Toplevel): # Toplevel: Master of popup windows
    def __init__(self):
        super().__init__(window)
        self.init_child()
        self.view=app

    def init_child(self):
        self.geometry("600x400")
        self.title("Add Operation")
        self.configure(bg="grey")

        operation_name_label = tk.Label(self, bg="grey", fg="black", text = "Bezeichnung", padx = 1, pady = 5)
        operation_name_label.grid(row=0, column=0, sticky="E")
        self.operation_entry = tk.Entry(self, width=75)
        self.operation_entry.grid(row=0, column=1, sticky="W")
        inout_name_label = tk.Label(self, bg="grey", fg="black", text = "Eingang/Ausgang", padx = 1, pady = 5)
        inout_name_label.grid(row=1, column=0, sticky="E")
        self.inout_combo = ttk.Combobox(self, values=['Eingang', 'Ausgang'])
        self.inout_combo.current(1)
        self.inout_combo.grid(row=1, column=1, sticky="W")
        category_label = tk.Label(self, bg="grey", fg="black", text = "Kategorie", padx = 1, pady = 5)
        category_label.grid(row=2, column=0, sticky="E")
        self.category_combo = ttk.Combobox(self, values=['Miete', 'Versicherung', 'Lebensmittel'])
        self.category_combo.grid(row=2, column=1, sticky="W")
        sum_name_label = tk.Label(self, bg="grey", fg="black", text = "Summe", padx = 1, pady = 5)
        sum_name_label.grid(row=3, column=0, sticky="E")
        self.sum_entry = tk.Entry(self, width=10)
        self.sum_entry.grid(row=3, column=1, sticky="W")
        date_label = tk.Label(self, bg="grey", fg="black", text = "Datum (DD.MM.YY)", padx = 1, pady = 5)
        date_label.grid(row=4, column=0, sticky="E")
        self.date_entry = tk.Entry(self, width=8)
        self.date_entry.grid(row=4, column=1, sticky="W")
        self.add_button = tk.Button(self, bg="orange", activebackground="red", fg="black", font="Arial 15", text="Speichern", padx=1, pady=5)
        self.add_button.place(x=100, y=250)
        self.add_button.bind("<Button-1>", lambda event: self.view.record(self.date_entry.get(), self.operation_entry.get(), self.inout_combo.get(), self.category_combo.get(), self.sum_entry.get())) #Привязываем событие кликов левой клавиша мыши к кнопке "добавить"
        
        cancel_button = tk.Button(self, bg="orange", activebackground="red", fg="black", font="Arial 15", text="Abbrechen", padx=1, pady=5, command=self.destroy)
        cancel_button.place(x=250, y=250)
        self.grab_set()
        self.add_button.destroy()

class DB:
    def __init__(self):
        self.conn = sqlite3.connect("todo.db") #Variable, die die Datenbank aufruft
        self.c = self.conn.cursor() #Wir rufen die Methode Cursor auf, mit der wir die Daten verarbeiten werden
        self.c.execute('''CREATE TABLE IF NOT EXISTS todo (id integer primary key, date text, description text, transactions text, category text, summ real)''') # integer = ganze Zahl, real = Zahl mit Komma
        self.conn.commit()

    def insert_data(self, date, description, transactions, category, summ):        
        self.c.execute('''INSERT INTO todo(date, description, transactions, category, summ) VALUES(?,?,?,?,?)''', (date, description, transactions, category, summ)) 
        # Spalten fuer die Parameter werden zuerst geschaffen, danach werden die Parameter uebergeben
        self.conn.commit() # Aendeungen werden in die DB eingetragen




if __name__ == "__main__": # Diese Konstruktion ist eine Standardbedingung in Python, die sicherstellt, dass ein Skript nur dann ausgeführt wird, wenn es direkt gestartet wird – und nicht, wenn es als Modul importiert wird.
    window = tk.Tk()
    db=DB()
    app = Main(window)
    app.pack()
    window.geometry("800x600")
    window.title("Task Manager")
    window.mainloop()
    
