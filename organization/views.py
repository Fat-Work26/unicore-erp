from django.shortcuts import render
from django.http import JsonResponse
from .models import OrganizationalUnit,University

# 1. الدالة التي تقوم بعرض صفحة الـ HTML
def org_chart_view(request):
    return render(request, 'organization/org_chart.html')

# 2. الدالة التي توفر البيانات لـ D3-Org-Chart عبر الـ Fetch API
def get_org_chart_data(request):
    chart_data = []
    
    # 1. إضافة الجامعات أولاً لتكون هي (الجذر الأكبر) للمخطط
    universities = University.objects.all()
    for uni in universities:
        chart_data.append({
            "id": f"univ_{uni.id}", # ميزنا الـ id بكلمة univ حتى لا يختلط مع أرقام الكليات
            "parentId": "",         # فارغ = هذا هو أعلى رأس في الهرم
            "name": uni.name,
            "title": "الجامعة الأم",
        })

    # 2. إضافة الوحدات التنظيمية (الكليات والمصالح)
    units = OrganizationalUnit.objects.all()
    for unit in units:
        # إذا لم يكن للوحدة parent (مثل الكليات)، نربطها بالجامعة الخاصة بها
        if unit.parent:
            parent_id = str(unit.parent.id)
        else:
            parent_id = f"univ_{unit.university.id}"

        chart_data.append({
            "id": str(unit.id),
            "parentId": parent_id,
            "name": unit.name,
            "title": unit.get_unit_type_display(),
        })
        
    return JsonResponse(chart_data, safe=False)