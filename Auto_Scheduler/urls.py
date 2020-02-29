from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns


# router = routers.DefaultRouter()
# router.register('languages', views.LanguageView)
# router.register('times', views.TimeView)
# router.register('Days', views.DayView)
# (?P<pk>[0-9]+)
urlpatterns = [
    # path('',include(router.urls)),
    # path(r'languages', views.LanguageView.as_view()),
    # path(r'update_language', views.updateLanguage.as_view()),
    # path(r'days', views.DayView.as_view()),
    # path(r'time', views.TimeView.as_view()),
    # path(r'time_day', views.Time_DayView.as_view()),
    # path(r'delete_time_day', views.Delete_Time_Day.as_view()),
    # path(r'room', views.Room_View.as_view()),
    # path(r'delete_room', views.Delete_Room.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
