from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from tkinter import messagebox


# MySQL Connection
con = mysql.connector.connect(host="localhost", user="root", passwd="2020Bca01", database="mca_minor_project")
cursor = con.cursor()

def updateT():
    global tree
    tree = ttk.Treeview(root88, columns=(1, 2, 3, 4, 5,6), show="headings", height="15")
    tree.place(x=25, y=200)

    tree.heading(1, text = "SL No")
    tree.heading(2, text="UID")
    tree.heading(3, text="Name")
    tree.heading(4, text="Period")
    tree.heading(5, text="Date")
    tree.heading(6, text="Status")

    s = ttk.Style(root88)
    s.theme_use("winnative")

    query ="SELECT a.a_id, a.uid,s.name, a.period, a.date, a.status FROM attendance a JOIN student s ON a.uid = s.uid;"
    # query = "SELECT uid, name, status, date, period FROM attendance"
    cursor.execute(query)
    rows = cursor.fetchall()
    tree.delete(*tree.get_children())
    for i in rows:
        tree.insert("", "end", values=i)

def select_record():
    global selected, value
    uid_entry.delete(0, END)
    status_entry.delete(0, END)
    date_entry.delete(0, END)
    period_entry.delete(0, END)

    selected = tree.focus()
    value = tree.item(selected, "values")

    uid_entry.insert(0, value[0])
    status_entry.insert(0, value[-1])
    date_entry.insert(0, value[4])
    period_entry.insert(0, value[3])
    updateT()

def update_status():
    global uid,status, date, period
    uid = uid_entry.get()
    status = status_entry.get()
    date = date_entry.get()
    period = period_entry.get()

    value = (status, date, period, uid)
    try:
        query = "UPDATE attendance SET status = %s, date = %s, period = %s WHERE a_id = %s"
        cursor.execute(query, value)
        con.commit()
        messagebox.showinfo("Success", "Attendance Updated Successfully")
    except:
        messagebox.showerror("Error", "Failed to update attendance")
    updateT()
#from Home_page import *
def go_back():
    root88.destroy()
    from Home_page import home_page_here
    home_page_here()
    #home_page_here()

def show_plz():
    global uid_entry, status_entry, date_entry, period_entry, tree, root88
    root88 = Tk()
    root88.geometry("1250x650+30+15")
    root88.title("Attendance System")
    root88.configure(bg="#326273")
    root88.resizable(0, 0)

    try:
        root88.attributes('-toolwindow', True)
    except TclError:
        print('Not supported on your platform')

    _fi = PhotoImage(file="Images/header.png")



    frame = Label(root88, image=_fi)
    frame.place(x=25, y=30)

    

    slt = Button(root88, overrelief=SUNKEN, text="Select", width=14, height=1, background="Grey", command=select_record)
    slt.place(x=680, y=620)

    back = Button(root88, bd=0, overrelief=SUNKEN, width=10, bg="black", text="Home", fg="White", command=go_back).place(x=25, y=5)

    fra = Frame(root88, border=3)
    fra.place(x=325, y=530)

    # Labels for UID, Name, Status, Date, Period
    uid_lbl = Label(fra, text="ID No", background="Grey")
    # name_lbl = Label(fra, text="Name", background="Grey")
    status_lbl = Label(fra, text="Status", background="Grey")
    date_lbl = Label(fra, text="Date", background="Grey")
    period_lbl = Label(fra, text="Period", background="Grey")

    uid_lbl.grid(row=1, column=0, padx=5, pady=5)
    # name_lbl.grid(row=1, column=1, padx=5, pady=5)
    status_lbl.grid(row=1, column=2, padx=5, pady=5)
    date_lbl.grid(row=1, column=3, padx=5, pady=5)
    period_lbl.grid(row=1, column=4, padx=5, pady=5)

    uid_entry = Entry(fra, bd=3)
    status_entry = ttk.Combobox(fra, values=("Present","Absent"))
    date_entry = Entry(fra, bd=3)
    period_entry = Entry(fra, bd=3)

    uid_entry.grid(row=0, column=0, padx=10, pady=10)
    status_entry.grid(row=0, column=2, padx=10, pady=10)
    date_entry.grid(row=0, column=3, padx=10, pady=10)
    period_entry.grid(row=0, column=4, padx=10, pady=10)

    upd = Button(root88, text="Update", width=14, height=1, background="Green", command=update_status)
    upd.place(x=520, y=620)

    # delt = Button(root88, overrelief=SUNKEN, text="Delete", width=14, height=1, background="Red")
    # delt.place(x=740, y=620)

    tree = ttk.Treeview(root88, columns=(1, 2, 3, 4, 5,6), show="headings", height="15")
    tree.place(x=25, y=200)
    tree.heading(1, text = "SL No")
    tree.heading(2, text="UID")
    tree.heading(3, text="Name")
    tree.heading(4, text="Period")
    tree.heading(5, text="Date")
    tree.heading(6, text="Status")

    s = ttk.Style(root88)
    s.theme_use("winnative")

    query ="SELECT a.a_id, a.uid,s.name, a.period, a.date, a.status FROM attendance a JOIN student s ON a.uid = s.uid;"
    # query = "SELECT u.name, uid, status, date, period FROM attendance"
    cursor.execute(query)
    rows = cursor.fetchall()
    tree.delete(*tree.get_children())
    for i in rows:
        tree.insert("", "end", values=i)

    root88.mainloop()
# show_plz()