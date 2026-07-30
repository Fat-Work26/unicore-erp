from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,TeacherProfile
import os


DEFAULT_USER_PASSWORD = os.getenv('DEFAULT_USER_PASSWORD' )
# =========================================================
# 1. إنشاء استمارة مخصصة لإضافة استاذ (ModelForm)
# =========================================================
class TeacherUserCreationForm(forms.ModelForm):
    class Meta:
        models = User
        fields = ('username','mail','role')
        
        def clean(self):
            cleaned_data = super().clean()
        # نضع كلمة مرور افتراضية مؤقتة لتجاوز شروط التحقق الخاصة بـ Django
            if not self.instance.password:
                self.instance.set_password(DEFAULT_USER_PASSWORD)
            return cleaned_data

        def save(self,commit=True):
            user = super().save(commit=False)
            user.set_password(DEFAULT_USER_PASSWORD)
            if commit:
                user.save()
            return user    

# =========================================================
# 2. كلاس التحكم والإدارة الخاّص بـ Django Admin
# =========================================================
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    # 1. إظهار حقل role في جدول عرض المستخدمين الخارجي
    list_display = ['username', 'email', 'role', 'is_staff']
    
    # 2. إظهار حقل role داخل صفحة تعديل المستخدم
    fieldsets = UserAdmin.fieldsets + (
        ('الصلاحيات والوظيفة', {'fields': ('role',)}),
    )
    
    # 3. إظهار حقل role في صفحة إنشاء مستخدم جديد
    # add_fieldsets = UserAdmin.add_fieldsets + (
    #     ('الصلاحيات والوظيفة', {'fields': ('role',)}),
    # )
    add_fieldsets = (
        ('الصلاحيات و الوظيفة', {
            'classes': ('wide',),             # تنسيق عريض ومريح للاستمارة
            'fields': ('username', 'role'),  # الحقول المعروضة للإداري في صفحة + Add
        }),
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
