from django.shortcuts import render
#from .forms import FormUserstable
from .models import Userstable
from django.contrib import messages


def Login(request):
    users = Userstable.objects.all()
    if request.method == "POST":
        getuserids = request.POST.get('userid')
        getuserpasswords = request.POST.get('userpassword')
        for login in users:
            if getuserids == login.userid and getuserpasswords == login.userpassword:
                return render(request, 'homepage.html', {'user': users, 'getuserid': getuserids, 'getuserpassword': getuserpasswords})

        return render(request, 'signin.html', {'user': users, 'getuserid': getuserids, 'getuserpassword': getuserpasswords})

    else:
        return render(request, 'signin.html', {'user': users})


def Home(request):
    users = Userstable.objects.all()
    return render(request, 'homepage.html', {'user': users})


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
