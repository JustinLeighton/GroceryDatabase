# cal/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.index, name='index'),
    path('', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.event, name='event_new'),
    path('event/edit/(?P<event_id>\d+)/', views.event, name='event_edit'),
]