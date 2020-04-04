"""AutoScheduler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from Auto_Scheduler import views
from Auto_Scheduler.ViewsCollection import SemesterView,Algorithm,ProfessorView,CourseView,RoomView,SelecetFile,TimeTable_View

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='scheduler-home'),
    path('register', views.register,name='scheduler-register'),
    path('login', views.login,name='scheduler-login'),

    path('logout', views.logout,name='scheduler-logout'),
    path('loginMethod', views.loginMethod,name='scheduler-loginMethod'),
    path('professor', views.professor,name='scheduler-professor'),
    path('periods', views.period,name='scheduler-periods'),
    path('room', views.room,name='scheduler-room'),
    path('day', views.day,name='scheduler-days'),
    path('courses', views.course,name='scheduler-course'),
    path('semester', views.semester,name='scheduler-semester'),

    path('addRoom',RoomView.addRoom,name='scheduler-addroom'),#add_Time
    path('delete_Room',RoomView.delete_Room,name='scheduler-deleteRoom'),

    path('addDay',views.addDay,name='scheduler-addDay'),#adddDay
    path('add_Time',views.add_Time,name='scheduler-addTime'),
    path('createTable',views.createTable,name='scheduler-createtable'),

    # PROFESSOR
    path('add_Professor',ProfessorView.add_Professor,name='scheduler-addProfessor'),
    path('del_Professor',ProfessorView.delete_Professor,name='scheduler-deleteProfessor'),

    path('add_Semester',SemesterView.add_Semester,name='scheduler-addSemester'),
    path('del_Semester',SemesterView.delete_Semester,name='scheduler-addSemester'),

    path('addCourse', CourseView.addCourse, name='scheduler-addcourse'),
    path('deleteCourse', CourseView.deleteCourse, name='scheduler-deletecourse'),

    path('api/',include('Auto_Scheduler.api.urls')),
    path('show_table',views.showTable,name='scheduler-showtable'),
    path('selectTimetable',views.saveTimetable,name='scheduler-saveTimetable'),
    path('create_Time_Table', Algorithm.create_Time_Table, name='scheduler-createTable'),

    path('showfile', views.showFile, name='scheduler-showFile'),
    path('selectfile', SelecetFile.selectFile, name='scheduler-selectfile'),

    path('timetable', TimeTable_View.TimeTableView, name='scheduler-timetableview'),
    path('view_timetable', TimeTable_View.ViewTimeTable, name='scheduler-viewtimetableview'),


]
