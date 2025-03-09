import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Contact Manager")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f2f5")

        # Initialize SQLite database
        self.conn = sqlite3.connect('contacts.db')
        self.create_table()

        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill="both", expand=True)

        # Style configuration
        self.style = ttk.Style()
        self.style.configure("TLabel", background="#f0f2f5", font=("Helvetica", 11))
        self.style.configure("TButton", font=("Helvetica", 10))
        self.style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
        
        # Configure custom style for Add button
        self.style.configure("Add.TButton", background="#0000ff", 
                           foreground="black", padding=6)
        self.style.map("Add.TButton",
                      background=[('active', '#d35400')])  # Darker shade when clicked

        self.create_widgets()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS contacts
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT NOT NULL,
                         prenom TEXT NOT NULL,
                         adresse TEXT,
                         numero TEXT,
                         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        self.conn.commit()

    def create_widgets(self):
        # Title
        title = ttk.Label(self.main_frame, text="Contact Manager", 
                         font=("Helvetica", 20, "bold"), foreground="#2c3e50")
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Input fields
        fields = [
            ("Nom", "name_entry"),
            ("Prénom", "prenom_entry"),
            ("Adresse", "adresse_entry"),
            ("Numéro", "numero_entry")
        ]

        for i, (label, attr) in enumerate(fields):
            ttk.Label(self.main_frame, text=f"{label}:").grid(row=i+1, column=0, 
                                                             pady=5, padx=5, sticky="e")
            entry = ttk.Entry(self.main_frame, width=40)
            entry.grid(row=i+1, column=1, pady=5, padx=5)
            setattr(self, attr, entry)

        # Buttons frame
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

        # Modern buttons with custom style for Add button
        self.add_btn = ttk.Button(btn_frame, text="Add Contact", 
                                command=self.add_contact, style="Add.TButton")
        self.add_btn.grid(row=0, column=0, padx=5)

        self.view_btn = ttk.Button(btn_frame, text="View Contacts", 
                                 command=self.view_contacts)
        self.view_btn.grid(row=0, column=1, padx=5)

        self.delete_btn = ttk.Button(btn_frame, text="Delete Contact", 
                                   command=self.delete_contact)
        self.delete_btn.grid(row=0, column=2, padx=5)

        # Search/Delete entry
        ttk.Label(self.main_frame, text="Search Name to Delete:").grid(row=6, column=0, 
                                                                     pady=5, padx=5, sticky="e")
        self.delete_entry = ttk.Entry(self.main_frame, width=40)
        self.delete_entry.grid(row=6, column=1, pady=5, padx=5)

    def add_contact(self):
        try:
            name = self.name_entry.get()
            prenom = self.prenom_entry.get()
            adresse = self.adresse_entry.get()
            numero = self.numero_entry.get()

            if not name or not prenom:
                messagebox.showwarning("Error", "Name and Prénom are required!")
                return

            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO contacts (name, prenom, adresse, numero)
                            VALUES (?, ?, ?, ?)''', (name, prenom, adresse, numero))
            self.conn.commit()

            messagebox.showinfo("Success", "Contact added successfully!")
            self.clear_entries()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.prenom_entry.delete(0, tk.END)
        self.adresse_entry.delete(0, tk.END)
        self.numero_entry.delete(0, tk.END)

    def view_contacts(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("All Contacts")
        view_window.geometry("700x500")
        view_window.configure(bg="#f0f2f5")

        # Create Treeview
        tree = ttk.Treeview(view_window, columns=("ID", "Name", "Prénom", "Adresse", "Numéro", "Created"),
                           show="headings", height=20)
        tree.pack(padx=20, pady=20, fill="both", expand=True)

        # Configure columns
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Prénom", text="Prénom")
        tree.heading("Adresse", text="Address")
        tree.heading("Numéro", text="Phone")
        tree.heading("Created", text="Created At")

        tree.column("ID", width=50)
        tree.column("Name", width=100)
        tree.column("Prénom", width=100)
        tree.column("Adresse", width=150)
        tree.column("Numéro", width=100)
        tree.column("Created", width=150)

        # Fetch and display contacts
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

    def delete_contact(self):
        name = self.delete_entry.get()
        if not name:
            messagebox.showwarning("Error", "Please enter a name to delete!")
            return

        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE name = ?", (name,))
        
        if cursor.rowcount > 0:
            self.conn.commit()
            messagebox.showinfo("Success", "Contact deleted successfully!")
            self.delete_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Contact not found!")

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()