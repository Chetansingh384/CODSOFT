# our code start here .....
import random
import string
import tkinter as tk
from tkinter import messagebox
import pyperclip

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_and_display_password():
    try:
        length = int(length_entry.get())
        num_passwords = int(num_passwords_entry.get())  
        if length <= 0 or num_passwords <= 0:
            messagebox.showerror("Error", "Please enter a positive length and number of passwords.")
            return
        passwords = [generate_password(length) for _ in range(num_passwords)] 
        password_display.config(state=tk.NORMAL)
        password_display.delete(1.0, tk.END)
        password_display.insert(tk.END, "\n".join(passwords))  
        password_display.config(state=tk.DISABLED)
        copy_button.config(state=tk.NORMAL)
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter valid integers.")

def copy_password():
    password = password_display.get(1.0, tk.END).strip()
    pyperclip.copy(password)
    messagebox.showinfo("Success", "Password(s) copied to clipboard!")


root = tk.Tk()
root.title("Password Generator")
root.configure(bg="#1f1f1f")

# Create and place widgets
length_label = tk.Label(root, text="Password Length:", bg="#1f1f1f", fg="white", font=("Courier", 12))
length_label.grid(row=0, column=0, padx=10, pady=5)

length_entry = tk.Entry(root, width=10, font=("Courier", 12))
length_entry.grid(row=0, column=1, padx=10, pady=5)

num_passwords_label = tk.Label(root, text="Number of Passwords:", bg="#1f1f1f", fg="white", font=("Courier", 12))
num_passwords_label.grid(row=1, column=0, padx=10, pady=5)

num_passwords_entry = tk.Entry(root, width=10, font=("Courier", 12))
num_passwords_entry.grid(row=1, column=1, padx=10, pady=5)

generate_button = tk.Button(root, text="Generate Password", command=generate_and_display_password, bg="#0f0", fg="white", font=("Courier", 12))
generate_button.grid(row=2, column=0, columnspan=2, pady=10)

password_display = tk.Text(root, height=5, width=30, state=tk.DISABLED, bg="#1f1f1f", fg="white", font=("Courier", 12))
password_display.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

copy_button = tk.Button(root, text="Copy Password", command=copy_password, state=tk.DISABLED, bg="#00f", fg="white", font=("Courier", 12))
copy_button.grid(row=4, column=0, columnspan=2, pady=5)

# Start the GUI event loop
root.mainloop()
