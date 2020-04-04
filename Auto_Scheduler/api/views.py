from django.shortcuts import render, redirect
from Auto_Scheduler.Forms import UserForm
from Auto_Scheduler.Forms import ProfessorForm
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from . import serializers
from Auto_Scheduler.Forms import TimeForm
from . import ResponseJSON

from Auto_Scheduler.api.serializers import LanguageSerializer,TimeSerializer,DaySerializer,Semester_Serializer,Semester_Course_Serializer
from Auto_Scheduler.models import Languages, Time,Days,Day_Time,Rooms,Professors,Day_Time_Professor,Courses_Professor,Courses,Semester,Semester_Courses


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

def add_Time(request):
    if request.method == "POST":
        form = TimeForm(request.POST)
        if form.is_valid():
            time = form.save()
            time.start_time = request.POST.get('start_time','default')
            time.end_time = request.POST.get('end_time','default')

            # try:
            time.save()
            return redirect("scheduler-home")
            # except:
            #     return redirect("scheduler-home")

        else:
            form = TimeForm()
            return render("scheduler-home", "", {'form': form})



def login(request):

    return render(request, 'login.html')


def home(request):
    style = "hold-transition sidebar-mini layout-fixed"
    # return render(request, 'blog/about.html', {'title': title})
    return render(request, 'index.html', {'style': style})

def professor(request):

    # return render(request, 'blog/about.html', {'title': title})
    return render(request, 'Professor.html')

def periods(request):

    # return render(request, 'blog/about.html', {'title': title})
    return render(request, 'Period.html')


class professor_view(APIView):
    def get(self, request):
        profs = Professors.objects.all()

        data = []
        for prof in profs:
            avail = []
            time = Day_Time_Professor.objects.filter(prof=prof.id)
            for t in time:
                d = Day_Time.objects.filter(id=t.id)
                for dt in d:
                    avail.append(dt.day_time)

            newdata = {'professor_id':prof.id,'professor_name':prof.professor_name,'professor_email':prof.professor_email,'availability':avail}
            data.append(newdata)
        return Response(ResponseJSON.ResponseJSON(data,True).getResponseJSON())


    def post(self, request):

        avail = request.data.get('professor_availability')
        prof_name = request.data.get('professor_name')
        prof_email = request.data.get('professor_email')

        newData = {'professor_name': prof_name, 'professor_email': prof_email}
        serializer = serializers.ProfessorSerializer(data=newData)
        if serializer.is_valid():
            try:
                serializer.save()
            except:
                return Response({'message': 'Sorry'})


        else:
            return Response({'message': 'Wrong Format'})

        prof_obj = Professors.objects.all().last()

        for i in avail:

            n_newData = {"prof": prof_obj.id, "day_time": i}
            n_serializer = serializers.Day_Time_prof_Serializer(data=n_newData)
            if n_serializer.is_valid():
                try:
                    n_serializer.save()

                except:
                    return Response({'message': 'Sorry in day Time'})

            else:
                return Response({'message': 'Not Valid'})
        if len(Day_Time_Professor.objects.filter(prof=prof_obj.id)) > 0:
            return Response({'message': 'Done'})
        return Response({'message': 'Sorry once again'})


class LanguageView(APIView):
    def get(self,request):
        language = Languages.objects.all()
        serializer = LanguageSerializer(language, many=True)
        return Response(ResponseJSON.ResponseJSON(serializer.data,True).getResponseJSON())

    def post(self,request):
        serializer = serializers.LanguageSerializer(data=request.data)
        prof_name = request.data.get('professor_name')
        if serializer.is_valid():

            try:
                # language = models.Languages.
                serializer.save()
                return Response({'message': 'Done'})
            except:
                return Response({'message': 'Sorry'})
        else:
            return Response({'message': 'Wrong Format'})

class getCount(APIView):
    def get(self,request):
        teacher_count = len(Professors.objects.all())
        course_count = len(Courses.objects.all())
        timeslot_count = len(Day_Time.objects.all())
        rooms_count = len(Rooms.objects.all())
        n_data = {'teacher_count':teacher_count,'course_count':course_count,'timeslot_count':timeslot_count,'rooms_count':rooms_count}
        return Response(ResponseJSON.ResponseJSON(n_data,True).getResponseJSON())

class updateLanguage(APIView):
    def post(self,request):
        lang_id = request.data.get('id')
        lang_name = request.data.get('name')

        language = Languages.objects.filter(id=lang_id)
        if len(language) != 0:
            try:
                # language.name = lang_name
                language.update(name=lang_name)
                return Response({'message': 'updated'})
            except:
                return Response({'message': 'error updating obj'})
        else:
            return Response({'message': 'No obj Found'})



class DayView(APIView):
    def get(self,request):
        days = Days.objects.all()
        serializer = DaySerializer(days, many=True)
        return Response(ResponseJSON.ResponseJSON(serializer.data,True).getResponseJSON())

    def post(self,request):
        serializer = serializers.DaySerializer(data=request.data)
        if serializer.is_valid():
            check_day = Days.objects.filter(day_name= request.data.get('day_name'))
            if len(check_day) > 0:
                return Response({'message': 'already there'})

            time = Time.objects.all()
            if len(time) > 0:
                try:
                    # language = models.Languages.
                    serializer.save()
                except:
                    return Response({'message': 'Sorry'})

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
                                    return Response({'message': 'Sorry in loop'})

                return Response({'message': 'Done'})


            else:
                return Response({'message': 'Please provide a time first'})


        else:
            return Response({'message': 'Wrong Format'})

class TimeView(APIView):
    def get(self,request):
        time = Time.objects.all()
        serializer = TimeSerializer(time, many=True)
        return Response({'data':serializer.data})

    def post(self,request):
        serializer = serializers.TimeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({'message': 'Done'})
            except:
                return Response({'message': 'Sorry'})
        else:
            return Response({'message': 'Wrong Format'})

class Delete_Time_Day(APIView):

    def post(self,request):
        time_id = request.data.get('id')

        timeday = Day_Time.objects.filter(id=time_id)
        if len(timeday) != 0:
            try:
                timeday.delete()
                return Response({'message': 'Deleted'})
            except:
                return Response({'message': 'error deleting obj'})
        else:
            return Response({'message': 'No obj Found'})


class Time_DayView(APIView):
    def get(self,request):
        timeDay = Day_Time.objects.all()
        serializer = serializers.Time_DaySerializer(timeDay, many=True)
        return Response({'data':serializer.data})

class Room_View(APIView):
    def get(self,request):
        rooms = Rooms.objects.all()
        serializer = serializers.RoomSerializer(rooms, many= True)
        return Response(ResponseJSON.ResponseJSON(serializer.data,True).getResponseJSON())

    def post(self, request):
        serializer = serializers.RoomSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({'message': 'Room Added'})
            except:
                return Response({'message': 'Sorry'})
        else:
            return Response({'message': 'Wrong Format'})

class Delete_Room(APIView):

    def post(self,request):
        room_id = request.data.get('id')

        room = Rooms.objects.filter(id=room_id)
        if len(room) != 0:
            try:
                room.delete()
                return Response({'message': 'Deleted'})
            except:
                return Response({'message': 'error deleting obj'})
        else:
            return Response({'message': 'No obj Found'})



class CoursesView(APIView):
    def get(self,request):
        course = Courses.objects.all()

        data = []
        for c in course:
            avail = []
            c_P = Courses_Professor.objects.filter(course=c.id)
            for cp in c_P:
                professor = cp.prof
                # for professor in professors:
                n = {'professor_id':professor.id,'professor_name':professor.professor_name}
                avail.append(n)

            newdata = {'course_id':c.id,'course_code': c.course_code,'course_name': c.course_name, 'course_capacity': c.course_capacity,
                       'availability': avail}
            data.append(newdata)
        return Response(ResponseJSON.ResponseJSON(data,True).getResponseJSON())

    def post(self,request):
        prof_ass = request.data.get('professors')
        course_code = request.data.get('course_code')
        course_name = request.data.get('course_name')
        course_capacity = request.data.get('course_capacity')
        newData = {'course_code':course_code,'course_name': course_name, 'course_capacity': course_capacity}
        serializer = serializers.CourseSerializer(data=newData)
        if serializer.is_valid():
            try:
                serializer.save()
            except:
                return Response({'message': 'Sorry'})


        else:
            return Response({'message': 'Wrong Format'})

        course_obj = Courses.objects.all().last()

        for i in prof_ass:

            n_newData = {"prof": i, "course": course_obj.id}
            n_serializer = serializers.Course_ProfessorSerializer(data=n_newData)
            if n_serializer.is_valid():
                try:
                    n_serializer.save()

                except:
                    return Response({'message': 'Sorry in course Professor'})

            else:
                return Response({'message': n_serializer.errors})
        if len(Courses_Professor.objects.filter(course=course_obj.id)) > 0:
            return Response({'message': 'Done'})
        return Response({'message': 'Sorry once again'})




class SemesterView(APIView):
    def post(self,request):
        courses = request.data.get('select_courses')
        mpw = request.data.get('meetingsperweek')
        name = request.data.get('name')
        newData = {"name": name, "meetings_per_week": mpw}
        serializer = serializers.Semester_Serializer(data=newData)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(ResponseJSON.Error_ResponseJSON("Something is missing",False))

        seme = Semester.objects.all().last()
        for id in courses:
            course_prof = Courses_Professor.objects.filter(id=id)
            if len(course_prof) > 0:
                for c_p in course_prof:
                    course = c_p.course.id
                    professor = c_p.prof.id
                    data = {"semester": seme.id, "Course": course, "selected_Professor": professor}
                    serializer = serializers.Semester_Course_Serializer(data=data)
                    if serializer.is_valid():
                        serializer.save()

                    else:
                        seme.delete()
                        return Response(ResponseJSON.Error_ResponseJSON("Something went wrong",False))

        if len(Semester_Courses.objects.filter(semester=seme.id)) > 0:

            return Response(ResponseJSON.ResponseJSON(None,True))

        return Response(ResponseJSON.Error_ResponseJSON("Something went wrong", False))

# class login(APIView):
#

class register(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {

            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)
    # def post(self,request):
    #     headers = request.headers
    #     return Response(ResponseJSON.ResponseJSON(headers,True).getResponseJSON())