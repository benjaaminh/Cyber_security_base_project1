from django.contrib.auth.decorators import login_required
from .models import Note
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import sqlite3

#import logging
#notesLogger= logging.getLogger("notes_logger")
#passwordlogger= logging.getLogger("password_logger")

@login_required
def addView(request):
	#if request.method == 'GET':	
		#text = request.GET.get('note') #iban is from input
		#Note.objects.create(owner=request.user,note=text)#create new account with user and iban input
	conn = sqlite3.connect("db.sqlite3")
	cursor= conn.cursor()
	text = request.GET.get('note') #iban is from input
	cursor.execute("INSERT INTO notes_note (note, owner_id) VALUES ('%s',%d)" % (text,request.user.id))
	conn.commit()
	#notesLogger.info("New note created: "+text)
	return redirect('/')

@login_required
def homePageView(request):
	note = Note.objects.filter(owner=request.user) #only show users accounts
	context = {'note': note}#pass context to index.html
	return render(request, 'pages/index.html',context)

def changePasswordView(request):
	#user=User.objects.get(username=request.POST.get("user"))
	#password= request.POST.get('password')
	user=User.objects.get(username=request.GET.get("user"))
	password= request.GET.get('password')
	user.set_password(password)
	user.save()
	#notesLogger.info("user "+user.username+" changed their password")
	return redirect('/')

def csrfView(request):
	return render(request,'pages/csrf.html')