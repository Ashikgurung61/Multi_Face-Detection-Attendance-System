from tkinter import *
import util_1
import cv2
from PIL import Image, ImageTk
from tkinter import messagebox
import os
import subprocess
from tkinter import ttk
import mysql.connector

con = mysql.connector.connect(host ="localhost", user = "root",passwd = "2020Bca01",database = "mca_minor_project")
cursor = con.cursor()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class Student:
    def __init__(self) -> None:
        self.main_window = Tk()
        self.main_window.title("Registration")
        self.main_window.geometry("1225x689+60+30")

        self.main_back = PhotoImage(file="Images/register.png")
        self. _ = Label(self.main_window, image= self.main_back).place(x = 0, y = 0)

        self.register_btn = util_1.get_button(self.main_window, 'Register New User', 'gray', self.register, fg='black')
        self.register_btn.place(x=785, y=400)

        self.webcam_label = util_1.get_img_label(self.main_window)
        self.webcam_label.place(x=20, y=110, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './student'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
        
        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            self.most_recent_capture_arr = frame
            img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)  
            self.most_rect_capture_pil = Image.fromarray(img_)

            imgtk = ImageTk.PhotoImage(image=self.most_rect_capture_pil)
            self._label.imgtk = imgtk
            self._label.configure(image=imgtk)
        self._label.after(20, self.process_webcam)

    def start(self):
        self.main_window.mainloop()

    def register(self):
        self.register_win = Toplevel(self.main_window)
        self.register_win.geometry("1200x600+50+25")

        # back_image = PhotoImage(file="Images/register_back.jpg")
        # labelba = Label(self.register_win, image=back_image)
        # labelba.place(x =0, y = 0)

        self._ = Frame(self.register_win, width=1180, height=250, background="navy")
        self._.place(x =10, y = 500)

        self.accept_button = util_1.get_button(self.register_win, 'Accept', "green", self.accept_register_new_user)
        self.accept_button.place(x=800, y=350)

        self.try_again_button = util_1.get_button(self.register_win, 'Try Again', "red", self.try_again_register_new_user)
        self.try_again_button.place(x=800, y=420)

        self.capture_label_ = util_1.get_img_label(self.register_win)
        self.capture_label_.place(x=10, y=10, width=700, height=500)

        self.add_img_to_label(self.capture_label_)

        self.entry_test_register_uid = util_1.get_entry_text(self.register_win)
        self.entry_test_register_uid.place(x=900, y=70)
        self.entry_test_register_new_user = util_1.get_entry_text(self.register_win)
        self.entry_test_register_new_user.place(x=900, y=140)
        self.entry_test_register_section = ttk.Combobox(self.register_win, values=("23MAM1","23MAM2","23MAM3","23MAM4"),height=1, width=14, font=("Arial", 25))
        self.entry_test_register_section.place(x=900, y=210)

        self.entry_test_register_seme = ttk.Combobox(self.register_win, values=("1","2","3","4","5","6","7","8"),height=1, width=14, font=("Arial", 25))
        #self.entry_test_register_seme = util_1.get_entry_text(self.register_win)
        self.entry_test_register_seme.place(x=900, y=280)

        self.text_label__ = util_1.get_text_label(self.register_win, 'UID ')
        self.text_label__.place(x=750, y=70)

        self.text_label1__ = util_1.get_text_label(self.register_win, 'Name ')
        self.text_label1__.place(x=750, y=140)

        self.text_label2__ = util_1.get_text_label(self.register_win, 'Section ')
        self.text_label2__.place(x=750, y=210)

        self.text_label3__ = util_1.get_text_label(self.register_win, 'Semester ')
        self.text_label3__.place(x=750, y=280)


    def try_again_register_new_user(self):
        self.register()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_rect_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_rect_capture_pil.copy()

    def accept_register_new_user(self):
        name = self.entry_test_register_new_user.get(1.0, "end-1c")
        uid = self.entry_test_register_uid.get(1.0,"end-1c")
        semester = self.entry_test_register_seme.get()
        section = self.entry_test_register_section.get()
        # names = name +"_"+uid
        value = (uid, name, section, semester)
        #print("----------------->", value)
        try:
            #print("------------------->",1)
            cursor.execute("INSERT INTO student (uid, name, section, semester) VALUES (%s, %s, %s, %s)", value)
            con.commit()
            if self.most_recent_capture_arr is not None:
                cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(uid)), self.most_recent_capture_arr)
            else:
                messagebox.showerror("Error", "No image captured.")
            messagebox.showinfo("Success","Register Successful")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", "UID already Exist")
        finally:
            self.register_win.destroy()
            self.main_window.destroy()
            from Home_page import home_page_here
            home_page_here()


if __name__ == "__main__":
    app = Student()
    app.start()