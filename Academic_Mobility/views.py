from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AcademicMobilityOrder
from .forms import AcademicMobilityOrderFormTeacher
from django.contrib import messages
from .permissions import postgrad_vice_dean_required
from .models import MobilitySession
from django.utils import timezone
# ================================================================

@login_required(login_url='login')
def newOrder(request):

    active_session = MobilitySession.objects.filter(is_active=True).first()
    if not active_session or not active_session.is_currently_open():
        messages.error(request, 'عذراً، فترة تقديم طلبات التربص مغلقة حالياً.')
        return render(request, 'Academic_Mobility/newOrder.html', {
            'active_session': active_session
        })
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
            return redirect('Academic_Mobility:newOrder')
       else:
            # Add Error Message if form validation fails
            messages.error(request, 'حدث خطأ أثناء إرسال الطلب، يرجى التحقق من البيانات المدخلة.')    
    else:
        form = AcademicMobilityOrderFormTeacher()

    return render(request, 'Academic_Mobility/newOrder.html', {
        'form': form,
        'active_session': active_session})
   



# ================================================================
@postgrad_vice_dean_required
def list_submitted_applications(request):
    """
    عرض جميع طلبات التربص المودعة لدراستها من طرف نائب العميد
    """
    # جلب جميع الطلبات المودعة (يمكنك تصفيتها حسب الحالة إذا أردت)
    applications = AcademicMobilityOrder.objects.all().order_by('-created')
    
    context = {
        'applications': applications,
    }
    
    return render(request, 'Academic_Mobility/submitted_applications.html', context)


# ================================================================
@postgrad_vice_dean_required                
def manage_mobility_session(request):
    """
    عرض وإنشاء وتمديد دورات التربص
    """
    active_session = MobilitySession.objects.filter(is_active=True).first()

    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
       
        action = request.POST.get('action')

        # 1. فتح دورة جديدة (عادية أو استثنائية)
        if action == 'create':
            # إغلاق أي دورة مفتوحة سابقاً تلقائياً
            MobilitySession.objects.filter(is_active=True).update(is_active=False)

            MobilitySession.objects.create(
                title=request.POST.get('title'),
                session_type=request.POST.get('session_type'),
                start_date = timezone.make_aware(timezone.datetime.fromisoformat(start_date_str)),
                end_date = timezone.make_aware(timezone.datetime.fromisoformat(end_date_str)),
                is_active=True
            )
            messages.success(request, "تم فتح دورة التربص بنجاح.")

        # 2. تمديد الدورة الحالية
        elif action == 'extend' and active_session:
            new_end_date = request.POST.get('new_end_date')
            active_session.end_date = new_end_date
            active_session.save()
            messages.success(request, "تم تمديد تاريخ غلق الدورة بنجاح.")

        # 3. إغلاق الدورة يدوياً
        elif action == 'close' and active_session:
            active_session.is_active = False
            active_session.save()
            messages.warning(request, "تم إغلاق الدورة الحالية.")

        return redirect('Academic_Mobility:manage_session')

    context = {
        'active_session': active_session,
    }
    return render(request, 'Academic_Mobility/manage_session.html', context)

