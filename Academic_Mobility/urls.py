from django import views
from django.urls import path
from . import views


urlpatterns = [
    path('newOrde',views.newOrder,name='newOrder'),
]