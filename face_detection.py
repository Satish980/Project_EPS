from operator import index
import face_recognition
import cv2
from face_recognition.api import face_distance, face_encodings, face_locations
import numpy as np 
import time as t
from tkinter import * 
from tkinter import messagebox
import sys
#webcam reference

#captureDevice = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# import the opencv library
#import cv2


# define a video capture object
str_id = input("Enter Your ID: ")
video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
guru_img = face_recognition.load_image_file(r"C:\Users\satish\Desktop\Project_EPS\Flask_Py\images\S160552\S160552.jpg")
guru_face_encoding = face_recognition.face_encodings(guru_img)[0]
print(guru_face_encoding)
sat_img = face_recognition.load_image_file(r"C:\Users\satish\Desktop\Project_EPS\Flask_Py\images\S160980\S160980.jpg")
sat_face_encoding = face_recognition.face_encodings(sat_img)[0]
ram_img = face_recognition.load_image_file(r"C:\Users\satish\Desktop\Project_EPS\Flask_Py\images\S160414\S160414.jpeg")
ram_face_encoding = face_recognition.face_encodings(ram_img)[0]
uday_img = face_recognition.load_image_file(r"C:\Users\satish\Desktop\Project_EPS\Flask_Py\images\S160827\S160827.jpeg")
uday_face_encoding = face_recognition.face_encodings(uday_img)[0]

#known faces array
known_face_encodings = [
    guru_face_encoding,
    sat_face_encoding,
    ram_face_encoding,
    uday_face_encoding
]

known_face_names = [
    "S160552",
    "S160980",
    "S160414",
    "S160827"
]

#variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
c = 0

while True:
    #
    ret, frame = video_capture.read()
    #resize the frame video for faster recognition
    small_frame = cv2.resize(frame,(0, 0), fx=0.25, fy = 0.25)

    #convert the img from BGR to RGB
    rgb_small_frame = small_frame[:, :, ::-1]

    #only process every other frame of video to save time

    if process_this_frame:
        #find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            #checking any face to match
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first face

           # if True in matches:
            #    first_match_index = matches.index(True)
             #   name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            
            face_names.append(name)

    process_this_frame = not process_this_frame


    #Display results
    for(top, right, bottom, left), name in zip(face_locations, face_names):
        #Scale back up locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        if name != "Unknown" and name == str_id:
            color = (0,128,0)

        else:
            color = (0,255,255)
            """root = Tk()
            root.geometry("300x200")
  
            w = Label(root, text ='GeeksForGeeks', font = "50") 
            w.pack()
              
            #messagebox.showinfo("showinfo", "Information")
              
            #messagebox.showwarning("showwarning", "Warning")
              
            messagebox.showerror("Error While Detecting", "Face is not matching with User ID")"""
  
        # draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        #draw a label with name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color , cv2.FILLED)
        font = cv2.FONT_HERSHEY_COMPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255,255,255),1)
        
        if name!=str_id:
            """root = Tk()
            root.geometry("300x200")
  
            w = Label(root, text ='GeeksForGeeks', font = "50") 
            w.pack()"""
              
            #messagebox.showinfo("showinfo", "Information")
              
            #messagebox.showwarning("showwarning", "Warning")
            c += 1
            root = Tk()
            root.withdraw()
            messagebox.showerror("Error While Detecting", "Face is not matching with User ID")
            
            #sys.exit()
            if c == 5:
                sys.exit()
        #cv2.putText(frame,name)
    # x = top, y = right , w = bottom , h = left
    """for ((x, y, w, h), name) in zip(face_locations, face_names):
            x1,y1=x+w, y+h
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1)
            cv2.line(frame, (x,y), (x+30, y),(0,0,255), 6) #Top Left
            cv2.line(frame, (x,y), (x, y+30),(0,0,255), 6)

            cv2.line(frame, (x1,y), (x1-30, y),(0,0,255), 6) #Top Right
            cv2.line(frame, (x1,y), (x1, y+30),(0,0,255), 6)

            cv2.line(frame, (x,y1), (x+30, y1),(0,0,255), 6) #Bottom Left
            cv2.line(frame, (x,y1), (x, y1-30),(0,0,255), 6)

            cv2.line(frame, (x1,y1), (x1-30, y1),(0,0,255), 6) #Bottom right
            cv2.line(frame, (x1,y1), (x1, y1-30),(0,0,255), 6)

            cv2.putText(frame, name, (h+6, w-6), cv2.FONT_HERSHEY_SIMPLEX,
            0.75, (0, 0, 255), 1)"""

    #Display the resulting image
    cv2.imshow('Video',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

