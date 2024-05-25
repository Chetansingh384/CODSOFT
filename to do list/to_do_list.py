import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
from PIL import Image, ImageTk
import telepot
import schedule
import time
import threading

class Task:
    def __init__(self, description, date_time, completed=False):
        self.description = description
        self.date_time = date_time
        self.completed = completed

class ToDoListApp:
    def __init__(self, master, bot, chat_id):
        self.master = master
        self.master.title("To-Do List App")

        self.bot = bot
        self.chat_id = chat_id

        image = Image.open("bg5.jpg")
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        image = image.resize((screen_width, screen_height), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(image)

        self.canvas = tk.Canvas(master, width=screen_width, height=screen_height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        self.tasks = []
        self.deleted_tasks = []
        self.points = 0

        self.heading_label = tk.Label(master, text="To-Do List", fg="blue", font=("Comic Sans MS", 30))
        self.heading_label.place(relx=0.5, rely=0.1, anchor="center")

        self.points_label = tk.Label(master, text=f"Points: {self.points}", fg="black", font=("Helvetica", 14))
        self.points_label.place(relx=0.9, rely=0.1, anchor="center")

        self.input_frame = tk.Frame(master, bg="black")
        self.input_frame.place(relx=0.5, rely=0.2, anchor="center")

        self.task_input = tk.Entry(self.input_frame, width=30, bg="gray", fg="black", font=("arial", 16))
        self.task_input.grid(row=0, column=0, padx=(5, 3), pady=5)

        self.add_button = tk.Button(self.input_frame, text="Add Task", command=self.add_task, bg="green", padx=0, pady=0, font=("arial", 13))
        self.add_button.grid(row=0, column=1, padx=(2, 4), pady=5)

        self.task_listbox = tk.Listbox(master, width=35, selectbackground="red", bg="peru", font=("arial", 12))
        self.task_listbox.place(relx=0.5, rely=0.35, anchor="center")

        self.reminder_frame = tk.Frame(master, bg="peru", bd=2, relief="sunken")
        self.reminder_frame.place(relx=0.15, rely=0.1, anchor="center")

        self.reminder_label = tk.Label(self.reminder_frame, text="Set Reminder Interval (minutes):", fg="black", font=("Helvetica", 12))
        self.reminder_label.grid(row=0, column=0, padx=5, pady=5)

        self.reminder_interval = tk.Spinbox(self.reminder_frame, from_=1, to=120, width=5, font=("Helvetica", 12))
        self.reminder_interval.grid(row=0, column=1, padx=5, pady=5)

        self.set_button = tk.Button(self.reminder_frame, text="Set", command=self.set_reminder, bg="orange", font=("Helvetica", 12))
        self.set_button.grid(row=0, column=2, padx=5, pady=5)

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

        self.history_button = tk.Button(self.button_frame, text="History", command=self.show_history, bg="lightgray", padx=10, pady=5)
        self.history_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Start with an empty task list
        self.load_tasks_to_listbox()
        self.run_scheduler()

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
                color = "dark green"
            else:
                status = " "
                color = "black"
            self.task_listbox.insert(tk.END, f"{i}. {status} {task.description}   ({task.date_time})")
            self.task_listbox.itemconfig(i - 1, {'fg': color})

    def mark_task_complete(self):
        try:
            index = int(self.task_listbox.curselection()[0])
            visible_tasks = [task for task in self.tasks if task not in self.deleted_tasks]
            task_to_complete = visible_tasks[index]
            task_to_complete.completed = True
            self.load_tasks_to_listbox()
            if all(task.completed for task in self.tasks if task not in self.deleted_tasks):
                self.show_reward_message()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task.")

    def show_reward_message(self):
        reward_window = tk.Toplevel(self.master)
        reward_window.title("Congratulations!")

        message_label = tk.Label(reward_window, text="Yeah! You completed all your tasks. Claim your reward.", font=("Helvetica", 14))
        message_label.pack(pady=10)

        claim_button = tk.Button(reward_window, text="Claim", command=lambda: self.claim_reward(reward_window), bg="gold", padx=10, pady=5)
        claim_button.pack(pady=10)

        reward_window.update_idletasks()
        width = reward_window.winfo_width()
        height = reward_window.winfo_height()
        x = (reward_window.winfo_screenwidth() // 2) - (width // 2)
        y = (reward_window.winfo_screenheight() // 2) - (height // 2)
        reward_window.geometry(f'{width}x{height}+{x}+{y}')

    def claim_reward(self, reward_window):
        self.points += 5
        self.points_label.config(text=f"Points: {self.points}")
        reward_window.destroy()

    def delete_task(self):
        try:
            index = int(self.task_listbox.curselection()[0])
            visible_tasks = [task for task in self.tasks if task not in self.deleted_tasks]
            task_to_delete = visible_tasks[index]
            task_to_delete.completed = True
            self.deleted_tasks.append(task_to_delete)
            self.load_tasks_to_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task.")

    def update_task(self):
        try:
            index = int(self.task_listbox.curselection()[0])
            new_description = self.task_input.get()
            if new_description:
                visible_tasks = [task for task in self.tasks if task not in self.deleted_tasks]
                task_to_update = visible_tasks[index]
                task_to_update.description = new_description
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

    def notify_incomplete_tasks(self):
        incomplete_tasks = [task.description for task in self.tasks if not task.completed and task not in self.deleted_tasks]
        if incomplete_tasks:
            message = "Incomplete Tasks please complete it:\n" + "\n".join(incomplete_tasks)
            self.bot.sendMessage(self.chat_id, message)

    def run_scheduler(self):
        def scheduler():
            while True:
                schedule.run_pending()
                time.sleep(1)

        threading.Thread(target=scheduler, daemon=True).start()

    def set_reminder(self):
        interval = int(self.reminder_interval.get())
        schedule.every(interval).minutes.do(self.notify_incomplete_tasks)

def main():
    root = tk.Tk()
    bot = telepot.Bot('7067501789:AAE0tgLtz5GFNdPsxjQp0-fGRcEWaWMAKgk')  # Replace with your actual bot token
    chat_id = '5774731114'  # Replace with your actual chat ID
    app = ToDoListApp(root, bot, chat_id)
    root.mainloop()

if __name__ == "__main__":
    main()
