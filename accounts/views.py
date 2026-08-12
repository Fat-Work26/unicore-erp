from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST .get('password')

        user = authenticate(request,username=username,password=password)
        if user and user.user_type:
            login(request,user)
            return redirect('home_user')
        else:
            return render(request,'accounts/login.html',{'error':'خطأ في المستخدم'})    
    return render(request,'accounts/login.html')

@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def home_user(request):
    if request.user.user_type == 'TEACHER':
        return render(request,'teachers/home_teacher.html')
    elif request.user.user_type == 'STUDENT':
        return render(request,'accounts/student_home.html')
    elif request.user.user_type == 'SUPER_ADMIN':
        return render(request,'accounts/dashboard_super_admin.html')    
    else:
        return redirect('login')
    