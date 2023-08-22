import tkinter
from tkinter import *

root = Tk()
root.title("To-do-list")
root.geometry("800x600+500+200")
root.resizable(False,False)

task_list = []


def addTask():
    task = task_entry.get()
    task_entry.delete(0, END)
    if task:
        with open("tasklist.txt", 'a') as taskfile:
            taskfile.write(f"\n{task}")
        task_list.append(task)
        listbox.insert(END, task)


def deleteTask():
    task = str(listbox.get(ANCHOR))
    if task in task_list:
        task_list.remove(task)
        with open("tasklist.txt", 'w') as taskfile:
            for task in task_list:
                taskfile.write(task + "\n")

        listbox.delete(ANCHOR)

def crossOff ():
    listbox.itemconfig(
        listbox.curselection(), fg="#dedede"
    )
    listbox.selection_clear(0,END)
  

def uncross():
    listbox.itemconfig(
        listbox.curselection(), fg="#000000"
    )
    listbox.selection_clear(0,END)

def deleteCrossedItems():
    count=0
    while count<listbox.size():
        if listbox.itemcget(count, "fg")=="#dedede":
           listbox.delete(listbox.index(count))
        else:
            count+=1


def openTaskFile():
    with open("Downloads\\tasklist.txt", "r") as taskfile:
        tasks = taskfile.readlines()
    for task in tasks:
        if task != '\n':
            task_list.append(task)
            listbox.insert(END, task)


Image_icon = PhotoImage(file="Downloads\\task.png")
root.iconphoto(False, Image_icon)

TopImage = PhotoImage(file="Downloads\\bar (1).png")
Label(root, image=TopImage).pack()

dockImage = PhotoImage(file="Downloads\dock.png")
Label(root, image=dockImage, bg="#32405b").place(x=30, y=25)

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

listbox = Listbox(frame1, font=('arial,12'), width=40, height=10, bg="#FFE6EE", fg="black", cursor="hand2",selectbackground="#0000FF")
listbox.pack(side=LEFT, fill=BOTH, padx=2)
scrollbar = Scrollbar(frame1)
scrollbar.pack(side=RIGHT, fill=BOTH)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

openTaskFile()

frame2=Frame(root,width=400,height=50,bg="white")
frame2.place(x=155,y=500)
delete_button= Button(frame2, text="DELETE TASK", font="arial 10 bold",width=15, bg="#FE036A",fg="#fff",bd=0,command=deleteTask)
delete_button.grid(row=10, column=0)

frame3=Frame(root,width=400,height=50,bg="white")
frame3.place(x=350,y=500)
taskdone_button= Button(frame3, text="DONE", font="arial 10 bold",width=10, bg="#FE036A",fg="#fff",bd=0,command=crossOff)
taskdone_button.grid(row=10, column=0)

frame4=Frame(root,width=400,height=50,bg="white")
frame4.place(x=500,y=500)
Tasknotdone_button= Button(frame4, text="NOT DONE", font="arial 10 bold",width=15, bg="#FE036A",fg="#fff",bd=0,command=uncross)
Tasknotdone_button.grid(row=10, column=0)

frame5=Frame(root,width=400,height=50,bg="white")
frame5.place(x=310,y=550)
deleteCrossedItems_button= Button(frame5, text="DELETE ALL DONE TASKS", font="arial 10 bold",width=20, bg="#FE036A",fg="#fff",bd=0,command=deleteCrossedItems)
deleteCrossedItems_button.grid(row=11, column=0)


root.mainloop()