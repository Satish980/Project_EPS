#from os import name
from flask import Flask, render_template, Response,request,redirect,url_for
#from camera import Video
import cv2
import imutils
from imutils.video import VideoStream

app=Flask(__name__)
videoStream = VideoStream(src=0).start()

@app.route('/')
def index():
    return render_template("videostream.html")

@app.route("/video")
def video():
    return Response(generateFrames(),mimetype='multipart/x-mixed-replace; boundary=frame')

def generateFrames():
    while True:
        frame = videoStream.read()
        frame = imutils.resize(frame, width=600)
        (flag, encodeImage) = cv2.imencode(".jpg",frame)
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + bytearray(frame) +
         b'\r\n\r\n')

if __name__ == '__main__':
    app.run(debug=True)

