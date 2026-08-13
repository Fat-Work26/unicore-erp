from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import AcademicMobilityOrder
from .forms import AcademicMobilityOrderFormTeacher
from django.contrib import messages
# ================================================================

# def newOrder(request):
#     return render(request,'Academic_Mobility/newOrder.html')
   
@login_required(login_url='login')
def newOrder(request):
    if request.method == 'POST':
       if(request.user.user_type=='TEACHER'):
          form = AcademicMobilityOrderFormTeacher(request.POST, request.FILES)
       if form.is_valid():
            order = form.save(commit=False) # إيقاف الحفظ المؤقت حتى إسناد المستخدم
            order.user = request.user       # ربط الطلب بالمستخدم الحالي
            order.save() 
            if 'file1' in request.FILES:
                order.file1 = request.FILES['file1']
            if 'file2' in request.FILES:
                order.file2 = request.FILES['file2']
            order.save()   
            messages.success(request, 'تم إرسال الطلب بنجاح!')                    # الحفظ النهائي في قاعدة البيانات
            return redirect('newOrder')
       else:
            # Add Error Message if form validation fails
            messages.error(request, 'حدث خطأ أثناء إرسال الطلب، يرجى التحقق من البيانات المدخلة.')    
    else:
        form = AcademicMobilityOrderFormTeacher()

    return render(request, 'Academic_Mobility/newOrder.html', {'form': form})
   