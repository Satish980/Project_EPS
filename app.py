from flask import Flask, render_template, Response,request,redirect,url_for,jsonify,flash,session,g
from camera import Video
from models import *
import cv2
from imutils.video import VideoStream
from cameramain import VideoMain
import sqlite3 as z
import datetime as dt


app=Flask(__name__)

folder_name = "static"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testquestions.db'
app.secret_key = b'hkahs3720/'
db = SQLAlchemy(app)


@app.route('/')
def index():
  session['result']=""
  return render_template('index.html')

## Credentials 

@app.route('/login', methods = ['GET', 'POST'])
def login():
   error = "Invalid username or password. Please try again!"
   if request.method == 'POST':
    session.pop('user',None)
    try:
      password = request.form['pass_w']
      uid = request.form['sid']
      credentials = dataset.query.filter_by(ID=str(uid)).first()
      if credentials.Password == password and credentials.ID == uid and credentials.status==0:
        session['user'] = uid
        return redirect(url_for('verifyID')) 
      elif credentials.Password == password and credentials.ID == uid and credentials.status==1:
        return render_template("completion.html")
      else:
        error = 'Invalid username or password. Please try again!'
        print(credentials.password,credentials.uid)
    except:
      return render_template('index.html', error = error)

@app.route('/verifyID')
def verifyID():
    if g.user:
      return render_template('verifyid1.html',user=session['user'])
    return redirect(url_for('index'))

@app.before_request
def before_request():
  g.user = None
  if 'user' in session:
    g.user = session['user']

@app.route('/dropsession')
def dropsession():
  session.pop('user',None)
  return render_template('index.html')


### face vefication code 


@app.route('/face_valid',methods=['POST','GET'])
def face_valid():
  con = z.connect('testquestions.db')
  
  query = "SELECT * FROM verification WHERE sid ='" + session['user'] + "'"
  #query = "INSERT INTO verification(sid, ename, status, ts) VALUES (?,?,?,?)"
  cur = con.execute(query)
  for row in cur:
    stat = row[2]
    break
  if(int(stat)):
    return render_template('examinstructions.html',user=session['user'])
  else:
    error = "Student Face is Not Matching With Student ID"
    return render_template('verifyid1.html',error = error)
  con.close()


@app.route('/submission')
def submission():
  if g.user:
      con = z.connect("testquestions.db")
      cur = con.cursor()
      iD = session['user']
      que = "UPDATE dataset SET status = ? WHERE ID = ?"
      que2 = "UPDATE studentlog SET status = ?, date = ? WHERE sid = ?"
      que3 = "UPDATE questions SET bcol = ?, status = ?, useranswer = ?"
      try:
          con.execute(que,(1,iD))
          con.execute(que2,("Completed",dt.datetime.now(),iD))
          con.commit()
          """qid += 1
          que = "SELECT * FROM questions WHERE qid = ?"
          quest = con.execute(que,(qid)).fetchall()"""
          #quest = que.fetchall()
          return render_template('submissionpage.html',user=session['user'])
      except Exception as e:
          return Response("Exception " + str(e))
  return redirect(url_for('index'))

@app.route('/clear')
def clear():
      con = z.connect("testquestions.db")
      cur = con.cursor()
      iD = session['user']
      que3 = "UPDATE questions SET bcol = ?, status = ?, useranswer = ?"
      try:
          con.execute(que3,("red","Not Answered",""))
          con.commit()
          """qid += 1
          que = "SELECT * FROM questions WHERE qid = ?"
          quest = con.execute(que,(qid)).fetchall()"""
          #quest = que.fetchall()
          return render_template('submissionpage.html',user=session['user'])
      except Exception as e:
          return Response("Exception " + str(e))
  


## Proctoring Window 


def gen(camera):
    while True:
        frame=camera.get_frame()
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')

@app.route('/video')
def video():

    return Response(gen(Video(session['user'])),
    mimetype='multipart/x-mixed-replace; boundary=frame')


### gaze detection code 

def gen_main(cameramain):
    while True:
        frame=cameramain.get_frame()
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')

@app.route('/video_main')

def video_main():
    return Response(gen_main(VideoMain(session['user'])),
    mimetype='multipart/x-mixed-replace; boundary=frame')



## Test Page Functions




@app.route('/quiz')

def quiz(): 
    session['result'] = ""
    subject= "Numerical"
    questList=questions.query.filter_by(subject=subject).all()
    quest=questions.query.filter_by(subject=subject).first()
    return render_template("testpage.html",questList=questList, quest=quest) 
    
    
@app.route("/showQuest/<string:subject>,<int:qid>")
def showQuest(subject,qid):
    questList=questions.query.filter_by(subject=subject).all()
    quest=questions.query.filter_by(qid=qid).first()
    return render_template("testpage.html",questList=questList, quest=quest)  
    

# for saving answer
@app.route('/saveAns',methods=["POST","GET"]) 
def saveAns():
    if request.method == "POST":
      ans = "None"
      qid=request.values.get('qid')
      ans=request.form.get('answer')
      sub=request.form.get('subject')
      #return Response(str(qid)+str(ans)+str(sub))
    #update the question id and its selected answer in session variable result
      con = z.connect("testquestions.db")
      cur = con.cursor()
      #return Response(ans)
      if ans == None:
        if int(qid) == 10:
            return showQuest(sub,1)
        return showQuest(sub,int(qid)+1)
      else:
        color = 'green'
        status = 'Answered'
        #query = "INSERT INTO questions(bcol,status,useranswer) VALUES(?,?,?) WHERE qid = " + qid
        que = "UPDATE questions SET bcol = ?, status = ?, useranswer = ? WHERE qid = ?"
        try:
          con.execute(que,(color,status,ans,qid))
          con.commit()
          if int(qid) == 10:
            return showQuest(sub,1)
          else:
            return showQuest(sub,int(qid)+1)
        except Exception as e:
          return Response("Exception " + str(e))
        

@app.route('/studentlogs')
def studentlogs():
    con = z.connect("testquestions.db")
    cur = con.cursor()
    status = []
    date = []
    sids = []
    color = []
    for row in cur.execute("SELECT * from studentlog"):
        sids.append(row[0])
        status.append(row[2])
        date.append(row[4])
        color.append(row[3])
    con.close()
    return render_template("studentlogs.html",logs = status,date = date,sids=sids,color = color,l=len(color))



## logs
@app.route('/logs')
def logs():
    con = z.connect("testquestions.db")
    cur = con.cursor()
    logs = []
    date = []
    sids = []
    color = []
    for row in cur.execute("SELECT * from Logtable"):
        sids.append(row[1])
        logs.append(row[0])
        date.append(row[2])
        color.append(row[3])
    con.close()
    return render_template("logs.html",logs = logs,date = date,sids=sids,color = color,l=len(color))


app.run(debug=True)
