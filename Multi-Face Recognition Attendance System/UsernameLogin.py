from tkinter import *
from tkinter import messagebox
import mysql.connector
from Home_page import home_page_here

con = mysql.connector.connect(host = "localhost", user = "root",passwd = "2020Bca01",database = "mca_minor_project")
cursor = con.cursor()

def clicks(event):
    if passwordentry.get() == "Password":
        passwordentry.config(state=NORMAL, show="") 
        passwordentry.delete(0, END)
        passwordentry.config(show="*")

def login():
    username = usernameentry.get()
    password = passwordentry.get()
    if (username == "") or (password == ""):
        messagebox.showerror("Empty","Please Enter username and password!!")
    else:
        cursor.execute("SELECT * FROM teacher WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        con.commit()
        messagebox.showinfo("Okay", "Success")
        if result:
            window.destroy()
            home_page_here()
        else:
            messagebox.showerror("Invalid Username and Password","Try Again!")

def main_login():
    global usernameentry, passwordentry, window
    window = Tk()
    window.geometry("1225x688")
    def click(event):
        usernameentry.config(state=NORMAL)
        usernameentry.delete(0,END)
        
    def clicks(events):
        passwordentry.config(state=NORMAL)
        passwordentry.delete(0,END)

    back_img = PhotoImage(file="Images/login_user.png")
    img_btn = PhotoImage(file = "Images/log_btn.png")
    _ = Label(window, image= back_img)
    _.place(x = 0, y = 0)

    usernameentry = Entry(window, font=("Times New Roman",20),foreground="white", background="#020e37", bd=0, highlightthickness=0)
    passwordentry = Entry(window,font=("Times New Roman",20), foreground="white", background="#020e37", bd= 0, highlightthickness= 0)

    usernameentry.insert(0,"Username")
    usernameentry.config(state=DISABLED)
    usernameentry.bind('<Button-1>',click)

    passwordentry.insert(1,"Password")
    passwordentry.config(state=DISABLED)
    passwordentry.bind('<Button-1>',clicks)

    # user_lbl = Label(window, text = ":Username", font=("Times New Roman",14), background="#020e37", foreground="white")
    # user_lbl.place(x = 1000, y = 280)

    # pas_lbl = Label(window, text = ":Password", font=("Times New Roman",14), background="#020e37", foreground="white")
    # pas_lbl.place(x = 800, y = 326)

    usernameentry.place(x = 800, y = 280)
    passwordentry.place(x = 800, y = 366)

    log_btn = Button(window, overrelief=SUNKEN,image= img_btn,bd = 0, highlightthickness=0, command=login)
    log_btn.place(x = 748, y = 471)
    window.mainloop()