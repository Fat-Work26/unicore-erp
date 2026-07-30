from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    # 1. إظهار حقل role في جدول عرض المستخدمين الخارجي
    list_display = ['username', 'email', 'role', 'is_staff']
    
    # 2. إظهار حقل role داخل صفحة تعديل المستخدم
    fieldsets = UserAdmin.fieldsets + (
        ('الصلاحيات والوظيفة', {'fields': ('role',)}),
    )
    
    # 3. إظهار حقل role في صفحة إنشاء مستخدم جديد
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('الصلاحيات والوظيفة', {'fields': ('role',)}),
    )


admin.site.register(User, CustomUserAdmin)


class TeacherProfileAdmin(admin.ModelAdmin):
    # الأعمدة التي ستظهر في صفحة الجدول
    list_display = (
        'employee_id', 
        'first_name_ar', 
        'last_name_ar', 
        'department', 
        'rank', 
        'joining_date'
    )
    list_display_links = ('employee_id', 'first_name_ar', 'last_name_ar')
    
    # شريط بحث سريع (بالاسم، اللقب، أو الرقم الوظيفي)
    search_fields = ('employee_id', 'first_name_ar', 'last_name_ar')
    
    # شريط تصفية جانبي (حسب القسم أو الرتبة)
    list_filter = ('department', 'rank')

admin.site.register(TeacherProfile,TeacherProfileAdmin)
