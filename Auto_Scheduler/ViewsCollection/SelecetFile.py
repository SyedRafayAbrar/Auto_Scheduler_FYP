from django.shortcuts import render, redirect
from Auto_Scheduler.Forms import UserForm
import csv, io
from Auto_Scheduler.models import Professors,Courses,Rooms,Day_Time,Time,Days
import datetime
from django.contrib import messages
from Auto_Scheduler.ViewsCollection import  ProfessorView,RoomView,CourseView

def selectFile(request):
    uID = 0
    myuser = None
    if request.session.has_key('user') == False:
        return redirect("scheduler-login")
    else:
        myuser = request.session['user']
        uID = myuser["id"]
        if len(Day_Time.objects.filter(_user=uID)) == 0:
            if len(Time.objects.filter(_user=uID)) == 0:
                return redirect("scheduler-periods")
            elif len(Days.objects.filter(_user=uID)) == 0:
                return redirect("scheduler-days")


    template = "ShowFile.html"
    if request.method == "GET":
        return render(request, template)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    context = []
    professors = []
    rooms = []
    courses = []
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        name=column
        f1=column[1]
        professors.append(column[1])
        rooms.append(column[5])
        n_course = {'Name':column[4],"course_code":column[3],'room':column[5],'capacity':column[6],'professor':column[1],'_user':uID}
        courses.append(n_course)
        f2 = column[2]
        n_c = {'name':name,'email':f1,'fieled':f2}
        # n_c = {'name': name}
        context.append(n_c)

    for room in rooms:
        splList = room.split(" ")
        isLab = False
        isPhysicsLab = False
        if len(Rooms.objects.filter(room_name=splList[3])) > 0:
            continue
        if "SR" in splList[3]:
            isPhysicsLab = True
        if "LAB" in splList[3]:
            isLab = True
        newData = {"room_name": splList[3], "room_capacity": 60, "islab": isLab,
                   "is_physics_lab": isPhysicsLab,'_user':uID}
        RoomView.processRoom(newData)




    for professor in professors:
        if professor == "N/I":
            continue
        if len(Professors.objects.filter(professor_name=professor).filter(_user=uID)) > 0:
            continue
        email = professor+"@gmail.com"

        data = {"professor_name": professor, "professor_email": email, "isPermanant": True,'_user':uID}
        ProfessorView.process_Professor(data,email,True,uID)


    for i in range(0,len(courses)):
        if courses[i]['professor'] == "N/I":
            continue
        if len(Courses.objects.filter(course_name=courses[i]['Name']).filter(_user=uID)) > 0:
            continue
        is_computer_lab = False
        is_physics_lab = False
        if "SR" in courses[i]['room']:
            is_physics_lab = True
        if "LAB" in courses[i]['room']:
            is_computer_lab = True

        prof=[courses[i]['professor']]
        data = {"course_code": courses[i]['course_code'], "course_name": courses[i]['Name'], "course_capacity": courses[i]['capacity'], "course_isLab": is_computer_lab,"course_isPhysics_Lab": is_physics_lab,'_user':uID}
        CourseView.processCourse(data,prof,uID)

    return render(request, template, {"context":context})

