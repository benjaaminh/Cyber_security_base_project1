from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Note
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import urllib.request
import sqlite3
from urllib.parse import urlparse

#import logging
#notesLogger= logging.getLogger("notes_logger")
#passwordlogger= logging.getLogger("password_logger")

@login_required
@csrf_exempt
def addView(request):
	#if request.method == 'GET':	
		#text = request.GET.get('note') #iban is from input
		#Note.objects.create(owner=request.user,note=text)#create new account with user and iban input
	conn = sqlite3.connect("db.sqlite3")
	cursor= conn.cursor()
	text = request.GET.get('note') #iban is from input
	cursor.execute("INSERT INTO notes_note (note, owner_id) VALUES ('%s',%d)" % (text,request.user.id))
	#print("your text: "+text)
	conn.commit()
	#notesLogger.info("New note created: "+text)
	return redirect('/')

@login_required
def homePageView(request):
	#conn = sqlite3.connect("db.sqlite3")
	#cursor= conn.cursor()
	#text = request.GET.get('note') #iban is from input
	#note=cursor.execute("SELECT note FROM notes_note WHERE owner_id='"+str(request.user.id)+"'and note LIKE '%"+str(text)+"%'").fetchall()
	
	note = Note.objects.filter(owner=request.user) #only show users accounts
	context = {'note': note}#pass context to index.html
	return render(request, 'pages/index.html',context)

def changePasswordView(request):
	user=User.objects.get(username=request.GET.get("user"))
	password= request.GET.get('password')
	#print(request.body.decode('utf-8'))
	user.set_password(password)
	user.save()
	#notesLogger.info("user "+user.username+" changed their password")
	return redirect('/')

def csrfView(request):
	return render(request,'pages/csrf.html')