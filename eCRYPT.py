import tkinter as tk
from tkinter import filedialog, simpledialog, scrolledtext, messagebox
import os
import hashlib
import secrets

class EncryptorApp:
    def __init__(self, master):
        self.master = master
        self.master.config(bg='#50AB65')
        self.master.geometry("500x400")
        master.title("eCRYPT | #EtacryptFiles! | v1")

        self.label = tk.Label(master, text="CHOOSE A FILE", fg="#1E6934", bg='#50B867', activebackground='#50B867', font="LanaPixel")
        self.label.pack(pady=10)

        self.file_content = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=10, fg="black", bg='white', font="Arial")
        self.file_content.pack(padx=10, pady=10)

        self.encrypt_button = tk.Button(master, text="ENCRYPT FILE", command=self.encrypt_file, fg="#1E6934", bg='#50B867', activebackground='#50B867', font="LanaPixel")
        self.encrypt_button.pack(pady=5)

        self.decrypt_button = tk.Button(master, text="DECRYPT FILE", command=self.decrypt_file, fg="#1E6934", bg='#50B867', activebackground='#50B867', font="LanaPixel")
        self.decrypt_button.pack(pady=5)

        self.status = tk.Label(master, text="", fg="#1E6934", bg="#50AB65", font=("LanaPixel", 12))
        self.status.pack(pady=5)

    def read_file(self, file_path):
        with open(file_path, "rb") as file:
            return file.read()

    def write_file(self, file_path, data):
        with open(file_path, "wb") as file:
            file.write(data)

    def display_file(self, data):
        self.file_content.delete(1.0, tk.END)
        self.file_content.insert(tk.END, data.decode(errors='ignore'))

    def pad_data(self, data):
        pad_len = 16 - len(data) % 16
        return data + bytes([pad_len] * pad_len)

    def unpad_data(self, data):
        pad_len = data[-1]
        return data[:-pad_len]

    def encrypt(self, data, key):
        iv = secrets.token_bytes(16)
        cipher_data = bytearray(iv)
        for i in range(0, len(data), 16):
            block = data[i:i+16]
            encrypted_block = bytes(a ^ b for a, b in zip(block, key))
            cipher_data.extend(encrypted_block)
        return cipher_data

    def decrypt(self, data, key):
        iv = data[:16]
        cipher_data = data[16:]
        decrypted_data = bytearray()
        for i in range(0, len(cipher_data), 16):
            block = cipher_data[i:i+16]
            decrypted_block = bytes(a ^ b for a, b in zip(block, key))
            decrypted_data.extend(decrypted_block)
        return decrypted_data

    def get_key(self, passphrase):
        key = hashlib.sha256(passphrase.encode()).digest()
        return key[:16]  # AES block size

    def encrypt_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            passphrase = simpledialog.askstring("INPUT", "ENTER enKEY (passphrase):", show='*')
            if passphrase:
                try:
                    file_data = self.read_file(file_path)
                    file_data = self.pad_data(file_data)
                    self.display_file(file_data)
                    key = self.get_key(passphrase)
                    encrypted_data = self.encrypt(file_data, key)
                    new_file_path = file_path + ".etacrypt"
                    self.write_file(new_file_path, encrypted_data)
                    self.status.config(text=f"ENCRYPTION SUCCESS! {new_file_path}")
                    self.display_file(encrypted_data)
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def decrypt_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Encrypted files", "*.etacrypt")])
        if file_path:
            passphrase = simpledialog.askstring("INPUT", "ENTER deKEY (passphrase):", show='*')
            if passphrase:
                try:
                    file_data = self.read_file(file_path)
                    self.display_file(file_data)
                    key = self.get_key(passphrase)
                    decrypted_data = self.decrypt(file_data, key)
                    decrypted_data = self.unpad_data(decrypted_data)
                    new_file_path = file_path.replace(".etacrypt", ".etadecrypt")
                    self.write_file(new_file_path, decrypted_data)
                    self.status.config(text=f"DECRYPTION SUCCESS! {new_file_path}")
                    self.display_file(decrypted_data)
                except Exception as e:
                    messagebox.showerror("ERR", str(e))

root = tk.Tk()
app = EncryptorApp(root)
root.mainloop()
