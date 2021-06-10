import sqlite3 as z
con = z.connect('testquestions.db')

h = "S160827"
query = "SELECT * FROM verification WHERE sid ='" + h + "'"
#query = "INSERT INTO verification(sid, ename, status, ts) VALUES (?,?,?,?)"
cur = con.execute(query)
for row in cur:
    print(row[2])
    
