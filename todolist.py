import tkinter as tk
from tkinter import messagebox
import sqlite3

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-do List")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        self.init_database()
        self.create_widgets()
        self.load_tasks()
        
    def init_database(self):
        self.conn = sqlite3.connect("task_database.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE if not exists tasks(task_text TEXT)""")
        self.conn.commit()
        
    def create_widgets(self):
        self.heading = tk.Label(self.root, text="My Tasks", font="bahnschrift 20 bold", fg="blue") 
        self.heading.place(x=320, y=5)
        
        self.task_frame = tk.Frame(self.root, width=400, height=50, bg="white")  
        self.task_frame.place(x=200, y=100)
        
        self.task_entry = tk.Entry(self.task_frame, width=18, font="arial 20", bg="white")  
        self.task_entry.grid(row=0, column=0, padx=5, pady=5)
        
        self.add_button = tk.Button(self.task_frame, text="ADD", font="arial 20 bold", command=self.add_task, bg="green", fg="white")  
        self.add_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.task_list_frame = tk.Frame(self.root, width=700, height=280, bg="white")  
        self.task_list_frame.pack(pady=(160, 0))
        
        self.task_listbox = tk.Listbox(self.task_list_frame, font=('arial,12'), width=40, height=10, bg="light blue", fg="black")  
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=2)
        self.task_list_frame.place(x=200, y=190)
        
        self.scrollbar = tk.Scrollbar(self.task_list_frame, command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.action_buttons_frame = tk.Frame(self.root, width=400, height=50) 
        self.action_buttons_frame.place(x=200, y=400)
        
        self.delete_button = tk.Button(self.action_buttons_frame, text="DELETE TASK", command=self.delete_task, bg="red", fg="white")  
        self.delete_button.grid(row=0, column=0, padx=50)
               
        self.task_done_button = tk.Button(self.action_buttons_frame, text="DONE", command=self.mark_task_done, bg="orange", fg="white")  
        self.task_done_button.grid(row=0, column=5, padx=70)
        
        
    def load_tasks(self): #all tasks written in the entry will be added to the listbox 
        self.task_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT task_text FROM tasks")
        fetched_tasks = self.cursor.fetchall()
        for task in fetched_tasks:
            self.task_listbox.insert(tk.END, task[0])
            
    def add_task(self): #adding a tak to the listbox
        task = self.task_entry.get().strip()
        if task:
            self.task_listbox.insert(0, task)
            self.cursor.execute("INSERT INTO tasks (task_text) VALUES (?)", (task,))
            self.conn.commit()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def delete_task(self):  #Deleting a selected task
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.task_listbox.get(selected_task_index)
            self.task_listbox.delete(selected_task_index)
            self.cursor.execute("DELETE FROM tasks WHERE task_text=?", (task,))
            self.conn.commit()
        else:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def mark_task_done(self): #select a task then click on done it will be marked done by changing colour to gray
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.task_listbox.get(selected_task_index)
            self.task_listbox.itemconfig(selected_task_index, fg="#dedede")
            self.task_listbox.selection_clear(0, tk.END)
            self.conn.commit()
        else:
            messagebox.showwarning("Warning", "Please select a task to mark as done.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()
