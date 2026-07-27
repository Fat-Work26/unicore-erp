from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def home(request):
    return render(request,'accounts/home.html')
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST .get('password')

        user = authenticate(request,username=username,password=password)
        if user and user.role:
            login(request,user)
            return home_user(request)
        else:
            return render(request,'accounts/login.html',{'error':'خطأ في المستخدم'})    
    return render(request,'accounts/login.html')
    
def home_user(request):
    if request.user.role == 'TEACHER':
        return render(request,'accounts/teacher_home.html')
    elif request.user.role == 'STUDENT':
        return render(request,'accounts/student_home.html')
    elif request.user.role == 'SUPER_ADMIN':
        return render(request,'accounts/dashboard_super_admin.html')    
    else:
        return redirect('login')
    