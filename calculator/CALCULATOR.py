#code start from here....
import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import math

def click(event):
    global expression
    text = event.widget.cget("text")
    if text == "=":
        try:
            result = str(eval(expression))
            input_var.set(result)
            history.append(expression + " = " + result)
            expression = result
        except Exception as e:
            input_var.set("Error")
            expression = ""
    elif text == "C":
        expression = ""
        input_var.set(expression)
    else:
        expression += text
        input_var.set(expression)

def toggle_theme():
    global dark_theme
    dark_theme = not dark_theme
    apply_theme()

def apply_theme():
    bg_color = "#2e2e2e" if dark_theme else "white"
    fg_color = "white" if dark_theme else "black"
    btn_bg_color = "#555555" if dark_theme else "#b0e0e6"
    special_btn_bg_color = "#444444" if dark_theme else "#87cefa"

    root.config(bg=bg_color)
    display.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
    for button in buttons_list:
        button.config(bg=btn_bg_color, fg=fg_color)
    theme_button.config(image=moon_img if dark_theme else sun_img, bg=special_btn_bg_color)
    toggle_keyboard_button.config(bg=special_btn_bg_color, fg=fg_color)
    history_button.config(bg=special_btn_bg_color, fg=fg_color)

def toggle_keyboard():
    global scientific_mode
    scientific_mode = not scientific_mode
    update_buttons()

def update_buttons():
    for button in buttons_list:
        button.grid_forget()
    buttons_list.clear()

    buttons = scientific_buttons if scientific_mode else basic_buttons
    row_val = 1
    col_val = 0
    for button in buttons:
        btn = tk.Button(root, text=button, padx=20, pady=20, font=tkfont.Font(size=15), bg="#b0e0e6")
        btn.grid(row=row_val, column=col_val, sticky="nsew")
        btn.bind("<Button-1>", click)
        buttons_list.append(btn)
        col_val += 1
        if col_val > 4:
            col_val = 0
            row_val += 1

    theme_button.grid(row=row_val, column=0, columnspan=2, sticky="nsew")
    toggle_keyboard_button.grid(row=row_val, column=2, columnspan=2, sticky="nsew")
    history_button.grid(row=row_val, column=4, sticky="nsew")

    apply_theme()

def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Calculation History")
    history_window.geometry("400x400")
    history_text = tk.Text(history_window, font=tkfont.Font(size=15))
    history_text.pack(expand=True, fill='both')
    history_text.insert('end', "\n".join(history))
    history_text.config(state='disabled')

root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("400x600")

expression = ""
input_var = tk.StringVar()
dark_theme = False
scientific_mode = False
history = []


display = tk.Entry(root, textvar=input_var, font=tkfont.Font(size=20), bd=10, insertwidth=4, width=14, borderwidth=4)
display.grid(row=0, column=0, columnspan=5, ipadx=8, ipady=8)

basic_buttons = [
    '7', '8', '9', '/', 'sqrt',
    '4', '5', '6', '*', 'pow',
    '1', '2', '3', '-', 'log',
    '0', '.', '=', '+', 'C'
]

scientific_buttons = [
    'sin', 'cos', 'tan', 'exp', 'sqrt',
    'asin', 'acos', 'atan', 'pi', 'pow',
    'sinh', 'cosh', 'tanh', 'e', 'log',
    '7', '8', '9', '/', 'C',
    '4', '5', '6', '*', '-',
    '1', '2', '3', '+', '=',
    '0', '.'
]

buttons_list = []

moon_img = Image.open("moon.jpg")
moon_img = moon_img.resize((40, 40), Image.LANCZOS)
moon_img = ImageTk.PhotoImage(moon_img)

sun_img = Image.open("sun.jpg")
sun_img = sun_img.resize((40, 40), Image.LANCZOS)
sun_img = ImageTk.PhotoImage(sun_img)

theme_button = tk.Button(root, command=toggle_theme, padx=20, pady=20, font=tkfont.Font(size=15))

toggle_keyboard_button = tk.Button(root, text="Toggle Keyboard", command=toggle_keyboard, padx=20, pady=20, font=tkfont.Font(size=15))

history_button = tk.Button(root, text="History", command=show_history, padx=20, pady=20, font=tkfont.Font(size=15))

update_buttons()

for i in range(5):
    root.grid_columnconfigure(i, weight=1)
for i in range(8):
    root.grid_rowconfigure(i, weight=1)

# Apply initial theme
apply_theme()

# Run the application
root.mainloop()
