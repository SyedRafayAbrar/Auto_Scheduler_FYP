from django.shortcuts import render, redirect
from django.contrib import messages
from Auto_Scheduler import models
from Auto_Scheduler.api import serializers

def ViewTimeTable(request):
    uID = 0
    myuser = None
    if request.session.has_key('user') == False:
        return redirect("scheduler-login")
    else:
        myuser = request.session['user']
        uID = myuser["id"]

    modID = request.POST.get('mod_id')
    data = models.Courses_Module.objects.filter(module=modID).filter(_user=uID)

    return render(request,"Timetable.html",{'data':data})

def TimeTableView(request):

    return render(request,"Timetable.html")