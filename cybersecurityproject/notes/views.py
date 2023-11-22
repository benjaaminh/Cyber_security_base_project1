from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Note
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@login_required
@csrf_exempt
def addView(request):
	if request.method == 'GET':	
		text = request.GET.get('note') #iban is from input
		Note.objects.create(owner=request.user,note=text)#create new account with user and iban input
    
	return redirect('/')

@login_required
def homePageView(request):
	note = Note.objects.filter(owner=request.user) #only show users accounts
	context = {'note': note}#pass context to index.html
	return render(request, 'pages/index.html',context)

def changePasswordView(request):
	user=User.objects.get(username=request.GET.get("user"))
	password= request.GET.get('password')
	user.set_password(password)
	user.save()
	return redirect('/')
