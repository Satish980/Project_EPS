"""@app.route('/saveAns',methods=['POST'])
def saveAns():
    qid=request.form.get('qid')
    ans=request.form.get('answer')
    sub=request.form.get('subject')
    con = z.connect("testquestions.db")
    cur = con.cursor()
    color = 'green'
    status = 'Answered'
    #query = "INSERT INTO questions(bcol,status,useranswer) VALUES(?,?,?) WHERE qid = " + qid
    que = "UPDATE questions SET bcol = ?, status = ?, useranswer = ? WHERE qid = ?"
    try:
      con.execute(que,(color,status,ans,qid))
      con.commit()
      qid += 1
      que = "SELECT * FROM questions WHERE qid = ?"
      quest = con.execute(que,(qid)).fetchall()
      #quest = que.fetchall()
      que2 = "SELECT * FROM questions WHERE subject = ?"
      questList = con.execute(que2,(sub)).fetchall()
      return render_template("testpage.html",questList = questList, quest = quest)
      con.close()

    except Exception as e:
      return "There was an issue updating your task "+str(e)
    
    try:
      db.session.commit()
      questList=questions.query.filter_by(subject=sub).all()
      quest=questions.query.filter_by(qid=qid).first()
      return render_template("testpage.html",questList=questList, quest=quest)  
    except Exception as e:
      return "There was an issue updating your task "+str(e)"""

"""@app.route('/markreview/<string:subject>,<int:qid>')
def markreview(subject,qid):
    quest = questions.query.get_or_404(id)
    qid=request.form.get('qid')
    ans=request.form.get('answer')
    sub=request.form.get('subject')
    quest.useranswer = ans
    quest.bcol = 'yellow'
    try:
      db.session.commit()
      questList=questions.query.filter_by(subject=sub).all()
      qid += 1
      quest=questions.query.filter_by(qid=qid).first()
      return render_template("testpage.html",questList=questList, quest=quest)  
    except:
      return "There was an issue updating your task"""

"""
"""
# for saving answer
#@app.route('/saveAns',methods=["POST"]) 
"""
def saeAns():
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
    #quest.useranswer = ans
    quest.bcol = 'green'
    try:
      db.session.commit()
      questList=questions.query.filter_by(subject=sub).all()
      quest=questions.query.filter_by(qid=qid).first()
      return render_template("testpage.html",questList=questList, quest=quest)  
    except Exception as e:
      return "There was an issue updating your task "+str(e)"""

    #return render_template("testpage.html",questList=questList, quest=quest)  

      """con.close()
      res=session['result']
      res= str(res)+str(qid)+','+str(ans)+','
      session['result']=res
      questList=questions.query.filter_by(subject=sub).all()
      setStatus(questList)
      return showQuest(sub,int(qid)+1)
      #quest=questions.query.filter_by(qid=qid).first()
      #return render_template("testpage.html",questList=questList, quest=quest)""" 


"""@app.route('/test')
def test():
  return render_template('testpage.html')

@app.route('/quiz')
def quiz(): 
    session['result']=""
    subject= "Numerical"
    c = 0
    questList=questions.query.filter_by(subject=subject).all()
    quest=questions.query.filter_by(subject=subject).first()
    return render_template("testpage.html",questList=questList, quest=quest) 
    
    
@app.route("/showQuest/<string:subject>,<int:qid>")
def showQuest(subject,qid):
    con = z.connect("testquestions.db")
    cur = con.cursor()
    q = "UPDATE Logtable SET qnlog = ? WHERE qid = ?"
    
    questList=questions.query.filter_by(subject=subject).all()
    quest=questions.query.filter_by(qid=qid).first()
    #setStatus(questList)
    return render_template("testpage.html",questList=questList, quest=quest)  
    

"""


"""@app.route('/saveAns',methods=["POST"]) 
def saveAns():
    qid=request.form.get('qid')
    ans=request.form.get('answer')
    sub=request.form.get('subject')
    #update the question id and its selected answer in session variable result
    try:
      res=session['result']
      res= res+qid+','+ans+','
      session['result']=res
      questList=questions.query.filter_by(subject=sub).all()
      setStatus(questList)
      quest=questions.query.filter_by(qid=(int(qid) + 1).first())
      return render_template("testpage.html",questList = questList, quest = quest)
    except Exception as e:
      return Response("Error :"+e)

"""
"""
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
    return render_template("testpage.html",questList=questList, quest=quest)  """
