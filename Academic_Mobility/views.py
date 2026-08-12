from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import AcademicMobilityOrder
from .forms import AcademicMobilityOrderFormTeacher
# ================================================================

# def newOrder(request):
#     return render(request,'Academic_Mobility/newOrder.html')
   
@login_required(login_url='login')
def newOrder(request):
    if request.method == 'POST':
        # تمرير request.FILES إذا كان هناك رفع ملفات PDF
        form = AcademicMobilityOrderFormTeacher(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False) # إيقاف الحفظ المؤقت حتى إسناد المستخدم
            order.user = request.user       # ربط الطلب بالمستخدم الحالي
            order.save() 
            if 'file1' in request.FILES:
                order.file1 = request.FILES['file1']
            if 'file2' in request.FILES:
                order.file2 = request.FILES['file2']
            order.save()                       # الحفظ النهائي في قاعدة البيانات
            return redirect('newOrder')
    else:
        form = AcademicMobilityOrderFormTeacher()

    return render(request, 'Academic_Mobility/newOrder.html', {'form': form})
   