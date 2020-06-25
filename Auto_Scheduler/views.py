from django.shortcuts import render, redirect
from Auto_Scheduler.Forms import UserForm
import csv, io

import datetime
from ipware import get_client_ip
from django.contrib import messages
from .models import  Users,Languages,IpAddresses, Time,Days,Day_Time,Rooms,Professors,Courses,Day_Time_Professor,Courses_Professor,Semester,Semester_Courses,Temp_Module,Temp_Courses_Module,Module,Courses_Module
from Auto_Scheduler.api import serializers
from Auto_Scheduler.models import Users

# Create your views here.
def login(request):

    ip, is_routable = get_client_ip(request)
    if ip is None:
    # Unable to get the client's IP address
        print("No ip")
    else:
        data = IpAddresses.objects.filter(ip_address=ip)
        if len(data) == 0:
            serializer = serializers.IpAddressSerializer(data={"ip_address":ip})
            if serializer.is_valid():
                serializer.save()

    print(ip)
    return render(request,"login.html")

def viewProfile(request):

    return render(request,"Profile.html")

def register(request):

    return render(request,"register.html")


def logout(request):
    try:
      del request.session['user']
      return redirect("scheduler-login")
    except:
      pass

def register_Method(request):
    if request.method == "POST":
        name = request.POST.get('fullname')
        email = request.POST.get('email')
        passwrd = request.POST.get('password')

        if name == None or passwrd == None or email == None:
            messages.error(request, 'All fields required')
            return redirect('scheduler-login')


        data = {"uName":name,"password":passwrd,"email":email}
        serializer = serializers.UserSerializer(data=data)
        if serializer.is_valid():
            try:

                serializer.save()
                u = Users.objects.filter(uName=name).last()
                request.session['user'] = {"id":u.id,"uName":name,"password":passwrd,"email":email}
                return redirect('scheduler-home')
            except:
                messages.error(request, 'Unable to save user')
                return redirect('scheduler-register')
        else:
            messages.error(request, 'Invalid data')
            return redirect('scheduler-register')


def loginMethod(request):
    if request.method == "POST":
        passwrd = request.POST.get('password')
        name = request.POST.get('username')
        if name == None or passwrd == None:
            messages.error(request, 'All fields required')
            return redirect('scheduler-login')

        if len(Users.objects.filter(email=name)) > 0:
            u = Users.objects.filter(email=name).last()
            if u.password == passwrd:

                request.session['user'] = {"id":u.id,"uName":u.uName,"password":u.password,"email":u.email}
                return redirect("scheduler-home")
            else:
                messages.error(request,'Incorrect Password')
                return redirect("scheduler-login")
        else:
            messages.error(request, 'User not found')
            return redirect("scheduler-login")

def user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect()
            except:
                pass

        else:
            form = UserForm()
        return render(request, "", {'form': form})

def alert(request):
    return render(request, 'index.html')

def course(request):
    uID = 0
    myuser = None
    if request.session.has_key('user') == False:
        return redirect("scheduler-login")
    else:
        myuser = request.session['user']
        uID = myuser["id"]

    profs = Professors.objects.filter(_user=uID)
    courses = Courses.objects.filter(_user=uID)
    data = []
    for course in courses:
        c_p = Courses_Professor.objects.filter(course=course.id).filter(_user=uID)
        professors = ""
        for c in c_p:
            _professor = c.prof
            professors += _professor.professor_name+", "

        newdata = {'Course_id': course.id,'course_code':course.course_code, 'course_name': course.course_name,
                   'course_capacity': course.course_capacity, 'professors': professors}
        data.append(newdata)
    return render(request, 'Course.html',{'data': data,'professors':profs})

def createTable(request):
    uID = 0
    myuser = None
    if request.session.has_key('user') == False:
        return redirect("scheduler-login")
    else:
        myuser = request.session['user']
        uID = myuser["id"]
    semester_data = []
    semesters = Semester.objects.filter(_user=uID)
    for d in semesters:
        courses = Semester_Courses.objects.filter(semester=d.id).filter(_user=uID)
        newdata = {'semester_id': d.id, 'semester_name': d.name,
                    'courses': courses}
        semester_data.append(newdata)

    return render(request, 'createtable.html',{'Semesters': semester_data})

def home(request):
    uID = 0
    myuser = None
    if request.session.has_key('user') == False:
        return redirect("scheduler-login")
    else:
        myuser = request.session['user']
        uID = myuser["id"]
    
    # try:
    #   del request.session['username']
    # except:
    #   pass
    lecturerCount = len(Professors.objects.filter(_user=uID))
    roomCount = len(Rooms.objects.filter(_user=uID))
    coursesCount = len(Courses.objects.filter(_user=uID))
    timeSlots = len(Day_Time.objects.filter(_user=uID))

    modules = Module.objects.filter(_user=uID)
    semsters = []
    for mod in modules:
        courses = Courses_Module.objects.filter(module=mod.id).filter(_user=uID)
        semester = {'mod_id':mod.id,'semester':mod.semester,'date_time':mod.date_time,'courses':len(courses)}
        semsters.append(semester)

    return render(request, 'index.html', {'lectureCount': lecturerCount, 'roomCount':roomCount, 'courseCount':coursesCount,'timeSlots':timeSlots,'data':semsters,'user':myuser})

def semester(request):
    uID = 0
    myuser = None
    if request.session.has_key('user') == False:
        return redirect("scheduler-login")
    else:
        myuser = request.session['user']
        uID = myuser["id"]

    semester_data = []
    semesters = Semester.objects.filter(_user=uID)
    for d in semesters:
        courses = Semester_Courses.objects.filter(semester=d.id).filter(_user=uID)
        newdata = {'semester_id': d.id, 'semester_name': d.name,
                    'courses_count': len(courses)}
        semester_data.append(newdata)

    courses_data = []
    sem_courses = Courses_Professor.objects.filter(_user=uID)
    for s_c in sem_courses:
        s_data = s_c.course.course_name+"-"+s_c.prof.professor_name
        courses_data.append({"str":s_data,"id":s_c.id})
    return render(request, 'Semester.html', {'Semesters': semester_data,"data":courses_data})

def showFile(request):
    uID = 0
    myuser = None
    if request.session.has_key('user') == False:
        return redirect("scheduler-login")
    else:
        myuser = request.session['user']
        uID = myuser["id"]
    return render(request,'ShowFile.html')


def professor(request):
    uID = 0
    myuser = None
    if request.session.has_key('user') == False:
        return redirect("scheduler-login")
    else:
        myuser = request.session['user']
        uID = myuser["id"]

    profs = Professors.objects.filter(_user=uID)
    day_t = Day_Time.objects.filter(_user=uID)
    data = []
    for prof in profs:
        avail = ""
        time = Day_Time_Professor.objects.filter(prof=prof.id).filter(_user=uID)
        for t in time:
            avail += t.day_time.day_time + " || "

        if prof.isPermanant:
            newdata = {'professor_id': prof.id, 'professor_name': prof.professor_name,
                       'professor_email': prof.professor_email, 'availability': 'Permanant'}
            data.append(newdata)
        else:
            newdata = {'professor_id': prof.id, 'professor_name': prof.professor_name,
                       'professor_email': prof.professor_email, 'availability': avail}
            data.append(newdata)



    return render(request, 'Professor.html',{'data':day_t,'Professors':data})

def period(request):
    uID = 0
    myuser = None
    if request.session.has_key('user') == False:
        return redirect("scheduler-login")
    else:
        myuser = request.session['user']
        uID = myuser["id"]

    time = Time.objects.filter(_user=uID)
    # return render(request, 'blog/about.html', {'title': title})
    return render(request, 'Period.html',{'data':time})

def deletePeriod(request):
    if request.method == "POST":
        uID = 0
        myuser = None
        if request.session.has_key('user') == False:
            return redirect("scheduler-login")
        else:
            myuser = request.session['user']
            uID = myuser["id"]


        period_id = request.POST.get('delete_btn')
        periodObj = Time.objects.filter(id=period_id).filter(_user=uID).last()
        try:
            periodObj.delete()
            messages.success(request, 'The period is deleted')
            return redirect("scheduler-periods")
        except:
            messages.error(request, 'Period Cant be Delete')
            return redirect("scheduler-periods")

def room(request):
    uID = 0
    myuser = None
    if request.session.has_key('user') == False:
        return redirect("scheduler-login")
    else:
        myuser = request.session['user']
        uID = myuser["id"]

    rooms = Rooms.objects.filter(_user=uID)
    # data = []
    # for room in rooms:
    #     # singleObj = {'room_id':room.id,'room_name':room.room_name,'room_capacity':room.room_capacity}
    #     data.append(room)
    # return render(request, 'blog/about.html', {'title': title})
    return render(request, 'Room.html',{'data':rooms})

def day(request):
    uID = 0
    myuser = None
    if request.session.has_key('user') == False:
        return redirect("scheduler-login")
    else:
        myuser = request.session['user']
        uID = myuser["id"]

    days = Days.objects.filter(_user=uID)
    return render(request, 'Day.html',{'data':days})


def addDay(request):
    uID = 0
    myuser = None
    if request.session.has_key('user') == False:
        return redirect("scheduler-login")
    else:
        myuser = request.session['user']
        uID = myuser["id"]

    if request.method == "POST":
        dayname = request.POST.get('day_name')
        if dayname == "":
            messages.error(request, 'Name Cannot be empty')
            return redirect('scheduler-days')

        data = {'day_name':dayname,'_user':uID}
        serializer = serializers.DaySerializer(data=data)
        if serializer.is_valid():

            check_day = Days.objects.filter(day_name= request.POST.get('day_name')).filter(_user=uID)

            if len(check_day) > 0:
                messages.error(request,'Already there')
                return redirect('scheduler-days')


            time = Time.objects.filter(_user=uID)
            if len(time) > 0:
                try:
                    # language = models.Languages.
                    serializer.save()
                except:
                    messages.error(request,'Error adding Day')
                    return redirect('scheduler-days')

                days = Days.objects.filter(_user=uID)
                for day in days:
                    for t in time:
                        # concat_str = day.day_name+"-"+Time.objects.get(pk=t).values('start_time')+"-"+Time.objects.get(pk=t).values('end_time')

                        concat_str = day.day_name + "-" + t.start_time + "-" + t.end_time
                        check_day_time = Day_Time.objects.filter(day_time=concat_str).filter(_user=uID)
                        if len(check_day_time)==0:
                            newData = {"time":t.id,"day":day.id,"day_time":concat_str,"_user":uID}
                            serializer = serializers.Time_DaySerializer(data=newData)
                            if serializer.is_valid():
                                try:
                                    serializer.save()
                                except:
                                    messages.error(request,'Error in Loop')
                                    return redirect('scheduler-days')

                messages.success(request,'Day added Successfully')
                return redirect('scheduler-days')


            else:
                messages.error(request,'Please provide a time first')
                return redirect('scheduler-days')


        else:
            return Response({'message': 'Wrong Format'})


def add_Time(request):
    uID = 0
    myuser = None
    if request.session.has_key('user') == False:
        return redirect("scheduler-login")
    else:
        myuser = request.session['user']
        uID = myuser["id"]

    if request.method == "POST":
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        newData = {"start_time": start_time, "end_time": end_time,"_user":uID}

        check = Time.objects.filter(start_time=start_time).filter(end_time=end_time).filter(_user=uID)
        if len(check) > 0:
            return redirect("scheduler-home")
        else:
            try:
                serializer = serializers.TimeSerializer(data=newData)
                if serializer.is_valid():
                    serializer.save()
                    return redirect("scheduler-periods")
                else:
                    return redirect("scheduler-periods")
            except:
                return redirect("scheduler-periods")



def showTable(request):
    uID = 0
    myuser = None
    if request.session.has_key('user') == False:
        return redirect("scheduler-login")
    else:
        myuser = request.session['user']
        uID = myuser["id"]

    data = []
    t_Module = Temp_Module.objects.filter(_user=uID)
    for mod in t_Module:
        mods = Temp_Courses_Module.objects.filter(module=mod.id).filter(_user=uID)
        n_data = {'Module_id':mod.id,'Module_data':mods,'fitness':mod.fitness}
        data.append(n_data)

    return render(request,'showtimetable.html',{'data':data})

def saveTimetable(request):
    uID = 0
    myuser = None
    if request.session.has_key('user') == False:
        return redirect("scheduler-login")
    else:
        myuser = request.session['user']
        uID = myuser["id"]

    if request.method == "POST":
        moduleID = request.POST.get('r1')
        print(moduleID)
        tempModule = Temp_Module.objects.filter(id=moduleID).filter(_user=uID).last()
        _serializers = serializers.Module_Serializer(data={'date_time': datetime.datetime.now(),'semester':tempModule.semester.id,'fitness':tempModule.fitness,'_user':uID})
        if _serializers.is_valid():
            _serializers.save()
        else:
            messages.error(request, 'Invalid Temp'+tempModule.semester.id)
            return redirect('scheduler-home')
        current_mod = Module.objects.filter(_user=uID).last()
        module = Temp_Courses_Module.objects.filter(module=moduleID).filter(_user=uID)
        for mod in module:
            n_data = {"module":current_mod.id,"course":mod.course.id, "selectedProfessor":mod.selectedProfessor.id, "assignedTime":mod.assignedTime.id,"assigned_room":mod.assigned_room.id,'_user':uID}
            new_serializers = serializers.Courses_Module_Serializer(data=n_data)

            if new_serializers.is_valid():
                try:
                    new_serializers.save()
                except:
                    current_mod.delete()
                    messages.error(request, 'Please Invalid data')
                    return redirect('scheduler-showtable')
            else:
                messages.error(request, 'Please Invalid data')
                return redirect('scheduler-showtable')

        if len(Courses_Module.objects.filter(module=current_mod.id).filter(_user=uID))>0:
            # messages.success(request, 'Done')
            Temp_Courses_Module.objects.filter(_user=uID).delete()
            Temp_Module.objects.filter(_user=uID).delete()
            return redirect('scheduler-home')
        else:
            messages.error(request, 'Please Invalid')
            return redirect('scheduler-showtable')

# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         print("returning FORWARDED_FOR")
#         ip = x_forwarded_for.split(',')[-1].strip()
#     elif request.META.get('HTTP_X_REAL_IP'):
#         print("returning REAL_IP")
#         ip = request.META.get('HTTP_X_REAL_IP')
#     else:
#         print("returning REMOTE_ADDR")
#         ip = request.META.get('REMOTE_ADDR')
#     return ip