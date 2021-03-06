from django.db import models
import datetime
# Create your models here.
class Users(models.Model):
    id = models.AutoField(primary_key=True)
    uName = models.CharField(max_length=100)
    password = models.CharField(max_length=100,default=None)
    email = models.CharField(max_length=100,default=None)

    class Meta:
        db_table = "Users"


class Time(models.Model):
    id = models.AutoField(primary_key=True)
    start_time = models.CharField(max_length=100,default=None)
    end_time = models.CharField(max_length=100, default=None)
    _user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = "Time"

class Days(models.Model):
    id = models.AutoField(primary_key=True)
    day_name = models.CharField(max_length=100,default=None)
    _user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = "Days"

class Day_Time(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.ForeignKey(Time,on_delete=models.CASCADE,default=None)
    day = models.ForeignKey(Days, on_delete=models.CASCADE, default=None)
    day_time = models.CharField(max_length=200,default=None)
    _user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = "Day_Time"


class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=100,default=None)
    course_name = models.CharField(max_length=100,default=None)
    course_capacity = models.IntegerField(max_length=100,default=None)
    course_isLab = models.BooleanField(default=False)
    course_isPhysics_Lab = models.BooleanField(default=False)
    _user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)
    class Meta:
        db_table = "Courses"

class Professors(models.Model):
    id = models.AutoField(primary_key=True)
    professor_name = models.CharField(max_length=100,default=None)
    professor_email = models.CharField(max_length=100,default=None)
    isPermanant = models.BooleanField(default=False)
    _user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = "Professors"

class Courses_Professor(models.Model):
    id = models.AutoField(primary_key=True)
    prof = models.ForeignKey(Professors,on_delete=models.CASCADE,default=None)
    course = models.ForeignKey(Courses,on_delete=models.CASCADE, default=None)
    _user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)
    class Meta:
        db_table = "Courses_Professor"

class Languages(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,default='General')
    _user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)
    class Meta:
        db_table = "Languages"

class Day_Time_Professor(models.Model):
    id = models.AutoField(primary_key=True)
    prof = models.ForeignKey(Professors,on_delete=models.CASCADE,default=None)
    day_time = models.ForeignKey(Day_Time,on_delete=models.CASCADE,default=None)
    _user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)
    class Meta:
        db_table = "Day_Time_Professor"


class Rooms(models.Model):
    id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=100,default=None)
    room_capacity = models.IntegerField(max_length=100,default=None)
    islab = models.BooleanField(default=False)
    is_physics_lab = models.BooleanField(default=False)
    _user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = "Rooms"

class Semester(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,default=None)
    meetings_per_week = models.IntegerField(default=None)
    _user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = "Semester"

class Semester_Courses(models.Model):
    id = models.AutoField(primary_key=True)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE,default=None)
    Course = models.ForeignKey(Courses,on_delete=models.CASCADE,default=None)
    selected_Professor = models.ForeignKey(Professors,on_delete=models.CASCADE,default=None)
    _user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)


    class Meta:
        db_table = "Semester_Courses"


class Module(models.Model):
    id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default=None)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, default=None)
    fitness = models.IntegerField(default=0)
    _user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)
    class Meta:
        db_table = "Module"

class Courses_Module(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module,on_delete=models.CASCADE,default=None)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, default=None)
    selectedProfessor = models.ForeignKey(Professors, on_delete=models.CASCADE, default=None)
    assignedTime = models.ForeignKey(Day_Time, on_delete=models.CASCADE, default=None)
    assigned_room = models.ForeignKey(Rooms, on_delete=models.CASCADE, default=None)
    _user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = "Courses_Module"

class Temp_Module(models.Model):
    id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default=None)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, default=None)
    fitness = models.IntegerField(default=0)
    _user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = "Temp_Module"

class Temp_Courses_Module(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Temp_Module,on_delete=models.CASCADE,default=None)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, default=None)
    selectedProfessor = models.ForeignKey(Professors, on_delete=models.CASCADE, default=None)
    assignedTime = models.ForeignKey(Day_Time, on_delete=models.CASCADE, default=None)
    assigned_room = models.ForeignKey(Rooms, on_delete=models.CASCADE, default=None)
    _user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)


    class Meta:
        db_table = "Temp_Courses_Module"

class IpAddresses(models.Model):
    id = models.AutoField(primary_key=True)
    ip_address = models.CharField(max_length=100, default=None)

    class Meta:
        db_table = "IpAddresses"