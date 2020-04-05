from django.shortcuts import render, redirect
from django.contrib import messages
from Auto_Scheduler.api import serializers
from Auto_Scheduler.models import Courses,Courses_Professor,Semester,Semester_Courses

def add_Semester(request):
    if request.method == "POST":

        uID = 0
        myuser = None
        if request.session.has_key('user') == False:
            return redirect("scheduler-login")
        else:
            myuser = request.session['user']
            uID = myuser["id"]

        courses = request.POST.getlist('select_Courses')
        mpw = request.POST.get('meetingsperweek')
        name = request.POST.get('name')
        newData = {"name":name,"meetings_per_week":mpw,'_user':uID}
        serializer = serializers.Semester_Serializer(data=newData)
        if serializer.is_valid():
            serializer.save()
        else:
            messages.error(request,'Semester cannot be saved')
            return redirect("scheduler-semester")

        seme = Semester.objects.filter(_user=uID).last()
        for id in courses:
            course_prof = Courses_Professor.objects.filter(id=id).filter(_user=uID)
            if len(course_prof) > 0:
                for c_p in course_prof:
                    course = c_p.course.id
                    professor = c_p.prof.id
                    data = {"semester":seme.id,"Course":course,"selected_Professor":professor,'_user':uID}
                    serializer = serializers.Semester_Course_Serializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        seme.delete()
                        messages.error(request,'Semester cannot be saved')
                        return redirect("scheduler-semester")
        if len(Semester_Courses.objects.filter(semester=seme.id).filter(_user=uID)) > 0:
            messages.success(request,'The Semester is Added')
            return redirect("scheduler-semester")

        return redirect("scheduler-semester")

def delete_Semester(request):
    if request.method == "POST":
        uID = 0
        myuser = None
        if request.session.has_key('user') == False:
            return redirect("scheduler-login")
        else:
            myuser = request.session['user']
            uID = myuser["id"]


        semester_id = request.POST.get('delete_btn')
        semesterObj = Semester.objects.filter(id=semester_id).filter(_user=uID).last()
        try:
            semesterObj.delete()
            messages.success(request, 'The Semester is deleted')
            return redirect("scheduler-semester")
        except:
            messages.error(request, 'Semester Cant be Delete')
            return redirect("scheduler-semester")