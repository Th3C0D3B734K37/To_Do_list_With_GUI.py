import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Task:
    def __init__(self, description, completed=False):
        self.description = description
        self.completed = completed

class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, description):
        task = Task(description)
        self.tasks.append(task)

    def update_task_status(self, task_index, completed=True):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].completed = completed
        else:
            print("Invalid task index.")

    def display_tasks(self):
        if not self.tasks:
            return "No tasks in the list."
        else:
            task_list_text = ""
            for i, task in enumerate(self.tasks):
                status = "✓" if task.completed else "✗"
                task_list_text += f"{i+1}. [{status}] {task.description}\n"
            return task_list_text

def on_title_bar_drag(event):
    x = root.winfo_pointerx() - root._offset_x
    y = root.winfo_pointery() - root._offset_y
    root.geometry(f"+{x}+{y}")

def on_title_bar_press(event):
    root._offset_x = event.x
    root._offset_y = event.y

def on_add_task():
    description = entry_task.get()
    if description.strip():
        todo_list.add_task(description)
        update_task_list()
        entry_task.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task description.")

def on_mark_completed():
    try:
        task_index = int(entry_task_index.get()) - 1
        if 0 <= task_index < len(todo_list.tasks):
            todo_list.update_task_status(task_index)
            update_task_list()
            entry_task_index.delete(0, tk.END)
            notify_task_completion(task_index)
        else:
            messagebox.showwarning("Warning", "Invalid task index.")
    except ValueError:
        messagebox.showwarning("Warning", "Please enter a valid task index.")

def notify_task_completion(task_index):
    if todo_list.tasks[task_index].completed:
        messagebox.showinfo("Task Completed", f"Task '{todo_list.tasks[task_index].description}' is marked as completed!")
    else:
        messagebox.showinfo("Task Pending", f"Task '{todo_list.tasks[task_index].description}' is pending!")

def update_task_list():
    task_list.config(state=tk.NORMAL)
    task_list.delete(1.0, tk.END)
    task_list.insert(tk.END, todo_list.display_tasks())
    task_list.config(state=tk.DISABLED)

def main():
    global todo_list, entry_task, entry_task_index, task_list, root, title_bar

    todo_list = TodoList()

    root = tk.Tk()
    root.title("To-Do List")
    root.geometry("400x400")

    # Remove the default title bar
    root.overrideredirect(1)

    # Get the absolute path to the directory where the Python script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the dragon_icon.jpg file
    icon_path = os.path.join(script_dir, "dragon_icon.jpg")

    try:
        # Use PIL to open the image
        icon_image = Image.open(icon_path)
        root.iconphoto(False, ImageTk.PhotoImage(icon_image))
    except Exception as e:
        print("Error opening icon image:", e)

    # Create a custom title bar
    title_bar = tk.Canvas(root, height=30, bg="#333333", highlightthickness=0)
    title_bar.pack(fill=tk.X)

    # Title bar 3D effect
    title_bar.create_line(0, 0, 0, 29, width=1, fill="#111111")
    title_bar.create_line(0, 0, 399, 0, width=1, fill="#111111")
    title_bar.create_line(0, 29, 399, 29, width=1, fill="#444444")

    label_title = tk.Label(title_bar, text="To-Do List", fg="white", bg="#333333", font=("Segoe UI", 12))
    label_title.pack(side=tk.LEFT, padx=10)

    # Close button
    def on_close():
        if messagebox.askyesno("Close", "Do you want to close the application?"):
            root.destroy()

    close_button = tk.Button(title_bar, text="X", bg="#333333", fg="white", bd=0, command=on_close, font=("Arial", 12))
    close_button.pack(side=tk.RIGHT, padx=5)

    # Minimize button
    def on_minimize():
        root.iconify()

    minimize_button = tk.Button(title_bar, text="-", bg="#333333", fg="white", bd=0, command=on_minimize, font=("Arial", 12))
    minimize_button.pack(side=tk.RIGHT)

    # Custom title bar event handlers for dragging the window
    title_bar.bind("<B1-Motion>", on_title_bar_drag)
    title_bar.bind("<ButtonPress-1>", on_title_bar_press)

    # Content Frame
    content_frame = tk.Frame(root, bg="white", bd=1, relief=tk.RAISED)
    content_frame.pack(fill=tk.BOTH, expand=True)

    label_task = tk.Label(content_frame, text="Enter Task:", font=("Segoe UI", 14))
    label_task.pack(pady=5)

    entry_task = tk.Entry(content_frame, width=30, font=("Segoe UI", 12))
    entry_task.pack()

    button_add_task = tk.Button(content_frame, text="Add Task", command=on_add_task, font=("Segoe UI", 12))
    button_add_task.pack(pady=5)

    label_task_index = tk.Label(content_frame, text="Task Index:", font=("Segoe UI", 14))
    label_task_index.pack(pady=5)

    entry_task_index = tk.Entry(content_frame, width=30, font=("Segoe UI", 12))
    entry_task_index.pack()

    button_mark_completed = tk.Button(content_frame, text="Mark Completed", command=on_mark_completed, font=("Segoe UI", 12))
    button_mark_completed.pack(pady=5)

    task_list = tk.Text(content_frame, width=40, height=10, state=tk.DISABLED, font=("Segoe UI", 12))
    task_list.pack(pady=10)

    update_task_list()

    root.mainloop()

if __name__ == "__main__":
    main()
