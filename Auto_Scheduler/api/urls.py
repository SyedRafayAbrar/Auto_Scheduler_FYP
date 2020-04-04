from django.urls import path, include
from Auto_Scheduler.api.views import LanguageView, updateLanguage,DayView,TimeView,Time_DayView,Delete_Room,Delete_Time_Day,Room_View, professor_view,CoursesView,getCount,register
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns


# router = routers.DefaultRouter()
# router.register('languages', views.LanguageView)
# router.register('times', views.TimeView)
# router.register('Days', views.DayView)
# (?P<pk>[0-9]+)
urlpatterns = [
    path(r'languages', LanguageView.as_view()),
    path(r'update_language', updateLanguage.as_view()),
    path(r'days', DayView.as_view()),
    path(r'time', TimeView.as_view()),
    path(r'getcount', getCount.as_view()),
    path(r'time_day', Time_DayView.as_view()),
    path(r'delete_time_day', Delete_Time_Day.as_view()),
    path(r'room', Room_View.as_view()),
    path(r'delete_room', Delete_Room.as_view()),
    path(r'professors', professor_view.as_view()),
    path(r'courses', CoursesView.as_view()),
    path(r'register', register.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
