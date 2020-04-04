from django.shortcuts import render, redirect
from django.contrib import messages
from Auto_Scheduler import models
from Auto_Scheduler.api import serializers

def ViewTimeTable(request):

    modID = request.POST.get('mod_id')
    data = models.Courses_Module.objects.filter(module=modID)

    return render(request,"Timetable.html",{'data':data})

def TimeTableView(request):

    return render(request,"Timetable.html")