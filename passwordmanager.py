import tkinter as tk
from tkinter import messagebox
import sqlite3
from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.conn = sqlite3.connect('passwords.db')
        self.create_table()
        self.setup_ui()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS passwords
                          (id INTEGER PRIMARY KEY, service TEXT, encrypted_password TEXT)''')
        self.conn.commit()

    def setup_ui(self):
        tk.Label(self.root, text="Service").grid(row=0)
        tk.Label(self.root, text="Password").grid(row=1)
        
        self.service_entry = tk.Entry(self.root)
        self.password_entry = tk.Entry(self.root)
        
        self.service_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        
        tk.Button(self.root, text='Save', command=self.save_password).grid(row=2, column=1, sticky=tk.W, pady=4)

    def save_password(self):
        service = self.service_entry.get()
        password = self.password_entry.get()
        encrypted_password = self.cipher_suite.encrypt(password.encode())
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO passwords (service, encrypted_password) VALUES (?, ?)", (service, encrypted_password))
        self.conn.commit()
        messagebox.showinfo("Info", "Password saved successfully")

root = tk.Tk()
app = PasswordManager(root)
root.mainloop()

