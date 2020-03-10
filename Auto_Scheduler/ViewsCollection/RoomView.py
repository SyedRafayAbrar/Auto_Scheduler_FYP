from django.shortcuts import render, redirect
from django.contrib import messages
from Auto_Scheduler.api import serializers
from Auto_Scheduler.models import Rooms


def addRoom(request):
    if request.method == "POST":

        roomname = request.POST.get('room_name')
        room_capacity = request.POST.get('room_capacity')
        isLab = False
        isPhysicsLab = False
        if request.POST.get('physicslab_switch'):
            isPhysicsLab = True
        else:
            isPhysicsLab = False

        if request.POST.get('lab_switch'):
            isLab = True
        newData = {"room_name": roomname, "room_capacity": room_capacity, "islab": isLab,
                   "is_physics_lab": isPhysicsLab}

        serializer = serializers.RoomSerializer(data=newData)
        if serializer.is_valid():
            try:
                serializer.save()
                messages.success(request, 'The room is created')
                return redirect("scheduler-room")
            except:
                return redirect("scheduler-room")
        else:
            messages.error(request, 'Something went wrong')
            return redirect("scheduler-room")

def delete_Room(request):
    if request.method == "POST":
        room_id = request.POST.get('delete_btn')
        roomObj = Rooms.objects.filter(id=room_id).last()
        try:
            roomObj.delete()
            messages.success(request, 'The Room is deleted')
            return redirect("scheduler-room")
        except:
            messages.error(request, 'Room Cant be Delete')
            return redirect("scheduler-room")