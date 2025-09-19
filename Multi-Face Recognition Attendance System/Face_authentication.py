from tkinter import *
import cv2
from PIL import Image, ImageTk
from tkinter import messagebox
import os
import subprocess

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#correct
# def login():
#         unknown_img_path = './.tmp.jpg'
#         cv2.imwrite(unknown_img_path, most_recent_capture_arr)
#         output = str(subprocess.check_output(['face_recognition',db_dir, unknown_img_path]))
#         name = output.split(',')[1][:-7]
#         if name in ['unknown_person']:
#             messagebox.showwarning("Error","Try Again Later")
#         else:
#             messagebox.showinfo("Success","Welcome {}".format(name))

#trial
import cv2
import subprocess
from tkinter import messagebox

def login():
    known_img_dir = './db/'  # Directory where known images are saved
    known_img_path = './db'  # Save the captured image with a filename

    cv2.imwrite(known_img_path, most_recent_capture_arr)
    try:
        output = subprocess.check_output(['face_recognition', db_dir, known_img_path])
        output = output.decode('utf-8')
        name = output.split(',')[1].strip()  
        if name in ['known_person']: 
            messagebox.showinfo("Success", "Welcome {}".format(name))
        else:
            messagebox.showwarning("Error", "Try Again Later")
    
    except Exception as e:
        messagebox.showwarning("Error", "Face recognition failed: {}".format(str(e)))

def process_webcam():
        global most_recent_capture_arr
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            most_recent_capture_arr = frame
            img_ = cv2.cvtColor(most_recent_capture_arr, cv2.COLOR_BGR2RGB)  
            most_rect_capture_pil = Image.fromarray(img_)

            imgtk = ImageTk.PhotoImage(image=most_rect_capture_pil)
            _label.imgtk = imgtk
            _label.configure(image=imgtk)
        _label.after(20, process_webcam)

def add_webcam(label):
        global cap, _label
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 700) 
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 620)
        _label = label
        process_webcam()

def log_page():
    global db_dir
    win1 = Tk()
    win1.title("Login")
    win1.geometry("1225x698")

    main_back = PhotoImage(file="Images/face_log.png")
    _ = Label(win1, image= main_back).place(x = 0, y = 0)

    webcam_label = Label(win1, background="black")
    webcam_label.place(x=20, y=100, width=700, height=500)

    add_webcam(webcam_label)
    db_dir = './db'
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)

    login_btn = Button(win1, text="Login",foreground="white", background="green",font=("Times New Roman",20), width=15, command=login)
    login_btn.place(x=800, y=500)

    win1.mainloop()
# log_page()