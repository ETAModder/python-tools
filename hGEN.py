import hashlib
import base64
import os
import tkinter as tk
from tkinter import messagebox

def generate_salt():
    """Generate a random salt."""
    return base64.b64encode(os.urandom(16)).decode()

def hash_text(text, algorithm, use_salt):
    """Hash text using the specified algorithm and optional salt."""
    salt = generate_salt() if use_salt else ""
    hash_function = hashlib.new(algorithm)
    hash_function.update((salt + text).encode())
    return salt, hash_function.hexdigest()

def encode_text(text):
    """Encode text using base64."""
    return base64.b64encode(text.encode()).decode()

def decode_text(encoded_text):
    """Decode base64 encoded text."""
    try:
        return base64.b64decode(encoded_text.encode()).decode()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return ""

def process_text():
    """Process the input text based on the selected option."""
    input_text = text_input.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showerror("Error", "Input text cannot be empty!")
        return

    use_salt = salt_option.get()
    selected_algo = selected_option.get()
    
    if selected_algo in hash_algorithms:
        salt, output_text = hash_text(input_text, selected_algo, use_salt)
        output_text = f"Salt: {salt}\nHash: {output_text}" if use_salt else f"Hash: {output_text}"
    elif selected_algo == "Encode":
        output_text = encode_text(input_text)
    elif selected_algo == "Decode":
        output_text = decode_text(input_text)
    else:
        output_text = ""
    
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, output_text)

def copy_to_clipboard():
    """Copy the output text to the clipboard."""
    root.clipboard_clear()
    root.clipboard_append(text_output.get("1.0", tk.END).strip())
    messagebox.showinfo("Copied", "Output text copied to clipboard!")

# Create the main window
root = tk.Tk()
root.title("hGEN | i love hashlib | v2")

# Input Text
tk.Label(root, text="INPUT:").pack()
text_input = tk.Text(root, height=5, width=50)
text_input.pack()

# Options for Hashing/Encoding/Decoding
options_frame = tk.Frame(root)
options_frame.pack()

# Get all available hashing algorithms from hashlib
hash_algorithms = sorted(hashlib.algorithms_available)
selected_option = tk.StringVar(value=hash_algorithms[0])

# Create radio buttons for each algorithm in a grid layout
row = 0
col = 0
for algo in hash_algorithms:
    if col >= 4:
        col = 0
        row += 1
    tk.Radiobutton(options_frame, text=f"{algo.upper()}", variable=selected_option, value=algo).grid(row=row, column=col, padx=5, pady=5, sticky='w')
    col += 1

# Encode and Decode options
tk.Radiobutton(options_frame, text="ENCODE (base64)", variable=selected_option, value="Encode").grid(row=row+1, column=0, padx=5, pady=5, sticky='w')
tk.Radiobutton(options_frame, text="DECODE (base64)", variable=selected_option, value="Decode").grid(row=row+1, column=1, padx=5, pady=5, sticky='w')

# Option to use salt
salt_option = tk.BooleanVar()
tk.Checkbutton(options_frame, text="SALTING", variable=salt_option).grid(row=row+1, column=2, padx=5, pady=5, sticky='w')

# Process Button
tk.Button(root, text="PROCESS", command=process_text).pack()

# Output Text
tk.Label(root, text="OUTPUT:").pack()
text_output = tk.Text(root, height=5, width=50)
text_output.pack()

# Copy to Clipboard Button
tk.Button(root, text="COPY", command=copy_to_clipboard).pack()

# Run the main loop
root.mainloop()