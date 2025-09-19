from tkinter import *
from tkinter import ttk
import mysql.connector
from datetime import datetime

con = mysql.connector.connect(host="localhost", user="root", passwd="2020Bca01", database="mca_minor_project")
cursor = con.cursor()

time = datetime.now()
date_today = time.date().strftime("%d/%m/%y")

def go_back_to_home():
    root88.destroy()
    from Home_page import home_page_here
    home_page_here()

def search_tree():
    query = search_var.get().lower()
    
    tree.delete(*tree.get_children())

    sql_query = """
        SELECT a.a_id, a.uid, s.name, a.period, a.date, a.status 
        FROM attendance a 
        JOIN student s ON a.uid = s.uid 
        WHERE a.date = %s AND a.period LIKE %s
    """
    # SELECT a.a_id, a.uid, s.name, a.period, a.date, a.status 
    #     FROM attendance a 
    #     JOIN student s ON a.uid = s.uid 
    #     WHERE a.date = %s AND (a.period LIKE %s OR LOWER(a.uid) LIKE %s)
    cursor.execute(sql_query, (date_today, f"%{query}%"))
    filtered_rows = cursor.fetchall()

    for row in filtered_rows:
        tree.insert("", "end", values=row)
    
def show_status():
    global root88, tree, search_var
    root88 = Tk()
    root88.geometry("1250x650+30+15")
    root88.title("Attendance System")
    root88.configure(bg="#326273")
    root88.resizable(0, 0)
    tree()

    try:
        root88.attributes('-toolwindow', True)
    except TclError:
        print('Not supported on your platform')

    _fg = PhotoImage(file="Images/status_head.png")

    heading = Label(root88,image=_fg)
    heading.place(x=15, y=32)

    b = Button(root88, text="Back", command=go_back_to_home)
    b.place(x=15, y=5)
    
    
    search_var = StringVar()
    search_entry = ttk.Entry(root88, font=("Times New roman",15),textvariable=search_var)
    search_entry.place(x=15, y=170)

    search_button = ttk.Button(root88, text="Search", command=search_tree)
    search_button.place(x=230, y=170)

    root88.mainloop()

def tree():
    global tree
    tree = ttk.Treeview(root88, columns=(1, 2, 3, 4, 5, 6), show="headings", height="21")
    tree.place(x=15, y=200)
    tree.heading(1, text="SL No")
    tree.heading(2, text="UID")
    tree.heading(3, text="Name")
    tree.heading(4, text="Period")
    tree.heading(5, text="Date")
    tree.heading(6, text="Status")

    s = ttk.Style(root88)
    s.theme_use("clam") 

    s.configure("Treeview.Heading", 
                    font=("Arial", 12, "bold"), 
                    foreground="blue", 
                    background="lightgray")

    s.configure("Treeview", 
                    font=("Arial", 11), 
                    rowheight=25, 
                    background="white", 
                    fieldbackground="white")

    s.map("Treeview", 
            background=[("selected", "green")], 
            foreground=[("selected", "white")])

    scrollbar = ttk.Scrollbar(root88, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    initial_query = """
        SELECT a.a_id, a.uid, s.name, a.period, a.date, a.status 
        FROM attendance a 
        JOIN student s ON a.uid = s.uid 
        WHERE a.date = %s 
        ORDER BY a.a_id
    """
    cursor.execute(initial_query, (date_today,))
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", "end", values=row)

# show_status()