from tkinter import *
import util
import cv2
from tkinter import messagebox
import os
import subprocess
from Home_page import *
from PIL import Image, ImageTk

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class App:
    def __init__(self) -> None:
        self.main_window = Tk()
        self.main_window.geometry("1225x689+80+30")
        self.main_window.title("Login")

        self.main_back = PhotoImage(file="Images/face_log.png")
        self. _ = Label(self.main_window, image= self.main_back).place(x = 0, y = 0)

        self.login_btn = util.get_button(self.main_window, 'Login', "Black", self.login)
        self.login_btn.place(x=800, y=500)

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

    def login(self):
        unknown_img_path = './.temp.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        output = str(subprocess.check_output(['face_recognition',self.db_dir, unknown_img_path]))
        name = output.split(',')[1][:-4]
        if name in ['unknown_img_path']:
            messagebox.showwarning("Error","Try Again Later")
        else:
            messagebox.showinfo("Success","Welcome to Attendance Management System")
            self.main_window.destroy()
            home_page_here()
            
        os.remove(unknown_img_path)

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_rect_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_rect_capture_pil.copy()

if __name__ == "__main__":
    app = App()
    app.start()