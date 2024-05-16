import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
from PIL import Image, ImageTk

class Task:
    def __init__(self, description, date_time, completed=False):
        self.description = description
        self.date_time = date_time
        self.completed = completed

class ToDoListApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List App")

        # Load background image
        image = Image.open("bg3.png")
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        image = image.resize((screen_width, screen_height), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(image)

        # Create a canvas for the background image
        self.canvas = tk.Canvas(master, width=screen_width, height=screen_height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        # Initialize tasks attribute
        self.tasks = []
        self.deleted_tasks = []

        # Main Heading
        self.heading_label = tk.Label(master, text="To-Do List", fg="black", font=("Helvetica", 18))
        self.heading_label.place(relx=0.5, rely=0.1, anchor="center")

        # Input Area
        self.input_frame = tk.Frame(master, bg="black")
        self.input_frame.place(relx=0.5, rely=0.2, anchor="center")

        self.task_input = tk.Entry(self.input_frame, width=30, bg="gray", fg="black")
        self.task_input.grid(row=0, column=0, padx=(5, 3), pady=5)

        self.add_button = tk.Button(self.input_frame, text="Add Task", command=self.add_task, bg="green", padx=0, pady=0)
        self.add_button.grid(row=0, column=1, padx=(2, 4), pady=5)

        # Task Listbox
        self.task_listbox = tk.Listbox(master, width=50,  selectbackground="black", bg="gray")
        self.task_listbox.place(relx=0.5, rely=0.35, anchor="center")

        # Button Area
        self.button_frame = tk.Frame(master, bg="black")
        self.button_frame.place(relx=0.5, rely=0.9, anchor="center")

        self.complete_button = tk.Button(self.button_frame, text="Mark as Complete", command=self.mark_task_complete, bg="lightgreen", padx=10, pady=5)
        self.complete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_task, bg="salmon", padx=10, pady=5)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.update_button = tk.Button(self.button_frame, text="Update Task", command=self.update_task, bg="lightblue", padx=10, pady=5)
        self.update_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = tk.Button(self.button_frame, text="Save and Quit", command=self.save_tasks_quit, bg="lightcoral", padx=10, pady=5)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        # History Button
        self.history_button = tk.Button(self.button_frame, text="History", command=self.show_history, bg="lightgray", padx=10, pady=5)
        self.history_button.pack(side=tk.LEFT, padx=5, pady=5)

    def add_task(self):
        description = self.task_input.get()
        if description:
            now = datetime.now()
            date_time = now.strftime("%d-%b-%Y")
            self.tasks.append(Task(description, date_time))
            self.task_input.delete(0, tk.END)
            self.load_tasks_to_listbox()

    def load_tasks_to_listbox(self):
        self.task_listbox.delete(0, tk.END)
        visible_tasks = [task for task in self.tasks if task not in self.deleted_tasks]
        for i, task in enumerate(visible_tasks, start=1):
            if task.completed:
                status = "\u2713"
                color = "green"
            else:
                status = " "
                color = "white"
            self.task_listbox.insert(tk.END, f"{i}. {status} {task.description}   ({task.date_time})")
            self.task_listbox.itemconfig(i - 1, {'fg': color})

    def mark_task_complete(self):
        try:
            index = int(self.task_listbox.curselection()[0])
            self.tasks[index].completed = True
            self.load_tasks_to_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task.")

    def delete_task(self):
        try:
            index = int(self.task_listbox.curselection()[0])
            deleted_task = self.tasks[index]
            deleted_task.completed = True  # Mark as deleted
            self.deleted_tasks.append(deleted_task)
            self.load_tasks_to_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task.")

    def update_task(self):
        try:
            index = int(self.task_listbox.curselection()[0])
            new_description = self.task_input.get()
            if new_description:
                self.tasks[index].description = new_description
                self.task_input.delete(0, tk.END)
                self.load_tasks_to_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task.")

    def save_tasks_quit(self):
        self.save_tasks('tasks.json')
        self.master.quit()

    def save_tasks(self, filename):
        with open(filename, 'w') as f:
            json.dump([{'description': task.description, 'date_time': task.date_time, 'completed': task.completed} for task in self.tasks], f)

    def load_tasks(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.tasks = [Task(task['description'], task['date_time'], task['completed']) for task in data]
        except FileNotFoundError:
            self.tasks = []

    def show_history(self):
        history_window = tk.Toplevel(self.master)
        history_window.title("Task History")

        history_listbox = tk.Listbox(history_window, width=50)
        history_listbox.pack(pady=10)

        for i, task in enumerate(self.tasks, start=1):
            if task in self.deleted_tasks:
                if task.completed:
                    status = "Completed but Deleted"
                else:
                    status = "Deleted"
            elif task.completed:
                status = "Completed"
            else:
                status = "Not Completed"
            history_listbox.insert(tk.END, f"{i}. {task.description}   ({task.date_time}) - {status}")

def main():
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
