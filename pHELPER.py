import tkinter as tk
from tkinter import messagebox
import secrets
import string
import math
import hashlib

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("pHELPER | chrome passwd manager got nothin on us | v2")
        self.root.geometry("500x600")

        # Password length label and entry
        self.label = tk.Label(root, text="PASSWORD LENGTH:", font=("LanaPixel", 14))
        self.label.pack(pady=10)

        self.length_var = tk.IntVar(value=16)
        self.length_entry = tk.Entry(root, textvariable=self.length_var, width=5, font=("LanaPixel", 14))
        self.length_entry.pack(pady=10)

        # Checkbuttons for character types
        self.include_upper = tk.BooleanVar(value=True)
        self.include_lower = tk.BooleanVar(value=True)
        self.include_digits = tk.BooleanVar(value=True)
        self.include_punctuation = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)

        tk.Checkbutton(root, text="UPPERCASE", variable=self.include_upper).pack(anchor="w")
        tk.Checkbutton(root, text="LOWECASE", variable=self.include_lower).pack(anchor="w")
        tk.Checkbutton(root, text="DIGITS", variable=self.include_digits).pack(anchor="w")
        tk.Checkbutton(root, text="PUNCTUATION", variable=self.include_punctuation).pack(anchor="w")
        tk.Checkbutton(root, text="EXCLUDE O, 0, I, l", variable=self.exclude_ambiguous).pack(anchor="w")

        # Checkbutton for hashing option
        self.use_hashing = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="HASHING (SHA-512)", variable=self.use_hashing).pack(anchor="w")

        # Generate password button, copy button, and entropy label
        self.generate_button = tk.Button(root, text="GENERATE", command=self.generate_password)
        self.generate_button.pack(pady=10)

        self.copy_button = tk.Button(root, text="COPY", command=self.copy_to_clipboard, state=tk.DISABLED)
        self.copy_button.pack(pady=5)

        self.entropy_label = tk.Label(root, text="", font=("LanaPixel", 10))
        self.entropy_label.pack(pady=5)

        # Password display label
        self.password_label = tk.Label(root, text="", font=("OCR A Extended", 14), wraplength=350, bg="black", fg="lime")
        self.password_label.pack(pady=20)

    def generate_password(self):
        length = self.length_var.get()
        if length < 12:  # Increased minimum length for better security
            messagebox.showwarning("WEAK", "LENGTH SHOULD BE ATLEAST 10 CHARS")
            return

        char_set = ''
        if self.include_upper.get():
            char_set += string.ascii_uppercase
        if self.include_lower.get():
            char_set += string.ascii_lowercase
        if self.include_digits.get():
            char_set += string.digits
        if self.include_punctuation.get():
            char_set += string.punctuation

        if self.exclude_ambiguous.get():
            char_set = char_set.replace('O', '').replace('0', '').replace('I', '').replace('l', '')

        if not char_set:
            messagebox.showwarning("SELECT ATLEAST 1 TYPE", "PLEASE SELECT ATLEAST ONE CHARACTER TYPE")
            return

        # Ensure at least one of each selected character type is included
        password = []
        if self.include_upper.get():
            password.append(secrets.choice(string.ascii_uppercase))
        if self.include_lower.get():
            password.append(secrets.choice(string.ascii_lowercase))
        if self.include_digits.get():
            password.append(secrets.choice(string.digits))
        if self.include_punctuation.get():
            password.append(secrets.choice(string.punctuation))

        while len(password) < length:
            password.append(secrets.choice(char_set))

        secrets.SystemRandom().shuffle(password)
        password = ''.join(password)

        # Hash the password if the option is selected
        if self.use_hashing.get():
            hashed_password = hashlib.sha512(password.encode()).hexdigest()
            self.password_label.config(text=hashed_password)
        else:
            self.password_label.config(text=password)

        # Calculate and display entropy
        entropy = length * math.log2(len(char_set))
        self.entropy_label.config(text=f"ENTROPY: {entropy:.2f} bits")

        self.copy_button.config(state=tk.NORMAL)

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.password_label.cget("text"))
        messagebox.showinfo("COPIED", "PASSWORD COPIED TO CLIPBOARD")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
