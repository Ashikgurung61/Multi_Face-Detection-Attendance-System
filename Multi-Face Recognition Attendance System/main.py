from tkinter import *
from UsernameLogin import *
from login_face import *

def main_go():
    root.destroy()
    main_login()

def face_go():
    root.destroy()
    obj = App()

root = Tk()
root.geometry("1225x689+50+30")

try:
    root.attributes('-toolwindow', True)
except TclError:
    print('Not supported on your platform')

img_back = PhotoImage(file= "Images/main_back.png")
ins_img = Label(root, image=img_back).pack()

userPass = Button(root, text = "Username and Password",font=("Times New Roman",20), border=0, background="white", command= main_go)
userPass.place(x = 220, y = 410)

face = Button(root, text = "Face Authentiation",font=("Times New Roman",20),command=face_go, background="white",  border=0)
face.place(x = 220, y = 522)
root.mainloop()