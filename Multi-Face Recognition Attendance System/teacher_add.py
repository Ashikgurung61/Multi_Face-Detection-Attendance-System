from tkinter import *
import util
import cv2
from PIL import Image, ImageTk
from tkinter import messagebox
import os
import subprocess
import mysql.connector

con = mysql.connector.connect(host = "localhost", user = "root",passwd = "2020Bca01",database = "mca_minor_project")
cursor = con.cursor()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class teacher:
    def __init__(self) -> None:
        self.main_window = Tk()
        self.main_window.title("Registration")
        self.main_window.geometry("1225x689+80+15")

        self.main_back = PhotoImage(file="Images/face_log.png")
        self. _ = Label(self.main_window, image= self.main_back).place(x = 0, y = 0)

        # self.login_btn = util.get_button(self.main_window, 'Login', "green", self.login)
        # self.login_btn.place(x=800, y=500)

        self.register_btn = util.get_button(self.main_window, 'Register New User', 'gray', self.register, fg='black')
        self.register_btn.place(x=785, y=400)


        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=20, y=110, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './admin_img'
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
        self.register_win.geometry("1200x520+100+105")

        self.accept_button = util.get_button(self.register_win, 'Confirm', "green", self.accept_register_new_user)
        self.accept_button.place(x=750, y=300)

        self.try_again_button = util.get_button(self.register_win, 'Retake', "red", self.try_again_register_new_user)
        self.try_again_button.place(x=750, y=400)

        self.capture_label_ = util.get_img_label(self.register_win)
        self.capture_label_.place(x=10, y=10, width=700, height=500)

        self.add_img_to_label(self.capture_label_)

        self.entry_test_register_new_user = util.get_entry_text(self.register_win)
        self.entry_test_register_new_user.place(x=750, y=80)

        self.entry_test_register_pass = util.get_entry_text(self.register_win)
        self.entry_test_register_pass.place(x=750, y=200)        

        self.text_label__ = util.get_text_label(self.register_win, 'Create Username: ')
        self.text_label__.place(x=750, y=30)

        self.text_label1__ = util.get_text_label(self.register_win, 'Create Password: ')
        self.text_label1__.place(x=750, y=145)

    def try_again_register_new_user(self):
        self.register()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_rect_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_rect_capture_pil.copy()

    def accept_register_new_user(self):
        username = self.entry_test_register_new_user.get(1.0, "end-1c")
        password = self.entry_test_register_pass.get(1.0, "end-1c")
        query = "INSERT INTO Teacher(username, password) VALUES (%s, %s)"
        values = (username, password)

        if not username or not password:
            messagebox.showerror("Error", "Username and Password cannot be empty.")
            return

        if self.most_recent_capture_arr is not None:
            if not os.path.exists(self.db_dir):
                os.makedirs(self.db_dir)
            
            image_path = os.path.join(self.db_dir, f"{username}.jpg")
            
            try:
                cv2.imwrite(image_path, self.most_recent_capture_arr)
                print(f"Image saved at {image_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")
                return

            try:
                cursor.execute(query, values)
                con.commit()
                messagebox.showinfo("Success", "Registration successful!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Database error: {err}")
            finally:
                self.register_win.destroy()
                self.main_window.destroy()
                from Home_page import home_page_here
                home_page_here()
        else:
            messagebox.showerror("Error", "No image captured.")


if __name__ == "__main__":
    app = teacher()
    app.start()