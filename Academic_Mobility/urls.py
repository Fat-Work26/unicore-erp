from django import views
from django.urls import path
from . import views

app_name = 'Academic_Mobility'

urlpatterns = [
    path('newOrde/',views.newOrder,name='newOrder'),
    path('submitted-applications/', views.list_submitted_applications, name='list_submitted_applications'),
    path('manage-session/', views.manage_mobility_session, name='manage_session'),
]