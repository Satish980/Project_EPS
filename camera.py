from operator import index
import face_recognition
import cv2
from face_recognition.api import face_distance, face_encodings, face_locations
import numpy as np 
import sqlite3 as z
import datetime as dt

guru_img = face_recognition.load_image_file(r"C:\Users\satish\Desktop\P\P\images\S160552\S160552.jpg")
guru_face_encoding = face_recognition.face_encodings(guru_img)[0]
sat_img = face_recognition.load_image_file(r"C:\Users\satish\Desktop\P\P\images\S160980\S160980.jpg")
sat_face_encoding = face_recognition.face_encodings(sat_img)[0]
ram_img = face_recognition.load_image_file(r"C:\Users\satish\Desktop\P\P\images\S160414\S160414.jpeg")
ram_face_encoding = face_recognition.face_encodings(ram_img)[0]
uday_img = face_recognition.load_image_file(r"C:\Users\satish\Desktop\P\P\images\S160827\S160827.jpeg")
uday_face_encoding = face_recognition.face_encodings(uday_img)[0]

class Video(object):
    def __init__(self,user):
        self.video=cv2.VideoCapture(0)
        self.user = user

    def __del__(self):
        self.video.release()
    def get_frame(self):

        con = z.connect('testquestions.db')
        cur = con.cursor()

        s_id = self.user
        # ct stores current time
        ct = dt.datetime.now() 
        

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
        ret,frame=self.video.read()
       # faces=faceDetect.detectMultiScale(frame, 1.3, 5)
        #resize the frame video for faster recognition
        small_frame = cv2.resize(frame,(0, 0), fx=0.25, fy = 0.25)

        #convert the img from BGR to RGB
        rgb_small_frame = small_frame[:, :, ::-1]

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

        for(top, right, bottom, left), name in zip(face_locations, face_names):
            #Scale back up locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            color = (0,128,0)
            
            if(name==self.user):
                query = "INSERT INTO verification(sid, ename, status, ts) VALUES (?,?,?,?)"
                con.execute(query,(s_id,"Numerical",1,ct))
                con.commit()
                con.close()
            else:
                query = "INSERT INTO verification(sid, ename, status, ts) VALUES (?,?,?,?)"
                con.execute(query,(s_id,"Numerical",0,ct))
                con.commit()
                con.close()



      
            # draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            #draw a label with name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color , cv2.FILLED)
            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255,255,255),1)
            

        ret,jpg=cv2.imencode('.jpg',frame)
        return jpg.tobytes()