from django.shortcuts import render, redirect
from Auto_Scheduler.Forms import UserForm
from Auto_Scheduler.api import serializers
from .models import Languages, Time,Days,Day_Time,Rooms,Professors,Courses,Day_Time_Professor,Courses_Professor,Semester,Semester_Courses


from Auto_Scheduler.models import Users
# Create your views here.

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

def home(request):

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
            d = Day_Time.objects.filter(id=t.id)
            for dt in d:
                avail+=dt.day_time+', '

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

def addRoom(request):
    if request.method == "POST":
        roomname = request.POST.get('room_name')
        room_capacity = request.POST.get('room_capacity')
        isLab = False
        if request.POST.get('lab_switch'):
            isLab = True
        newData = {"room_name": roomname, "room_capacity": room_capacity,"islab":isLab}

        serializer = serializers.RoomSerializer(data=newData)
        if serializer.is_valid():
            try:
                serializer.save()
                return redirect("scheduler-room")
            except:
                return redirect("scheduler-room")
        else:
            return redirect("scheduler-home")

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
                    return redirect("scheduler-periods",{'alert':'Success!!','message':'Time Added'})
                else:
                    return redirect("scheduler-periods",{'alert':'Sorry :(','message':'Some thing went wrong'})
            except:
                return redirect("scheduler-periods",{'alert':'Sorry :(','message':'Some thing went wrong'})

def add_Professor(request):
    if request.method == "POST":

        avail = request.POST.getlist('select_time')
        prof = request.POST.get('name')
        email = request.POST.get('email')

        data = {"professor_name":prof,"professor_email":email}
        serializer = serializers.ProfessorSerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.save()
            except:
                return redirect("scheduler-professor",{'alert':'Sorry :(','message':'Some thing went wrong'})

        else:
            return redirect("scheduler-professor", {'alert': 'Sorry :(', 'message': 'Some thing went wrong'})

        prof_obj = Professors.objects.all().last()
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
                    return redirect("scheduler-professor")

            else:
                return redirect("scheduler-professor")
        if len(Day_Time_Professor.objects.filter(prof=prof_obj.id)) > 0:
            return redirect("scheduler-home")
        return redirect("scheduler-professor")

def addCourse(request):
    if request.method == "POST":

        profs = request.POST.getlist('select_prof')
        code = request.POST.get('course_code')
        name = request.POST.get('course_name')
        capacity = request.POST.get('course_capacity')

        data = {"course_code":code,"course_name":name,"course_capacity":capacity}
        serializer = serializers.CourseSerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.save()

            except:
                return redirect("scheduler-professor")
        else:
            return redirect("scheduler-professor")
        courseObj = Courses.objects.all().last()

        for professor in profs:
            obj = Professors.objects.filter(professor_name=professor)

            for j in obj:
                n_newData = {"prof": j.id, "course": courseObj.id}
                n_serializer = serializers.Course_ProfessorSerializer(data=n_newData)
                if n_serializer.is_valid():
                    try:
                        n_serializer.save()
                    except:
                        return redirect("scheduler-professor")

        if len(Courses_Professor.objects.filter(prof=courseObj.id)) > 0:
            return redirect("scheduler-home")
        return redirect("scheduler-professor")
# class TimeView(viewsets.ModelViewSet):
#     queryset = Time.objects.all()
#     serializer_class = TimeSerializer

# class DayView(viewsets.ModelViewSet):
#     queryset = Days.objects.all()
#     serializer_class = DaySerializer