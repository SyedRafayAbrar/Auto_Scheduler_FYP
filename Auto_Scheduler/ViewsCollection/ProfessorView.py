from django.shortcuts import render, redirect
from django.contrib import messages
from Auto_Scheduler.api import serializers
from Auto_Scheduler.models import Courses,Courses_Professor,Professors,Semester,Semester_Courses,Day_Time,Day_Time_Professor


def add_Professor(request):
    if request.method == "POST":

        avail = request.POST.getlist('select_time')
        prof = request.POST.get('name')
        email = request.POST.get('email')
        permanant_switch = request.POST.get('permanant_switch')
        if len(Day_Time.objects.all()) == 0:
            messages.error(request, 'Please Add Day and Time First')
            return redirect("scheduler-professor")

        isPermanant = False
        if permanant_switch:
            isPermanant = True

        data = {"professor_name": prof, "professor_email": email, "isPermanant": isPermanant}

        response = process_Professor(data,isPermanant,avail)
        if response["isError"]:
            messages.error(request, response["message"])
            return redirect("scheduler-showFile")
        else:
            messages.success(request, 'The Professor is added')
            return redirect("scheduler-showFile")

def process_Professor(data,isPermanant,avail):
    serializer = serializers.ProfessorSerializer(data=data)
    if serializer.is_valid():
        try:
            serializer.save()
        except:
            return redirect("scheduler-professor")

    else:
        return redirect("scheduler-professor")

    prof_obj = Professors.objects.all().last()
    if not isPermanant:
        for i in avail:

            obj = Day_Time.objects.filter(day_time=i)
            n_newData = {}
            for j in obj:
                n_newData = {"prof": prof_obj.id, "day_time": j.id}

            n_serializer = serializers.Day_Time_prof_Serializer(data=n_newData)
            if n_serializer.is_valid():
                try:
                    n_serializer.save()

                except:
                    return {"isError": True, "message": 'The Professor is cannot be added'}

            else:
                return {"isError": True, "message": "Invalid Serialization"}

    else:
        objects = Day_Time.objects.all()
        for obj in objects:
            n_newData = {"prof": prof_obj.id, "day_time": obj.id}
            n_serializer = serializers.Day_Time_prof_Serializer(data=n_newData)
            if n_serializer.is_valid():
                try:
                    n_serializer.save()

                except:
                  return {"isError":True,"message":"Invalid Serialization"}

            else:
                return {"isError": True, "message": 'The Professor is not added'}


    if len(Day_Time_Professor.objects.filter(prof=prof_obj.id)) > 0:
        return {"isError": False, "message": 'The Professor is added'}
    else:
        return {"isError": False, "message": 'The Professor is not added'}





def delete_Professor(request):
    if request.method == "POST":
        prof_id = request.POST.get('delete_btn')
        professorObj = Professors.objects.filter(id=prof_id).last()
        try:
            professorObj.delete()
            messages.success(request, 'The Professor is deleted')
            return redirect("scheduler-professor")
        except:
            messages.error(request, 'Professor Cant be Delete')
            return redirect("scheduler-professor")