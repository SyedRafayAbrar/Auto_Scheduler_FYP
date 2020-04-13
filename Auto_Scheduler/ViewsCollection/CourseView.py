from django.shortcuts import render, redirect
from django.contrib import messages
from Auto_Scheduler.api import serializers
from Auto_Scheduler.models import Courses,Courses_Professor,Professors,Semester,Semester_Courses,Day_Time,Day_Time_Professor

def addCourse(request):
    if request.method == "POST":
        uID = 0
        myuser = None
        if request.session.has_key('user') == False:
            return redirect("scheduler-login")
        else:
            myuser = request.session['user']
            uID = myuser["id"]

        profs = request.POST.getlist('select_prof')
        code = request.POST.get('course_code')
        name = request.POST.get('course_name')
        capacity = request.POST.get('course_capacity')
        is_computer_lab = request.POST.get('computer_switch') if request.POST.get('computer_switch') == True else False
        is_physics_lab = request.POST.get('physics_switch') if request.POST.get('physics_switch') == True else False

        data = {"course_code":code,"course_name":name,"course_capacity":capacity,"course_isLab":is_computer_lab,"course_isPhysics_Lab":is_physics_lab,"_user":uID}

        response = processCourse(data,profs,uID)
        if response["isError"]:
            messages.error(request, response["message"])
            return redirect("scheduler-course")
        else:
            messages.success(request, 'The Course is added')
            return redirect("scheduler-course")

def processCourse(data,profs,uID):
    serializer = serializers.CourseSerializer(data=data)
    if serializer.is_valid():
        try:
            serializer.save()

        except:
            print(serializer.error_messages)
            return {"isError": True, "message": 'The Course is cannot be added'}
    else:
        print('error in serial2')
        return {"isError": True, "message": 'Error in Course Serialization'}
    courseObj = Courses.objects.filter(_user=uID).last()

    for professor in profs:
        obj = Professors.objects.filter(professor_name=professor).filter(_user=uID)

        for j in obj:
            n_newData = {"prof": j.id, "course": courseObj.id,'_user':uID}
            n_serializer = serializers.Course_ProfessorSerializer(data=n_newData)
            if n_serializer.is_valid():
                try:
                    n_serializer.save()
                except:
                    courseObj.delete()
                    print('error in prof')
                    return {"isError": True, "message": 'Error in Adding Course'}

    if len(Courses_Professor.objects.filter(course=courseObj.id).filter(_user=uID)) > 0:
        return {"isError": False, "message": "Course Added"}

    else:
        print('error')
        return {"isError": True, "message": 'Error in Adding Course'}



def deleteCourse(request):
    if request.method == "POST":
        uID = 0
        myuser = None
        if request.session.has_key('user') == False:
            return redirect("scheduler-login")
        else:
            myuser = request.session['user']
            uID = myuser["id"]

        u_id = request.POST.get('delete_btn')

        try:
            Courses.objects.filter(id=u_id).filter(_user=uID).delete()
            return redirect('scheduler-course')
        except:
            return redirect('scheduler-course')
    else:
        return redirect('scheduler-course')