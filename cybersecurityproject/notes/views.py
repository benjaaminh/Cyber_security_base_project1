from django.contrib.auth.decorators import login_required
from .models import Note
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import sqlite3

#logging needed!
#import logging
#notesLogger= logging.getLogger("notes_logger")
#passwordlogger= logging.getLogger("password_logger")

@login_required
@csrf_exempt #remove this and add csrf-token in index.html
def addView(request):
	#if request.method == 'POST':	
		#text = request.POST.get('note')
		#Note.objects.create(owner=request.user,note=text)
	conn = sqlite3.connect("db.sqlite3")
	cursor= conn.cursor()
	text = request.POST.get('note') 
	cursor.execute("INSERT INTO notes_note (note, owner_id) VALUES ('%s',%d)" % (text,request.user.id))
	conn.commit()
	#notesLogger.info("New note created: "+text)
	return redirect('/')

@login_required
def homePageView(request):
	note = Note.objects.filter(owner=request.user) #only show users notes
	context = {'note': note}#pass context to index.html
	return render(request, 'pages/index.html',context)

#@login_required
def changePasswordView(request):
	#user = request.user
	#password= request.POST.get('password')
	user=User.objects.get(username=request.GET.get("user"))
	password= request.GET.get('password')
	if (password):
		user.set_password(password)
		user.save()
	
	#notesLogger.info("user "+user.username+" changed their password")
	return redirect('/')

def csrfView(request):
	return render(request,'pages/csrf.html')