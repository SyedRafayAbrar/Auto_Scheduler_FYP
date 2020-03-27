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
        response = processRoom(newData)
        if response["isError"]:
            messages.error(request, response["message"])
            return redirect("scheduler-room")
        else:
            messages.success(request, 'The Room is added')
            return redirect("scheduler-room")

def processRoom(newData):
    serializer = serializers.RoomSerializer(data=newData)
    if serializer.is_valid():
        try:
            serializer.save()
            return {"isError":False,"message":"Room is Created"}

        except:
            return {"isError":True,"message":"Some thing went wrong"}
    else:
        return {"isError":True,"message":"Invalid Serialization"}

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