import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk # Bibliothek für die Arbeit mit Bildern
from datetime import datetime

class Main(tk.Frame): # Main ist ein Frame, also ein Container für andere GUI-Elemente.
    def __init__ (self, root): #root ist das Hauptfenster (Tk()).
        super().__init__(root) #берем root из фрейма, root основа создания фрейма
        self.db =  db
        self.init_main() #richtet GUI ein.
        self.view_records() # lädt Daten aus DB in die Oberfläche (Tabelle).

    def init_main(self): #Erstellt eine Toolbar mit Buttons (Add, Edit, Refresh, Search, Delete).
        toolbar = tk.Frame(bg="white", bd=5) # bd = border
        toolbar.pack(side=tk.TOP, fill=tk.X) #erstellt die Toolbar oben, fill=tk.X bildet die Horiyontale Linie x, auf der die Elemente angeordnet werden




        self.add_img = tk.PhotoImage(file="add.gif")
        btn_add = tk.Button(toolbar, text="Add task", bg="white", activebackground="red", compound=tk.BOTTOM, image=self.add_img, width="100", command=self.open_popup_add)
        btn_add.pack(side=tk.LEFT)

        self.edit_img = tk.PhotoImage(file="edit.gif")
        btn_edit = tk.Button(toolbar, text="Edit task", bg="white", activebackground="red", compound=tk.BOTTOM, image=self.edit_img, width="100", command=self.open_popup_edit)
        btn_edit.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file="refresh.gif")
        btn_refresh = tk.Button(toolbar, text="Refresh task", bg="white", activebackground="red", compound=tk.BOTTOM, image=self.refresh_img, width="100")
        btn_refresh.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file="search.gif")
        btn_search = tk.Button(toolbar, text="Search task", bg="white", activebackground="red", compound=tk.BOTTOM, image=self.search_img, width="100")
        btn_search.pack(side=tk.LEFT)    
  
        self.delete_img = tk.PhotoImage(file="delete.gif")
        btn_delete = tk.Button(toolbar, text="Delete task", bg="white", activebackground="red", compound=tk.BOTTOM, image=self.delete_img, width="100", command = self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        #Die Tabelle (ttk.Treeview) zeigt Datenbankinhalte:
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

        self.tree.pack(side=tk.TOP)

        self.search_label = tk.Label(self, bg="grey", fg="black", text = "Suche", padx = 1, pady = 5)
        self.search_entry = tk.Entry(self, width=200)
        search_button = tk.Button(self, bg="orange", activebackground="red", fg="black", font="Arial 15", text="Finden", padx=1, pady=5)
        self.search_label.pack(side=tk.BOTTOM)
        self.search_entry.pack(side=tk.BOTTOM)
        search_button.pack(side=tk.BOTTOM)
        search_button.bind("<Button-1>", lambda event: self.search_records(self.search_entry.get()))


        # Scrollbar
        scrollbar = tk.Scrollbar(self, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)

    def update_record(self, date, description, transactions, category, summ):
        # Diese Methode aktualisiert einen bestehenden Datensatz (eine Zeile) in der SQLite-Datenbanktabelle todo. Sie basiert auf dem
        # aktuell ausgewählten Eintrag in der GUI-Tabelle (self.tree), und ersetzt dessen Werte mit den neuen, übergebenen Parametern.
        self.db.c.execute('''UPDATE todo SET date=?, description=?, transactions=?, category=?, summ=? WHERE ID=?''', (date, description, transactions, category, summ, self.tree.set(self.tree.selection()[0], "#1")))
        # Das ist ein parameterisiertes Statement – das schützt vor SQL-Injection. Die Fragezeichen ? werden durch die folgenden Werte ersetzt (date...).
        # self.tree.set(self.tree.selection()[0], "#1") - das ist die ID des aktuell ausgewählten Eintrags in der GUI-Tabelle (Treeview)
        # self.tree.selection() gibt eine Liste von ausgewählten Einträgen zurück. [0] nimmt das erste ausgewählte Element.
        # self.tree.set(item, "#1") gibt den Wert in der ersten Spalte (Spalte mit der ID) dieses Elements zurück.
        self.db.conn.commit()
        self.view_records()
        

    def open_popup_add(self):
        Child()
    def record(self, date, description, transactions, category, summ): #die Namen der Paramter sind nur Labels. Wir koennen hier auch a,b,c,d... schreiben
        if len(description.strip()) <3:
            # Messagebox ist ein Element von tk und hat diverse Methoden an Board, z.B. showerror.
            messagebox.showerror("Fehlermeldung", "Die Beschreibung muss mind. 3 Zeichen lang sein!")
        elif not summ.strip():
            messagebox.showerror("Fehlermeldung", "Du musst eine Summe eintragen!")
        elif not date.strip():
            messagebox.showerror("Fehlermeldung", "Du musst ein Datum eintragen!")
            
        self.db.insert_data(date, description, transactions, category, summ)
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM todo''') # Wir erhalten die Daten durch die Methode c (Cursor)
        [self.tree.delete(i) for i in self.tree.get_children()] # Entfernen von Daten aus der Ansicht. i wird nicht im Code definiert und wird automatisch auf 0 gesetzt. In jedem Zyklus wird dann der Wert +1 gesetzt
        [self.tree.insert("", "end", values=row) for row in self.db.c.fetchall()]

    def open_popup_edit(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Keine Auswahl", "Bitte wähle einen Eintrag aus.")
            return

        values = self.tree.item(selected[0], 'values')  # Tuple: (id, date, description, transactions, category, sum)
        ChildEdit(self, values)

    def search_records(self, description):
        description = ("%" + description + "%",) #Leerzeichen werden ignoriert
        self.db.c.execute('''SELECT * FROM todo WHERE description LIKE ?''', description) #WHERE description - Bezeichnung der Spalte, description - Variable fuer die Beschreibung
        [self.tree.delete(i) for i in self.tree.get_children()] # Entfernen von Daten aus der Ansicht. i wird nicht im Code definiert und wird automatisch auf 0 gesetzt. In jedem Zyklus wird dann der Wert +1 gesetzt
        [self.tree.insert("", "end", values=row) for row in self.db.c.fetchall()] # fetchall: Show all elements from execute method from line 116

    def delete_records(self):
        chosen_element = self.tree.selection()
        if not chosen_element:
            messagebox.showwarning("Keine Auswahl", "Bitte wähle einen Eintrag aus.")
            return
        items = "\n".join([self.tree.set(item,"#3") for item in chosen_element[:3]]) # \n Zeilenumbruch, join vereinigt Zeilen, #3 ist die description
        if len(chosen_element) > 3:
            items = items + f"\n ...und {len(chosen_element)- 3} Elemente"
        complete = messagebox.askyesno("Bestätige die Löschung", f"Willst du wirklich die folgenden Elemente löschen? \n{items}",icon="warning")
        if complete: #Eine Konstruktion, die genutzt wird, sobald complete true zurueckgibt
            for deletion in self.tree.selection():
                self.db.c.execute('''DELETE FROM todo WHERE ID=?''', (self.tree.set(deletion, "#1"),))
                self.db.conn.commit()
                self.view_records()           

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

        current_data = datetime.now().strftime("%d.%m.%y") # Methode strftime() wird von der Bibliothek datetime zur Verfuegung gestellt
        
        
        self.date_entry = tk.Entry(self, width=8)
        self.date_entry.grid(row=4, column=1, sticky="W")
        self.date_entry.insert(0, current_data) #The insert method is a tkinter method. 0 is defining the insertion into first position, current_data is the variable
        
        self.add_button = tk.Button(self, bg="orange", activebackground="red", fg="black", font="Arial 15", text="Speichern", padx=1, pady=5)
        self.add_button.place(x=100, y=250)
        self.add_button.bind("<Button-1>", lambda event: self.view.record(self.date_entry.get(), self.operation_entry.get(), self.inout_combo.get(), self.category_combo.get(), self.sum_entry.get())) #Привязываем событие кликов левой клавиша мыши к кнопке "добавить"
            
        cancel_button = tk.Button(self, bg="orange", activebackground="red", fg="black", font="Arial 15", text="Abbrechen", padx=1, pady=5, command=self.destroy)
        cancel_button.place(x=250, y=250)
        self.grab_set()

class ChildEdit(tk.Toplevel):
    def __init__(self, parent, values):
        super().__init__(parent)
        self.parent = parent
        self.record_id = values[0]  # ID speichern für UPDATE später

        self.title("Datensatz bearbeiten")
        self.geometry("600x400")
        self.configure(bg="grey")

        # Felder mit Werten befüllen
        tk.Label(self, text="Bezeichnung", bg="grey").grid(row=0, column=0, sticky="e")
        self.operation_entry = tk.Entry(self, width=75)
        self.operation_entry.insert(0, values[2])
        self.operation_entry.grid(row=0, column=1)

        tk.Label(self, text="Eingang/Ausgang", bg="grey").grid(row=1, column=0, sticky="e")
        self.inout_combo = ttk.Combobox(self, values=['Eingang', 'Ausgang'])
        self.inout_combo.set(values[3])
        self.inout_combo.grid(row=1, column=1)

        tk.Label(self, text="Kategorie", bg="grey").grid(row=2, column=0, sticky="e")
        self.category_combo = ttk.Combobox(self, values=['Miete', 'Versicherung', 'Lebensmittel'])
        self.category_combo.set(values[4])
        self.category_combo.grid(row=2, column=1)

        tk.Label(self, text="Summe", bg="grey").grid(row=3, column=0, sticky="e")
        self.sum_entry = tk.Entry(self, width=10)
        self.sum_entry.insert(0, values[5])
        self.sum_entry.grid(row=3, column=1)

        tk.Label(self, text="Datum (DD.MM.YY)", bg="grey").grid(row=4, column=0, sticky="e")
        self.date_entry = tk.Entry(self, width=10)
        self.date_entry.insert(0, values[1])
        self.date_entry.grid(row=4, column=1)

        # Änderung speichern
        save_btn = tk.Button(self, text="Änderung speichern", bg="orange", command=self.save_changes)
        save_btn.place(x=100, y=300)

        cancel_btn = tk.Button(self, text="Abbrechen", bg="orange", command=self.destroy)
        cancel_btn.place(x=250, y=300)

        self.grab_set()

    def save_changes(self):
        date = self.date_entry.get()
        description = self.operation_entry.get()
        transaction = self.inout_combo.get()
        category = self.category_combo.get()
        summ = self.sum_entry.get()

        if len(description.strip()) < 3:
            messagebox.showerror("Fehler", "Beschreibung zu kurz.")
            return
        if not summ.strip():
            messagebox.showerror("Fehler", "Summe fehlt.")
            return

        self.parent.db.c.execute('''UPDATE todo SET date=?, description=?, transactions=?, category=?, summ=? WHERE ID=?''',
                                 (date, description, transaction, category, summ, self.record_id))
        self.parent.db.conn.commit()
        self.parent.view_records()
        self.destroy()


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
    
