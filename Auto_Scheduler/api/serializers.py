from rest_framework import serializers
from  Auto_Scheduler.models import Users,Languages,Time,Days,Day_Time,Rooms,Day_Time_Professor,Professors,Courses,Courses_Professor,Semester,Semester_Courses,Temp_Module,Temp_Courses_Module,Module,Courses_Module,IpAddresses

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = ('id','name')

class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = ('id','start_time','end_time','_user')

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professors
        fields = ('id','professor_name','professor_email','isPermanant','_user')

class ShowProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = ('id','professor_name','professor_email','availablity','_user')

class Day_Time_prof_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Day_Time_Professor
        fields = ('id','prof','day_time','_user')


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Days
        fields = ('id','day_name','_user')

class Time_DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day_Time
        fields = ('id','day_time','time','day','_user')

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = ('id','room_name','room_capacity','islab','is_physics_lab','_user')

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ('course_code','course_name','course_capacity','course_isLab','course_isPhysics_Lab','_user')

class Course_ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses_Professor
        fields = ('prof','course','_user')

class Semester_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ('name', 'meetings_per_week','_user')

class Semester_Course_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Semester_Courses
        fields = ('semester','Course','selected_Professor','_user')

class Temp_Module_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Temp_Module
        fields = "__all__"

class Temp__Courses_Module_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Temp_Courses_Module
        fields = ('module', 'course', 'selectedProfessor','assignedTime','assigned_room','_user')

class Module_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"

class Courses_Module_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Courses_Module
        fields = ('module', 'course', 'selectedProfessor','assignedTime','assigned_room','_user')

class IpAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = IpAddresses
        fields = "__all__"