from import_export import resources
from . import models

class Course(resources.ModelResource):

    class Meta:
        model = models.Courses
        fields = ('course_code', 'course_name', 'course_capacity', 'course_isLab','course_isPhysics_Lab')