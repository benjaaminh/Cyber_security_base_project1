from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Note
from django.shortcuts import render, redirect


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@login_required
def addView(request):
	if request.method == 'POST':	
		text = request.POST.get('note') #iban is from input
		Note.objects.create(owner=request.user,note=text)#create new account with user and iban input
    
	return redirect('/')

@login_required
def homePageView(request):
	note = Note.objects.filter(owner=request.user) #only show users accounts
	context = {'note': note}#pass context to index.html
	return render(request, 'pages/index.html',context)