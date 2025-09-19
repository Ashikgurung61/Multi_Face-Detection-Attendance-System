from tkinter import *
from teacher_add import *
from tkinter import messagebox
from student_register import *
from MarkAttendance import *
from update_attendance import *
from check_status import *

def teacher_go():
    win1.destroy()
    teacher()

def student_go():
    win1.destroy()
    Student()

def mark():
    win1.destroy()
    main()

def go_their():
    win1.destroy()
    show_plz()

def today_go():
    win1.destroy()
    show_status()

def home_page_here():
    global win1
    win1 = Tk()
    win1.title("Home Page")
    win1.geometry("1225x698+50+20")

    main_back = PhotoImage(file="Images/home.png")

    _ = Label(win1, image= main_back).place(x = 0, y = 0)

    mark_attendance = Button(win1, text = "Mark",foreground="white",font=("Times New Roman",15), background="red", width=10, command=mark)
    mark_attendance.place(x = 55, y = 480)

    new_btn = Button(win1, text = "Add",foreground="white",font=("Times New Roman",15), background="red", width=10, command=student_go)
    new_btn.place(x = 305, y = 480)

    Check_status = Button(win1, text = "Check",foreground="white",font=("Times New Roman",15), background="red", width=10, command=today_go)
    Check_status.place(x = 555, y = 480)

    update_attendance = Button(win1, text = "Correct",foreground="white",font=("Times New Roman",15), background="red", width=10, command=go_their)
    update_attendance.place(x = 805, y = 480)

    new_faculty = Button(win1, text = "Add",foreground="white",font=("Times New Roman",15), background="red", width=10, command=teacher_go)
    new_faculty.place(x = 1055, y = 480)

    win1.mainloop()
home_page_here()