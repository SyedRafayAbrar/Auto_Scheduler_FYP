from django.shortcuts import render, redirect
from Auto_Scheduler.Forms import UserForm
import csv, io
from Auto_Scheduler.api import serializers
import datetime
from django.contrib import messages
from Auto_Scheduler.ViewsCollection import  ProfessorView

def selectFile(request):
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
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        name=column
        f1=column[1]
        professors.append(column[1])
        rooms.append(column[5])
        n_course = {'Name':column[4],"course_code":column[3],'room':column[5]}
        courses.append(n_course)
        f2 = column[2]
        n_c = {'name':name,'email':f1,'fieled':f2}
        # n_c = {'name': name}
        context.append(n_c)

    for professor in professors:
        email = professor+"@gmail.com"
        profSerial = serializers.ProfessorSerializer
        data = {"professor_name": professor, "professor_email": email, "isPermanant": True}
        response = ProfessorView.process_Professor(data,email,True)
        if response["isError"]:
            messages.error(request, response["message"])
            return redirect("scheduler-professor")
        else:
            messages.success(request, 'The Professor is added')
            return redirect("scheduler-professor")


    return render(request, template, {"context":context})

