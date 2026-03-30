import customtkinter as ctk
from CTkListbox import CTkListbox
from tkinter import messagebox
import matplotlib.pyplot as plt

# ---------------- APP SETUP ---------------- #
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("To-Do List")
app.geometry("520x650")

# Background color options
#BG_COLOR = "#d0ebff"   # pastel blue
BG_COLOR = "#d3f9d8" # pastel green

app.configure(fg_color=BG_COLOR)

# ---------------- DATA ---------------- #
tasks = []

# ---------------- FUNCTIONS ---------------- #
def add_task():
    text = task_entry.get()
    due = due_entry.get()
    priority = priority_var.get()

    if text == "":
        messagebox.showwarning("Warning", "Enter a task!")
        return

    task = {
        "text": text,
        "completed": False,
        "priority": priority,
        "due": due
    }

    tasks.append(task)
    update_tasks()

    task_entry.delete(0, "end")
    due_entry.delete(0, "end")

def delete_task():
    try:
        index = task_list.curselection()
        tasks.pop(index)
        update_tasks()
    except:
        messagebox.showwarning("Warning", "Select a task!")

def toggle_complete():
    try:
        index = task_list.curselection()
        tasks[index]["completed"] = not tasks[index]["completed"]
        update_tasks()
    except:
        messagebox.showwarning("Warning", "Select a task!")

def update_tasks():
    task_list.delete("all")
    
    selected_filter = filter_var.get()

    for task in tasks:
        
        # FILTER LOGIC
        if selected_filter == "Completed" and not task["completed"]:
            continue
        elif selected_filter == "Pending" and task["completed"]:
            continue
        elif selected_filter in ["High", "Medium", "Low"] and task["priority"] != selected_filter:
            continue
        
        display = ""

        # ✔ Checkbox
        if task["completed"]:
            display += "✔ "
        else:
            display += "☐ "

        # Priority Indicator (TEXT instead of color)
        if task["priority"] == "High":
            display += "[HIGH PRIORITY] "
        elif task["priority"] == "Medium":
            display += "[MED PRIORITY] "
        else:
            display += "[LOW PRIORITY] "

        display += task["text"]

        # 📅 Due Date
        if task["due"]:
            display += f" | {task['due']}"

        task_list.insert("end", display)
        
def show_analytics():
    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    pending = total - completed

    high = sum(1 for t in tasks if t["priority"] == "High")
    medium = sum(1 for t in tasks if t["priority"] == "Medium")
    low = sum(1 for t in tasks if t["priority"] == "Low")

    message = f"""
TASK ANALYTICS

Total Tasks: {total}
Completed: {completed}
Pending: {pending}

Priority Breakdown:
High: {high}
Medium: {medium}
Low: {low}
"""

    messagebox.showinfo("Analytics", message)

def show_graph():
    total = len(tasks)
    if total == 0:
        messagebox.showwarning("Warning", "No tasks to analyze!")
        return

    completed = sum(1 for t in tasks if t["completed"])
    pending = total - completed

    labels = ["Completed", "Pending"]
    values = [completed, pending]

    plt.figure()
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Task Completion Analytics")
    plt.show()

filter_var = ctk.StringVar(value="All")
    
# ---------------- UI ---------------- #

# Title
title = ctk.CTkLabel(app, text="My Tasks", font=("Poppins", 22, "bold"), text_color="black")
title.pack(pady=20)

# Task Entry
task_entry = ctk.CTkEntry(app, placeholder_text="Enter your task", width=350, text_color="black", fg_color="white")
task_entry.pack(pady=10)

# Due Date
due_entry = ctk.CTkEntry(app, placeholder_text="Due Date (DD-MM-YYYY)", width=350, text_color="black", fg_color="white")
due_entry.pack(pady=10)

# Priority Dropdown
priority_var = ctk.StringVar(value="Low")
priority_menu = ctk.CTkOptionMenu(
    app,
    values=["High", "Medium", "Low"],
    variable=priority_var,
    fg_color="white",
    text_color="black",
    button_color="#e6e6e6"
)
priority_menu.pack(pady=10)

#Menu Dropdown
filter_menu = ctk.CTkOptionMenu(
    app,
    values=["All", "Completed", "Pending", "High", "Medium", "Low"],
    variable=filter_var,
    command=lambda x: update_tasks(),
    fg_color="white",
    text_color="black",
    button_color="#e6e6e6"
)
filter_menu.pack(pady=10)

# Buttons
btn_frame = ctk.CTkFrame(app, fg_color="transparent")
btn_frame.pack(pady=15)

analytics_btn = ctk.CTkButton(
    btn_frame,
    text="Analytics",
    command=show_analytics,
    fg_color="white",
    text_color="black",
    hover_color="#e6e6e6"
)
analytics_btn.grid(row=1, column=1, pady=10)

graph_btn = ctk.CTkButton(
    btn_frame,
    text="Show Graph",
    command=show_graph,
    fg_color="white",
    text_color="black",
    hover_color="#e6e6e6"
)
graph_btn.grid(row=1, column=0, pady=10)

add_btn = ctk.CTkButton(
    btn_frame,
    text="Add Task",
    command=add_task,
    fg_color="white",
    text_color="black",
    hover_color="#e6e6e6"
)
add_btn.grid(row=0, column=0, padx=10)

delete_btn = ctk.CTkButton(
    btn_frame,
    text="Delete",
    command=delete_task,
    fg_color="white",
    text_color="black",
    hover_color="#e6e6e6"
)
delete_btn.grid(row=0, column=1, padx=10)

complete_btn = ctk.CTkButton(
    btn_frame,
    text="Mark Done",
    command=toggle_complete,
    fg_color="white",
    text_color="black",
    hover_color="#e6e6e6"
)
complete_btn.grid(row=0, column=2, padx=10)

# Task List (FIXED)
task_list = CTkListbox(
    app,
    width=450,
    height=350,
    fg_color="white",
    text_color="black",
    button_color="#e6e6e6",
    border_color="#cccccc"
)
task_list.pack(pady=20)

if __name__ == "__main__":
    app.mainloop()
