from django.shortcuts import render, redirect
from django.contrib import messages
from Auto_Scheduler.api import serializers
from Auto_Scheduler.models import Courses,Courses_Professor,Semester,Semester_Courses

def add_Semester(request):
    if request.method == "POST":
        courses = request.POST.getlist('select_Courses')
        mpw = request.POST.get('meetingsperweek')
        name = request.POST.get('name')
        newData = {"name":name,"meetings_per_week":mpw}
        serializer = serializers.Semester_Serializer(data=newData)
        if serializer.is_valid():
            serializer.save()
        else:
            messages.error(request,'Semester cannot be saved')
            return redirect("scheduler-semester")

        seme = Semester.objects.all().last()
        for id in courses:
            course_prof = Courses_Professor.objects.filter(id=id)
            if len(course_prof) > 0:
                for c_p in course_prof:
                    course = c_p.course.id
                    professor = c_p.prof.id
                    data = {"semester":seme.id,"Course":course,"selected_Professor":professor}
                    serializer = serializers.Semester_Course_Serializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        seme.delete()
                        messages.error(request,'Semester cannot be saved')
                        return redirect("scheduler-semester")
        if len(Semester_Courses.objects.filter(semester=seme.id)) > 0:
            messages.success(request,'The Semester is Added')
            return redirect("scheduler-semester")

        return redirect("scheduler-home")

