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
from Auto_Scheduler.ViewsCollection import DeleteCourseView,AddSemester

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='scheduler-home'),
    # path('login', views.login,name='scheduler-login'),
    path('professor', views.professor,name='scheduler-professor'),
    path('periods', views.period,name='scheduler-periods'),
    path('room', views.room,name='scheduler-room'),
    path('day', views.day,name='scheduler-days'),
    path('courses', views.course,name='scheduler-course'),
    path('semester', views.semester,name='scheduler-semester'),
    path('addRoom',views.addRoom,name='scheduler-addroom'),#add_Time
    path('addDay',views.addDay,name='scheduler-addDay'),#adddDay
    path('add_Time',views.add_Time,name='scheduler-addTime'),
    path('add_Professor',views.add_Professor,name='scheduler-addProfessor'),
    path('add_Semester',AddSemester.add_Semester,name='scheduler-addSemester'),
    path('addCourse', views.addCourse, name='scheduler-addcourse'),
    path('ViewsCollection/deleteCourse', DeleteCourseView.deleteCourse, name='scheduler-deletecourse'),
    path('api/',include('Auto_Scheduler.api.urls'))
]
