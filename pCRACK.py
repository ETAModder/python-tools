import tkinter as tk
import random
import time
import threading

# Define the characters to be randomized
CUSTOM_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_+=[]?"

# Function to generate a fake IPv4 address
def generate_fake_ip():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))

class PrankPasswordCracker:
    def __init__(self, root):
        self.root = root
        self.root.title("pCRACK | the extra intel | v1.7")
        self.root.config(bg='#50AB65')

        self.ip_label = tk.Label(root, text="TARGET IP:", fg="#1E6934", bg='#50B867', activebackground='#50B867', font="LanaPixel")
        self.ip_label.pack(pady=5)

        self.ip_entry = tk.Entry(root, width=50, fg="#1E6934", bg='#50B867', font="LanaPixel")
        self.ip_entry.pack(pady=10)
        self.ip_entry.insert(0, generate_fake_ip())  # Insert fake IP into the entry field

        self.db_entry = tk.Entry()

        self.refresh_button = tk.Button(root, text="GET IP FROM DATABASE", command=self.refresh_ip, fg="#1E6934", bg='#50B867', activebackground='#50B867', cursor="hand2", font="LanaPixel")
        self.refresh_button.pack(pady=5)

        self.output_area = tk.Text(root, width=60, height=10, font=("OCR A Extended", 12), bg="black", fg="lime")
        self.output_area.pack(pady=20)

        self.start_button = tk.Button(root, text="BRUTE FORCE", command=self.start_cracking, fg="#1E6934", bg='#50B867', activebackground='#50B867', cursor="hand2", font="LanaPixel")
        self.start_button.pack(pady=10)

    def refresh_ip(self):
        new_ip = generate_fake_ip()
        self.ip_entry.delete(0, tk.END)
        self.ip_entry.insert(0, new_ip)

    def start_cracking(self):
        self.start_button.config(state=tk.DISABLED)
        threading.Thread(target=self.crack_password).start()

    def crack_password(self):
        target_ip = self.ip_entry.get()
        password_length = 25
        cracked_password = ''.join(random.choice(CUSTOM_CHARS) for _ in range(password_length))

        for i in range(5000):
            fake_password = ''.join(random.choice(CUSTOM_CHARS) for _ in range(password_length))
            self.output_area.insert(tk.END, f"TARGET: {target_ip} | TRYING: {fake_password}\n")
            self.output_area.see(tk.END)
            self.root.update()
            time.sleep(0.001)

        self.output_area.insert(tk.END, f"\n]=--------------------------------------------------------=[\n")
        self.output_area.insert(tk.END, f"  ROOT PASSWD FOR {target_ip}: {cracked_password}\n")
        self.output_area.insert(tk.END, f"]=--------------------------------------------------------=[")
        self.output_area.see(tk.END)
        self.start_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = PrankPasswordCracker(root)
    root.mainloop()
