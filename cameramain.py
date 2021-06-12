import cv2
import numpy as np
import module as m
import datetime as dt
from models import *
import sqlite3 as z


class VideoMain(object):
    def __init__(self,sid):
        self.video=cv2.VideoCapture(0)
        self.sid = sid
        self.count = 0
        self.fcount = 0
    def __del__(self):
        self.video.release()
    def get_frame(self):
        con = z.connect('testquestions.db')
        cur = con.cursor()

        s_id = self.sid
        # ct stores current time
        ct = dt.datetime.now() 
        color = "info"

        f = self.video.get(cv2.CAP_PROP_FPS)
        width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        ret,frame=self.video.read()

        
        

        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = grayFrame.shape
        circleCenter = (int(width/2), 50)
        image, face = m.faceDetector(frame, grayFrame)

        if face is None:
            self.fcount += 1
            if self.fcount == 10:
                log = "Student Not Present"
                #writing to database that no face found
                color = "danger"
                query = "INSERT INTO Logtable(Log, SID, timeStamp,color) VALUES (?,?,?,?)"
                con.execute(query,(log,s_id,ct,color))
                con.commit()
                con.close()
                self.fcount = 0

        if face is not None:
            image, PointList = m.faceLandmakDetector(frame, grayFrame, face, False)
            RightEyePoint = PointList[36:42]
            LeftEyePoint = PointList[42:48]
            leftRatio, topMid, bottomMid = m.blinkDetector(LeftEyePoint)
            rightRatio, rTop, rBottom = m.blinkDetector(RightEyePoint)

            mask, pos, color = m.EyeTracking(frame, grayFrame, RightEyePoint)
            maskleft, leftPos, leftColor = m.EyeTracking(frame, grayFrame, LeftEyePoint)
            cv2.putText(image, f'{pos}', (35, 95), m.fonts, 0.6, color[1], 2)
            cv2.putText(image, f'{leftPos}', (int(width-140), 95),
                       m.fonts, 0.6, leftColor[1], 2)
            #write to database
            if(pos == "Right" or pos == "Left" or leftPos == "Right" or leftPos == "Left"):
                self.count+=1

            if(self.count==10):
                color = "danger"
                log = "Student Looked at Right : " + pos + " Left: "+ leftPos
                query = "INSERT INTO Logtable(Log, SID, timeStamp,color) VALUES (?,?,?,?)"
                con.execute(query,(log,s_id,ct,color))
                con.commit()
                con.close()
                self.count = 0

        ret,jpg=cv2.imencode('.jpg',frame)
        return jpg.tobytes()
