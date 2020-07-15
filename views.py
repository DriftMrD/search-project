# -*- coding: utf-8 -*- 
from django.shortcuts import render
from django.shortcuts import HttpResponse
from .testSeparate import TextRank
import sys
sys.path.insert(0,'/var/www/project')
import mainControl as mc
#from django.db import connection
import pymysql
import os
# Create your views here.
def index(request):
	ctx={}
	if request.method=="POST":
		question = request.POST.get("question")
		connection= connectdb()
		cursor =connection.cursor()
		tr=TextRank(question,3,0.85,500)
		keyword=tr.all();
		items=""
		for word in keyword:
			items+=word+" "
		cursor.execute("SELECT * FROM Keyword where Keyword='" +items+"';")
		result=cursor.fetchall()
		if(len(result)>0):
				for row in result:
					keyword=row['Keyword']
					answer=row['Answer']
					reference=row['Reference']
		else:
			cursor.execute("SELECT WordID FROM Keyword order by WordID desc;")
			lastID=cursor.fetchone();
			tempID=lastID['WordID']+1
			cursor.execute("insert into Keyword values("+str(tempID)+",'"+items+"','',curdate(),'')")
			connection.commit()
			#Execute your files here.
			#here just test

			#tempResult=['this is update answer',"https://www.bilibili.com/"]
			print("hello")
			tempResult=mc.run(question,tempID)
			print("goodbye")
			print(tempResult)
			answer=tempResult[0]
			print("Answer:")
			reference=tempResult[1]
			print("Reference")
			updateSQL="update Keyword  set Answer=%s , Reference=%s where WordID= "+str(tempID)+" ;"
			cursor.execute(updateSQL,(answer,reference))
			connection.commit()
		
		ctx['question']=question
		ctx['answer']=answer
		ctx['ref']=reference
		connection.close()
	return render(request,"index.html",ctx)


def connectdb():
    print('Connecting...')
    conn = pymysql.connect(
    host = "127.0.0.1",
    user = "x7tz",
    password = "741741",
    database = "search_project",
    charset = 'utf8',
    cursorclass = pymysql.cursors.DictCursor)
    print('Connection successful')

    return conn
