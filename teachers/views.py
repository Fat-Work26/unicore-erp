from django.shortcuts import render
from django.contrib.auth.decorators import login_required



@login_required
def home_teacher(request):
    return render(request,'home_teacher.html')


@login_required
def profile_view(request):
    return render(request, 'teachers/profile.html')    