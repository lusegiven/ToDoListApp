import tkinter
from tkinter import *
import sqlite3

#hey POV you made your first app and pushed it to github 

def addTask():
    task = task_entry.get()
    task_entry.delete(0, END)
    if task:
        listbox.insert(0, task)
    conn.commit()


def deleteTask():
    selected_task_index = listbox.curselection()
    if selected_task_index:
        selected_task_index = selected_task_index[0]
        task = listbox.get(selected_task_index)
        listbox.delete(selected_task_index)
        cursor.execute("DELETE FROM tasks WHERE task_text=?", (task,))
        conn.commit()


def saveList():
    cursor.execute("DELETE FROM tasks")
    conn.commit()
    for task in listbox.get(0, END):
        cursor.execute("INSERT INTO tasks (task_text) VALUES (?)", (task,))
    conn.commit()

    listbox.delete(0, END)
    grabAll()


def grabAll():
    cursor.execute("SELECT task_text FROM tasks")
    fetched_tasks = cursor.fetchall()
    for task in fetched_tasks:
        listbox.insert(END, task[0])


conn = sqlite3.connect("task_database.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE if not exists tasks(task_text Text)""")
conn.commit()

root = Tk()
root.title("To-do-list")
root.geometry("800x600+500+200")
root.resizable(False, False)


def crossOff():
    listbox.itemconfig(
        listbox.curselection(), fg="#dedede"
    )
    listbox.selection_clear(0, END)


def uncross():
    listbox.itemconfig(
        listbox.curselection(), fg="#000000"
    )
    listbox.selection_clear(0, END)


def deleteCrossedItems():
    count = 0
    while count < listbox.size():
        if listbox.itemcget(count, "fg") == "#dedede":
            listbox.delete(listbox.index(count))
        else:
            count += 1


def deleteSelectedItems():
    selected_indices = listbox.curselection()
    for index in selected_indices:
        listbox.delete(index)


Image_icon = PhotoImage(file="Downloads\\task.png")
root.iconphoto(False, Image_icon)

heading = Label(root, text="My Tasks", font="bahnschrift 20 bold", fg="black", bg="#EEF1F4")
heading.place(x=320, y=5)

frame = Frame(root, width=400, height=50, bg="white")
frame.place(x=200, y=100)

task = StringVar()
task_entry = Entry(frame, width=18, font="arial 20", bd=0)
task_entry.place(x=10, y=7)

button = Button(frame, text="ADD", font="arial 20 bold", width=6, bg="#FE036A", fg="#fff", bd=0, command=addTask)
button.place(x=300, y=0)

frame1 = Frame(root, bd=3, width=700, height=280, bg="#FFE6EE")
frame1.pack(pady=(160, 0))

listbox = Listbox(frame1, font=('arial,12'), width=40, height=10, bg="#FFE6EE", fg="black", cursor="hand2",
                  selectmode='multiple', selectbackground="#0000FF")
listbox.pack(side=LEFT, fill=BOTH, padx=2)
scrollbar = Scrollbar(frame1)
scrollbar.pack(side=RIGHT, fill=BOTH)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

frame2 = Frame(root, width=400, height=50, bg="white")
frame2.place(x=155, y=500)
delete_button = Button(frame2, text="DELETE TASK", font="arial 10 bold", width=15, bg="#FE036A", fg="#fff", bd=0,
                       command=deleteTask)
delete_button.grid(row=10, column=0)

frame3 = Frame(root, width=400, height=50, bg="white")
frame3.place(x=350, y=500)
taskdone_button = Button(frame3, text="DONE", font="arial 10 bold", width=10, bg="#FE036A", fg="#fff", bd=0,
                         command=crossOff)
taskdone_button.grid(row=10, column=0)

frame4 = Frame(root, width=400, height=50, bg="white")
frame4.place(x=500, y=500)
Tasknotdone_button = Button(frame4, text="NOT DONE", font="arial 10 bold", width=15, bg="#FE036A", fg="#fff", bd=0,
                            command=uncross)
Tasknotdone_button.grid(row=10, column=0)

frame5 = Frame(root, width=400, height=50, bg="white")
frame5.place(x=100, y=550)
deleteCrossedItems_button = Button(frame5, text="DELETE DONE TASKS", font="arial 10 bold", width=20, bg="#FE036A",
                                   fg="#fff", bd=0, command=deleteCrossedItems)
deleteCrossedItems_button.grid(row=11, column=0)

frame6 = Frame(root, width=400, height=50, bg="white")
frame6.place(x=300, y=550)
saveList_button = Button(frame6, text="SAVE TASKS", font="arial 10 bold", width=20, bg="#FE036A", fg="#fff", bd=0,
                         command=saveList)
saveList_button.grid(row=12, column=0)

frame7 = Frame(root, width=400, height=50, bg="white")
frame7.place(x=500, y=550)
deleteSelectedItems_button = Button(frame7, text="DELETE SELECTED", font="arial 10 bold", width=20, bg="#FE036A",
                                    fg="#fff", bd=0, command=deleteSelectedItems)
deleteSelectedItems_button.grid(row=13, column=0)

grabAll()
root.mainloop()
conn.close()
