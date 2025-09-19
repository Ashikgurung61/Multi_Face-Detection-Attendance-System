import cv2
import numpy as np
import face_recognition as fs
import os
from datetime import datetime, time
import mysql.connector 
from tkinter import *
from mysql.connector import Error
from tkinter import messagebox
#from proto import *
from PIL import Image, ImageTk

con = mysql.connector.connect(host="localhost", user="root", passwd="2020Bca01", database="mca_minor_project")
cursor = con.cursor()
uid = []

def period():
    now = datetime.now().time()
    print(now)
    
    periods = [
        (time(9, 55), time(10, 40)),
        (time(10, 40), time(11, 25)),
        (time(11, 25), time(12, 10)),
        (time(12, 10), time(12, 55)),
        (time(12, 55), time(13, 40)),
        (time(13, 40), time(14, 25)),
        (time(14, 25), time(15, 10)),
        (time(15, 10), time(15, 55))
    ]
    
    for i, (start, end) in enumerate(periods, start=1):
        if start <= now < end:
            return i
    return "extra"

def markAttendance(name):
    if name not in uid:
        uid.append(name)
        print("-------------------------------------\n",uid)


def findEncoding(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fs.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def startRecognition():
    global encodeListKnown, classNames, cap
    path = 'student'
    images = []
    classNames = []
    mylist = os.listdir(path)
    
    for cl in mylist:
        curimg = cv2.imread(f'{path}/{cl}')
        images.append(curimg)
        classNames.append(os.path.splitext(cl)[0])

    encodeListKnown = findEncoding(images)
    
    cap = cv2.VideoCapture(0)  
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 850) 
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 850)
    update_frame()

def update_frame():
    success, img = cap.read()
    if success:
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = fs.face_locations(imgS)
        encodesCurFrame = fs.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = fs.compare_faces(encodeListKnown, encodeFace)
            faceDis = fs.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                y1, x2, y2, x1 = [val * 4 for val in faceLoc]
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                markAttendance(name)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        
        webcam_label.imgtk = imgtk
        webcam_label.configure(image=imgtk)
    webcam_label.after(10, update_frame)

def close_webcam():
    peri = period()
    time = datetime.now()
    date_today = time.date().strftime("%d/%m/%y")
    day_today = time.strftime('%A')
    # print("-----------------------------------------------------Available------------------------------------------\n",uid)

    try:
        while uid:
            if not uid:
                continue
            for name_i in uid:
                value = (name_i, "MCA", day_today, date_today, peri, "Present")
                # print(value)
                query = "insert into attendance(uid, department, day, date, period, status) values (%s, %s, %s, %s, %s, %s);"
                cursor.execute(query,value)
                con.commit()
                uid.remove(name_i)
                # print("------------------------------------------------------Remove-----------------------------------", uid)
                
        submit_confirmation = messagebox.askyesnocancel("Attendance Complete", "Submit the attendance")
        # print(submit_confirmation)
        if submit_confirmation == True: 
            root.destroy()
            from Home_page import home_page_here
            home_page_here()

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        # root.destroy()
        # from Home_page import home_page_here
        # home_page_here()
        # #root_okay()
        print("Great Work")


def main():
    global webcam_label, root
    root = Tk()
    root.title("Attendance System")
    root.geometry("1160x654+90+50")

    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=True)

    img_bg = PhotoImage(file="Images/Attendance_bc.png")
    ___ = Label(main_frame,image=img_bg)
    ___ .place(x = 0, y = 0)

    please = Label(main_frame, text = "Please wait....", font=("Brittany", 18))
    please.place(x = 500, y = 58)

    webcam_label = Label(main_frame)
    webcam_label.place(x = 480, y = 62)

    close_button = Button(main_frame, text="Check Attendance", command=close_webcam, font=("Arial", 14))
    close_button.place(x = 730, y = 590)

    root.after(500, startRecognition) 
    root.mainloop()

# main()