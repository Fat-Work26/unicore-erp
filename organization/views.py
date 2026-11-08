from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import OrganizationalUnit, PositionAssignment

def org_chart_view(request):
    return render(request, 'organization/org_chart.html')

def get_org_chart_data(request):
    chart_data = []
    building_icon = "https://cdn-icons-png.flaticon.com/512/2231/2231625.png"
    default_person = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

    # جلب جميع الوحدات التنظيمية مع العلاقات المسبقة لتفادي النشر المتكرر للاستعلامات
    units = OrganizationalUnit.objects.select_related('template', 'parent').all()

    for unit in units:
        # 1. تحديد نوع الوحدة وهل هي كلية/جامعة
        unit_type = unit.template.unit_type
        is_building = unit_type in ['UNIVERSITY']

        # 2. تحديد الاسم والعنوان الوظيفي الافتراضي للوحدة
        unit_name = unit.name or unit.template.name
        unit_title = unit.template.get_unit_type_display()
        full_name = ""  # اسم المسؤول النشط (إن وجد)

        # 3. تحديد الصورة المسندة للعقدة (Node)
        image_url = building_icon if is_building else default_person
        
        # البحث عن التكليف النشط الحالي للمنصب الإداري في هذه الوحدة
        active_assignment = PositionAssignment.objects.filter(
            unit=unit, 
            is_active=True
        ).select_related('user', 'position_type').first()

        if active_assignment and not is_building:
            # إحضار الاسم الكامل للمسؤول
            full_name = active_assignment.user.get_full_name() or active_assignment.user.username
            
            # تفصيل العنوان: المسمى الوظيفي للمنصب
            unit_title = active_assignment.position_type.title
            
            # جلب الصورة الشخصية للمسؤول إن وجدت في بروفايله
            if hasattr(active_assignment.user, 'teacher_profile') and active_assignment.user.teacher_profile.photo:
                image_url = active_assignment.user.teacher_profile.photo.url

        # 4. بناء قاموس البيانات الموجه لـ D3-Org-Chart
        chart_data.append({
            "id": str(unit.id),
            "parentId": str(unit.parent.id) if unit.parent else "",
            "unit_name": unit_name,       # اسم الوحدة/المصلحة/القسم
            "full_name": full_name,       # اسم المسؤول الكامل
            "title": unit_title,           # مسمى المنصب أو نوع الكلية
            "image_url": image_url,
            "unit_type": unit_type,
            "node_type": "building" if is_building else "person"
        })

    return JsonResponse(chart_data, safe=False)




def unit_detail_view(request, unit_id):
    # 1. جلب الوحدة التنظيمية المطلوبة
    unit = get_object_or_404(OrganizationalUnit, id=unit_id)
    
    # 2. البحث عن التكليف الإداري النشط حالياً في هذه الوحدة
    active_assignment = unit.assignments.filter(is_active=True).first()
    
    teacher_profile = None
    staff_profile = None
    qualifications = []
    researches = []
    affiliations = []
    staff_qualifications = []
    promotions = []
    regulation = None
    
    if active_assignment:
        # جلب مهام وقوانين المنصب المرتبط بالتكليف
        position_type = active_assignment.position_type
        regulation = getattr(position_type, 'regulation', None)
        user = active_assignment.user

         # جلب بيانات الأستاذ المكلف بالسيرة الذاتية
        if hasattr(user, 'teacher_profile'):
            teacher_profile = user.teacher_profile
            qualifications = teacher_profile.qualifications.all()
            researches = teacher_profile.researches.all()
            affiliations = teacher_profile.affiliations.filter(is_active=True)
        # ب) حالة: المكلف موظف إداري
        elif hasattr(user, 'staff_profile'):
            staff_profile = user.staff_profile
            staff_qualifications = staff_profile.qualifications.all()
            promotions = staff_profile.promotions.all()
    context = {
        'unit': unit,
        'active_assignment': active_assignment,
        'teacher_profile': teacher_profile,
        'staff_profile': staff_profile,
        'qualifications': qualifications,
        'researches': researches,
        'affiliations': affiliations,
        'staff_qualifications': staff_qualifications,
        'promotions': promotions,
        'regulation': regulation,
    }
    
    return render(request, 'organization/unit_detail.html', context)    