from django.shortcuts import render
#from .forms import FormUserstable
from .models import Userstable
from django.contrib import messages


def Login(request):
    return render(request, 'signin.html')


def Home(request):
    return render(request, 'homepage.html')


def InsertUser(request):
    if request.method == "POST":
        if request.POST.get('userid') and request.POST.get('userpassword') and request.POST.get('aidifficulty'):
            saverecord = Userstable()
            saverecord.userid = request.POST.get('userid')
            saverecord.userpassword = request.POST.get('userpassword')
            saverecord.aidifficulty = request.POST.get('aidifficulty')
            saverecord.save()
            messages.success(request, 'Record saved')
            return render(request, 'signup.html')
    else:
        messages.success(request, 'Record saved')
        return render(request, 'signup.html')
