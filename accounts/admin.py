from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

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
