from django.contrib import admin
from .models import University,OrganizationalUnit,Department,Position


admin.site.register(University)

admin.site.register(Department)
admin.site.register(Position)

from django.contrib import admin
from .models import OrganizationalUnit, Department, Position, University

@admin.register(OrganizationalUnit)
class OrganizationalUnitAdmin(admin.ModelAdmin):
    # 1. الأعمدة التي ستظهر في الجدول (من اليمين إلى اليسار)
    list_display = ('name',  'parent', 'unit_type','university', 'code')
    
    # 2. الفلاتر الجانبية لتصفية الكيانات بسرعة
    list_filter = ('unit_type', 'university')
    
    # 3. حقل البحث بالاسم أو الرمز
    search_fields = ('name', 'code')
    
    # 4. ترتيب العناصر حسب التبعية
    ordering = ('university', 'parent', 'name')
