from django.shortcuts import render, redirect
from Auto_Scheduler.Forms import UserForm
from Auto_Scheduler.api import serializers
import datetime
from django.contrib import messages
from .models import  Users,Languages, Time,Days,Day_Time,Rooms,Professors,Courses,Day_Time_Professor,Courses_Professor,Semester,Semester_Courses,Temp_Module,Temp_Courses_Module,Module,Courses_Module


from Auto_Scheduler.models import Users
# Create your views here.
def login(request):

    return render(request,"login.html")
    
def logout(request):
    try:
      del request.session['username']
      return redirect("scheduler-login")
    except:
      pass

def loginMethod(request):
    if request.method == "POST":
        passwrd = request.POST.get('password')
        if len(Users.objects.filter(uName="admin")) > 0:
            u = Users.objects.filter(uName="admin").last()
            if u.password == passwrd:
                request.session['username'] = "admin"
                return redirect("scheduler-home")
            else:
                messages.error(request,'Incorrect Password')
                return redirect("scheduler-login")
        else:
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
    profs = Professors.objects.all()
    courses = Courses.objects.all()
    data = []
    for course in courses:
        c_p = Courses_Professor.objects.filter(course=course.id)
        professors = ""
        for c in c_p:
            _professor = c.prof
            professors += _professor.professor_name+", "

        newdata = {'Course_id': course.id,'course_code':course.course_code, 'course_name': course.course_name,
                   'course_capacity': course.course_capacity, 'professors': professors}
        data.append(newdata)
    return render(request, 'Course.html',{'data': data,'professors':profs})

def createTable(request):

    semester_data = []
    semesters = Semester.objects.all()
    for d in semesters:
        courses = Semester_Courses.objects.filter(semester=d.id)
        newdata = {'semester_id': d.id, 'semester_name': d.name,
                    'courses': courses}
        semester_data.append(newdata)

    return render(request, 'createtable.html',{'Semesters': semester_data})

def home(request):
    if request.session.has_key('username') == False:
        return redirect("scheduler-login")
    
    # try:
    #   del request.session['username']
    # except:
    #   pass
    lecturerCount = len(Professors.objects.all())
    roomCount = len(Rooms.objects.all())
    coursesCount = len(Courses.objects.all())
    timeSlots = len(Day_Time.objects.all())
    style = "hold-transition sidebar-mini layout-fixed"
    return render(request, 'index.html', {'lectureCount': lecturerCount, 'roomCount':roomCount, 'courseCount':coursesCount,'timeSlots':timeSlots})

def semester(request):

    semester_data = []
    semesters = Semester.objects.all()
    for d in semesters:
        courses = Semester_Courses.objects.filter(semester=d.id)
        newdata = {'semester_id': d.id, 'semester_name': d.name,
                    'courses_count': len(courses)}
        semester_data.append(newdata)

    courses_data = []
    sem_courses = Courses_Professor.objects.all()
    for s_c in sem_courses:
        s_data = s_c.course.course_name+"-"+s_c.prof.professor_name
        courses_data.append({"str":s_data,"id":s_c.id})
    return render(request, 'Semester.html', {'Semesters': semester_data,"data":courses_data})


def professor(request):


    profs = Professors.objects.all()
    day_t = Day_Time.objects.all()
    data = []
    for prof in profs:
        avail = ""
        time = Day_Time_Professor.objects.filter(prof=prof.id)
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
    time = Time.objects.all()
    # return render(request, 'blog/about.html', {'title': title})
    return render(request, 'Period.html',{'data':time})


def room(request):

    rooms = Rooms.objects.all()
    # data = []
    # for room in rooms:
    #     # singleObj = {'room_id':room.id,'room_name':room.room_name,'room_capacity':room.room_capacity}
    #     data.append(room)
    # return render(request, 'blog/about.html', {'title': title})
    return render(request, 'Room.html',{'data':rooms})

def day(request):
    days = Days.objects.all()
    return render(request, 'Day.html',{'data':days})


def addDay(request):
    if request.method == "POST":
        dayname = request.POST.get('day_name')
        if dayname == "":
            messages.error(request, 'Name Cannot be empty')
            return redirect('scheduler-days')
        data = {'day_name':dayname}
        serializer = serializers.DaySerializer(data=data)
        if serializer.is_valid():
            check_day = Days.objects.filter(day_name= request.POST.get('day_name'))
            if len(check_day) > 0:
                messages.error(request,'Already there')
                return redirect('scheduler-days')

            time = Time.objects.all()
            if len(time) > 0:
                try:
                    # language = models.Languages.
                    serializer.save()
                except:
                    messages.error(request,'Error adding Day')
                    return redirect('scheduler-days')

                days = Days.objects.all()
                for day in days:
                    for t in time:
                        # concat_str = day.day_name+"-"+Time.objects.get(pk=t).values('start_time')+"-"+Time.objects.get(pk=t).values('end_time')

                        concat_str = day.day_name + "-" + t.start_time + "-" + t.end_time
                        check_day_time = Day_Time.objects.filter(day_time=concat_str)
                        if len(check_day_time)==0:
                            newData = {"time":t.id,"day":day.id,"day_time":concat_str}
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
    if request.method == "POST":
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        newData = {"start_time": start_time, "end_time": end_time}
        check = Time.objects.filter(start_time=start_time).filter(end_time=end_time)
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

    data = []
    t_Module = Temp_Module.objects.all()
    for mod in t_Module:
        mods = Temp_Courses_Module.objects.filter(module=mod.id)
        n_data = {'Module_id':mod.id,'Module_data':mods}
        data.append(n_data)

    return render(request,'showtimetable.html',{'data':data})

def saveTimetable(request):
    if request.method == "POST":
        moduleID = request.POST.get('r1')
        _serializers = serializers.Module_Serializer(data={'date_time': datetime.datetime.now()})
        if _serializers.is_valid():
            _serializers.save()
        else:
            messages.error(request, 'Invalid Temp')
            return redirect('scheduler-home')
        current_mod = Module.objects.all().last()
        module = Temp_Courses_Module.objects.filter(module=moduleID)
        for mod in module:
            n_data = {"module":current_mod.id,"course":mod.course.id, "selectedProfessor":mod.selectedProfessor.id, "assignedTime":mod.assignedTime.id,"assigned_room":mod.assigned_room.id}
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

        if len(Courses_Module.objects.filter(module=current_mod.id))>0:
            # messages.success(request, 'Done')
            temp = Temp_Module.objects.all().last()
            temp.delete()
            return redirect('scheduler-home')
        else:
            messages.error(request, 'Please Invalid')
            return redirect('scheduler-showtable')