from django.shortcuts import render, redirect

from Auto_Scheduler.api import serializers
from Auto_Scheduler.models import Courses

def deleteCourse(request):
    if request.method == "POST":
        u_id = request.POST.get('delete_btn')

        try:
            Courses.objects.filter(id=u_id).delete()
            return redirect('scheduler-course')
        except:
            return redirect('scheduler-home')
    else:
        return redirect('scheduler-room')