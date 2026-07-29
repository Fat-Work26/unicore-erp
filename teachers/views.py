from django.shortcuts import render

def home_teacher(request):
    return render(request,'home_teacher.html')