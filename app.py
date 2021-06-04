from flask import Flask, render_template, Response,request,redirect,url_for,jsonify,flash,session
#from camera import Video
from detection import Video
from models import *
import cv2
from imutils.video import VideoStream


app=Flask(__name__)
#videoStream = VideoStream(src=0).start()
folder_name = "static"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testquestions.db'
app.secret_key = b'hkahs3720/'
db = SQLAlchemy(app)


"""
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
        yield(b'--frame\r\n' b'Content-Type:  image/jpeg\r\n' + bytearray(encodeImage) + b'\r\n')

if __name__ == '__main__':
    app.run(debug=True)


"""
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verifyID')
def verifyID():
    return render_template('verifyid1.html')


@app.route('/softwareinstructions',methods = ['GET', 'POST'])
def softwareinstructions():
  if request.method == "POST":
    return render_template('softwareinstructions.html')



@app.route('/submission')
def submission():
  return render_template('submissionpage.html')



@app.route('/login', methods = ['GET', 'POST'])
def login():
   error = None
   if request.method == 'POST':
      if request.form['sid'] != 'admin' or request.form['pass_w'] != 'admin':
         error = 'Invalid username or password. Please try again!'
      else:
         return redirect(url_for('verifyID'))
   return render_template('index.html', error = error)

def gen(detection):
    while True:
        frame=detection.get_frame()
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')

@app.route('/video')
def video():
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')



#to change color of question buttons and disable 
def setStatus(qlist):
    qAttempt=[]
    strval=session['result'].strip()
    ans=strval.split(',')
    for i in range(int(len(ans)/2)):
        qAttempt.append(int(ans[2*i]))  
    
    """for rw in qlist:
        if rw.qid in qAttempt:
            rw.bcol='green'   # set color
            #rw.status='disabled' # disable
"""



@app.route('/test')
def test():
  return render_template('testpage.html')

@app.route('/quiz')
def quiz(): 
    session['result']=""
    subject= "Numerical"
    questList=questions.query.filter_by(subject=subject).all()
    quest=questions.query.filter_by(subject=subject).first()
    return render_template("testpage.html",questList=questList, quest=quest) 
    
    
@app.route("/showQuest/<string:subject>,<int:qid>")
def showQuest(subject,qid):
    questList=questions.query.filter_by(subject=subject).all()
    quest=questions.query.filter_by(qid=qid).first()
    setStatus(questList)
    return render_template("testpage.html",questList=questList, quest=quest)  
    

# for saving answer
@app.route('/saveAns',methods=["POST"]) 
def saveAns():
    qid=request.form.get('qid')
    ans=request.form.get('answer')
    sub=request.form.get('subject')
    #update the question id and its selected answer in session variable result
    res=session['result']
    res= str(res)+str(qid)+','+str(ans)+','
    session['result']=res
    questList=questions.query.filter_by(subject=sub).all()
    setStatus(questList)
    quest=questions.query.filter_by(qid=qid).first()
    return render_template("testpage.html",questList=questList, quest=quest)  

app.run(debug=True)
