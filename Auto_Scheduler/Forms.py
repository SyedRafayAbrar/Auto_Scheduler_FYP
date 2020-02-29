from django import forms
from Auto_Scheduler.models import Users
from Auto_Scheduler.models import Professors
from Auto_Scheduler.models import Time
class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = "__all__"

class ProfessorForm(forms.ModelForm):

    class Meta:
        model = Professors
        fields = "__all__"


class TimeForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = ('start_time', 'end_time')