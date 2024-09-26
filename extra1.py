from tkinter import *
import util
import cv2
from PIL import Image, ImageTk
from tkinter import messagebox
import os
import subprocess

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class App:
    def __init__(self) -> None:
        self.main_window = Tk()
        self.main_window.geometry("1225x689")

        self.main_back = PhotoImage(file="Images/face_log.png")
        self. _ = Label(self.main_window, image= self.main_back).place(x = 0, y = 0)

        self.login_btn = util.get_button(self.main_window, 'Login', "green", self.login)
        self.login_btn.place(x=800, y=500)

        # self.register_btn = util.get_button(self.main_window, 'Register New User', 'gray', self.register, fg='black')
        # self.register_btn.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=20, y=110, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
        
        self._label = label
        self.process_webcam()

    # def process_webcam(self):
    #     ret, frame = self.cap.read()
    #     self.most_recent_capture_arr = frame

    #     img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
    #     self.most_rect_capture_pil = Image.fromarray(img_)

    #     imgtk = ImageTk.PhotoImage(image=self.most_rect_capture_pil)
    #     self._label.imgtk = imgtk
    #     self._label.configure(image=imgtk)

    #     self._label.after(20, self.process_webcam)

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
        unknown_img_path = './.tmp.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        output = str(subprocess.check_output(['face_recognition',self.db_dir, unknown_img_path]))
        name = output.split(',')[1][:-7]
        if name in ['unknown_person']:
            messagebox.showwarning("Error","Try Again Later")
        else:
            messagebox.showinfo("Success","Welcome {}".format(name))
            
        os.remove(unknown_img_path)

    def register(self):
        self.register_win = Toplevel(self.main_window)
        self.register_win.geometry("1200x520+200+105")

        self.accept_button = util.get_button(self.register_win, 'Accept', "green", self.accept_register_new_user)
        self.accept_button.place(x=750, y=300)

        self.try_again_button = util.get_button(self.register_win, 'Try Again', "red", self.try_again_register_new_user)
        self.try_again_button.place(x=750, y=400)

        self.capture_label_ = util.get_img_label(self.register_win)
        self.capture_label_.place(x=10, y=10, width=700, height=500)

        self.add_img_to_label(self.capture_label_)

        self.entry_test_register_new_user = util.get_entry_text(self.register_win)
        self.entry_test_register_new_user.place(x=750, y=150)

        self.text_label__ = util.get_text_label(self.register_win, 'Create Username: ')
        self.text_label__.place(x=750, y=70)

    def try_again_register_new_user(self):
        self.register()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_rect_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_rect_capture_pil.copy()

    def accept_register_new_user(self):
        name = self.entry_test_register_new_user.get(1.0, "end-1c")
    
        if self.most_recent_capture_arr is not None:
            cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.most_recent_capture_arr)
        else:
            messagebox.showerror("Error", "No image captured.")
        messagebox.showinfo("Success","Register Successful")
        self.register_win.destroy()


if __name__ == "__main__":
    app = App()
    app.start()
