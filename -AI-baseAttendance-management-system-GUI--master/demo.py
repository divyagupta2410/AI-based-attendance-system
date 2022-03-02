
#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 5.0.3
#  in conjunction with Tcl version 8.6
#    Mar 26, 2020 01:10:04 PM IST  platform: Windows NT

import sys
import face_recognition as fr
import numpy as np
import os
import cv2
import face_recognition
import tkinter as tk
from tkinter import *
import pandas as pd
import datetime
import time
from PIL import Image,ImageTk
import csv
from tkinter import messagebox




TOLERANCE = 0.5
MODEL = "hog"      # hyperparameter
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import demo_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = arch (root)
    demo_support.init(root, top)
    root.mainloop()

w = None
def create_arch(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_arch(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    top = arch (w)
    demo_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_arch():
    global w
    w.destroy()
    w = None

class arch:


    def clear_func1(self):
        length_1 = len(self.Entry1.get())
        self.Entry1.delete(length_1 - 1, "end")
    def clear_func2(self):
        length_2 = len(self.Entry1_2.get())
        self.Entry1_2.delete(length_2-1, "end")

    #def mail(self):



    def take_images(self):
        print("Enter the Name...")
        name = input()
        os.chdir("faces/")
        os.makedirs(name)
        detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        sampleNum = 0
        while True:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imshow('Frame', img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("k"):
                cv2.imwrite(name + "/" + name + str(sampleNum) +  ".jpg", img[y:y + h, x:x + w ])
                # cv2.imshow('Frame', img)
                sampleNum = sampleNum + 1
            elif key == ord("q"):
                    os.chdir("C:/Users/satya/Desktop/face_recog/")
                    break
        cap.release()
        cv2.destroyAllWindows()
        
    
    def classify_face(self):

        subject = self.Entry1.get()
        room = self.Entry1_2.get()

        if subject == "" or room == "":
            messagebox.showinfo("Error", "Invalid Subject or Room")
        else:
            subject = list(subject.split(" "))
            room = list(room.split(" "))
            def get_encoded_faces():
                encoded = {}

                for dirpath, dnames, fnames in os.walk("./faces"):
                    for f in fnames:
                        if f.endswith(".jpg") or f.endswith(".png"):
                            face = fr.load_image_file("faces/" + f)
                            encoding = fr.face_encodings(face)[0]
                            encoded[f.split(".")[0]] = encoding

                return encoded

            def unknown_image_encoded(img):
                face = fr.load_image_file("faces/" + img)
                encoding = fr.face_encodings(face)[0]

                return encoding
            cap = cv2.VideoCapture(0)
            while True:

                process_this_frame = True

                faces = get_encoded_faces()
                faces_encoded = list(faces.values())
                known_face_names = list(faces.keys())
                ret, img = cap.read()
                # img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
                # img = img[:,:,::-1]
                if process_this_frame:
                    face_locations = face_recognition.face_locations(img, model=MODEL)
                    unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

                    face_names = []
                    for face_encoding in unknown_face_encodings:
                        # See if the face is a match for the known face(s)
                        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
                        name = "Unknown"

                        # use the known face with the smallest distance to the new face
                        face_distances = face_recognition.face_distance(faces_encoded,face_encoding)
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = known_face_names[best_match_index]

                        face_names.append(name)

                process_this_frame = not process_this_frame

                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    # Draw a box around the face
                    cv2.rectangle(img, (left - 20, top - 20), (right + 20, bottom + 20), (255, 0,0), 2)

                    # Draw a label with a name below the face
                    cv2.rectangle(img, (left - 20, bottom - 15), (right + 20, bottom + 20), (255, 0, 0), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(img, name, (left - 20, bottom + 15), font, 1.0, (255, 255, 255), 2)

                # Display the resulting image

                    cv2.imshow('Video', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    #list_joint = face_names + subject + room
                    subjects = subject * len(face_names)
                    room = room * len(face_names)
                    dict = {"Name":face_names, "Subject":subjects, "Classroom":room}
                    df = pd.DataFrame(dict)
                    df.to_csv(str(subject) + ".csv", index = False)
                    break



            cap.release()
            cv2.destroyAllWindows()
        

    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font11 = "-family {@Arial Unicode MS} -size 12"
        font12 = "-family {Segoe UI} -size 15"
        font9 = "-family {Castellar} -size 24 -weight bold -underline "  \
            "1"

        top.geometry("900x600+587+167")
        top.minsize(148, 1)
        top.maxsize(1924, 1055)
        top.resizable(1, 1)
        top.title("A.R.C.H")
        top.configure(background="#000000")

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.0, rely=0.0, height=106, width=902)
        self.Label1.configure(activeforeground="#000000")
        self.Label1.configure(background="#ff0000")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font=font9)
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''A.R.C.H''')

        self.Entry1 = tk.Entry(top)
        self.Entry1.place(relx=0.344, rely=0.217,height=44, relwidth=0.471)
        self.Entry1.configure(background="white")
        self.Entry1.configure(borderwidth="5")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")

        self.enter_name = tk.Label(top)
        self.enter_name.place(relx=0.189, rely=0.217, height=46, width=134)
        self.enter_name.configure(activeforeground="#000000")
        self.enter_name.configure(background="#ff0000")
        self.enter_name.configure(disabledforeground="#a3a3a3")
        self.enter_name.configure(font=font11)
        self.enter_name.configure(foreground="#000000")
        self.enter_name.configure(text='''Subject''')

        self.enter_name_1 = tk.Label(top)
        self.enter_name_1.place(relx=0.189, rely=0.45, height=46, width=135)
        self.enter_name_1.configure(activebackground="#f9f9f9")
        self.enter_name_1.configure(activeforeground="#000000")
        self.enter_name_1.configure(background="#ff0000")
        self.enter_name_1.configure(disabledforeground="#a3a3a3")
        self.enter_name_1.configure(font="-family {@Arial Unicode MS} -size 12")
        self.enter_name_1.configure(foreground="#000000")
        self.enter_name_1.configure(highlightbackground="#d9d9d9")
        self.enter_name_1.configure(highlightcolor="black")
        self.enter_name_1.configure(text='''Room''')

        self.Entry1_2 = tk.Entry(top)
        self.Entry1_2.place(relx=0.344, rely=0.45,height=44, relwidth=0.471)
        self.Entry1_2.configure(background="white")
        self.Entry1_2.configure(borderwidth="5")
        self.Entry1_2.configure(disabledforeground="#a3a3a3")
        self.Entry1_2.configure(font="TkFixedFont")
        self.Entry1_2.configure(foreground="#000000")
        self.Entry1_2.configure(highlightbackground="#d9d9d9")
        self.Entry1_2.configure(highlightcolor="black")
        self.Entry1_2.configure(insertbackground="black")
        self.Entry1_2.configure(selectbackground="#c4c4c4")
        self.Entry1_2.configure(selectforeground="black")

        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.533, rely=0.317, height=33, width=56)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#ff0000")
        self.Button1.configure(borderwidth="5")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Clear''')
        self.Button1.configure(command = self.clear_func1)

        self.Button1_4 = tk.Button(top)
        self.Button1_4.place(relx=0.533, rely=0.55, height=33, width=56)
        self.Button1_4.configure(activebackground="#ececec")
        self.Button1_4.configure(activeforeground="#000000")
        self.Button1_4.configure(background="#ff0000")
        self.Button1_4.configure(borderwidth="5")
        self.Button1_4.configure(disabledforeground="#a3a3a3")
        self.Button1_4.configure(foreground="#000000")
        self.Button1_4.configure(highlightbackground="#d9d9d9")
        self.Button1_4.configure(highlightcolor="black")
        self.Button1_4.configure(pady="0")
        self.Button1_4.configure(text='''Clear''')
        self.Button1_4.configure(command = self.clear_func2)

        self.Button2 = tk.Button(top)
        self.Button2.place(relx=0.389, rely=0.667, height=63, width=306)
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#ff0000")
        self.Button2.configure(borderwidth="5")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(font=font12)
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''Take Attendance''')
        self.Button2.configure(command = self.classify_face)

        self.Button2_5 = tk.Button(top)
        self.Button2_5.place(relx=0.455, rely=0.817, height=63, width=186)
        self.Button2_5.configure(activebackground="#ececec")
        self.Button2_5.configure(activeforeground="#000000")
        self.Button2_5.configure(background="#ff0000")
        self.Button2_5.configure(borderwidth="5")
        self.Button2_5.configure(disabledforeground="#a3a3a3")
        self.Button2_5.configure(font="-family {Segoe UI} -size 15")
        self.Button2_5.configure(foreground="#000000")
        self.Button2_5.configure(highlightbackground="#d9d9d9")
        self.Button2_5.configure(highlightcolor="black")
        self.Button2_5.configure(pady="0")
        self.Button2_5.configure(text='''Take Images''')
        self.Button2_5.configure(command=self.take_images)

        

if __name__ == '__main__':
    vp_start_gui()





