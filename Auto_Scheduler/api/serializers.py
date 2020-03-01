from rest_framework import serializers
from  Auto_Scheduler.models import Languages,Time,Days,Day_Time,Rooms,Day_Time_Professor,Professors,Courses,Courses_Professor,Semester,Semester_Courses


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = ('id','name')

class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = ('id','start_time','end_time')

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professors
        fields = ('id','professor_name','professor_email')

class ShowProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = ('id','professor_name','professor_email','availablity')

class Day_Time_prof_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Day_Time_Professor
        fields = ('id','prof','day_time')


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Days
        fields = ('id','day_name')

class Time_DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day_Time
        fields = ('id','day_time','time','day')

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = ('id','room_name','room_capacity','islab')

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ('course_code','course_name','course_capacity')

class Course_ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses_Professor
        fields = ('prof','course')

class Semester_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ('name', 'meetings_per_week')

class Semester_Course_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Semester_Courses
        fields = ('semester','Course','selected_Professor')