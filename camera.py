import cv2
import face_recognition
import imutils
import pickle
import time
import os


# load the known faces and embeddings saved in last file
data = pickle.loads(open('face_enc', "rb").read())
faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

class Video(object):
    def __init__(self):
        self.video=cv2.VideoCapture(0+cv2.CAP_DSHOW)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        ret,frame=self.video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(60, 60),
                                         flags=cv2.CASCADE_SCALE_IMAGE)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb)
        names = []
        for encoding in encodings:
            matches = face_recognition.compare_faces(data["encodings"],
         encoding)
            name = "Unknown"
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                    name = max(counts, key=counts.get)
                names.append(name)
        
        for ((x, y, w, h), name) in zip(faces, names):
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

            cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
             0.75, (0, 0, 255), 2)
        ret,jpg=cv2.imencode('.jpg',frame)
        return jpg.tobytes()
