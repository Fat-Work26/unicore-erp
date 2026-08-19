from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,TeacherProfile,Teacher,Student,Staff
import os


DEFAULT_USER_PASSWORD = os.getenv('DEFAULT_USER_PASSWORD' )
# =========================================================
# 1. إنشاء استمارة مخصصة لإضافة استاذ (ModelForm)
# =========================================================
class TeacherUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email')
        
    def save(self,commit=True):
            user = super().save(commit=False)
            user.num_inscription = None
            user.type = User.user_type.TEACHER
            user.set_password(DEFAULT_USER_PASSWORD)
            if commit:
                user.save()
            return user    

# =========================================================
# 2. كلاس التحكم والإدارة الخاّص بـ Django Admin
# =========================================================
class CustomTeacherUserAdmin(UserAdmin):
    add_form = TeacherUserCreationForm
    # 1. إظهار حقل role في جدول عرض المستخدمين الخارجي
    list_display = ['username', 'email',  'is_staff']
    
    # 2. إظهار حقل role داخل صفحة تعديل المستخدم
    # fieldsets = UserAdmin.fieldsets + (
    #     ('الصلاحيات والوظيفة', {'fields': ('role',)}),
    # )
    
    # 3. إظهار حقل role في صفحة إنشاء مستخدم جديد
   
    add_fieldsets = (
        ('الصلاحيات و الوظيفة', {
            'classes': ('wide',),             # تنسيق عريض ومريح للاستمارة
            'fields': ('username','email'),  # الحقول المعروضة للإداري في صفحة + Add
        }),
    )

# admin.site.register(User, CustomTeacherUserAdmin)


class TeacherAdmin(CustomTeacherUserAdmin):
    def get_queryset(self,request):
        return super().get_queryset(request).filter(user_type='TEACHER')
    


admin.site.register(Teacher, TeacherAdmin)


class TeacherProfileAdmin(admin.ModelAdmin):
    # الأعمدة التي ستظهر في صفحة الجدول
    list_display = (
        'employee_id', 
        'first_name_ar', 
        'last_name_ar', 
        # 'department', 
        'rank', 
        'joining_date'
    )
    list_display_links = ('employee_id', 'first_name_ar', 'last_name_ar')
    
    # شريط بحث سريع (بالاسم، اللقب، أو الرقم الوظيفي)
    search_fields = ('employee_id', 'first_name_ar', 'last_name_ar')
    
    # شريط تصفية جانبي (حسب القسم أو الرتبة)
    # list_filter = ('department', 'rank')

admin.site.register(TeacherProfile,TeacherProfileAdmin)
# ***************************************************
# Studiants
# ***************************************************
class StudentUserCreationForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ('username','num_inscription')

    def save(self,commit=True):
        user = super().save(commit=False)
        # user.email = None
        user.type =  User.user_type.STUDENT
        user.set_password(DEFAULT_USER_PASSWORD)
        if commit:
            user.save()
        return user   

class CustomStudentUserAdmin(UserAdmin):
    add_form = StudentUserCreationForm
    list_display = ['username','num_inscription']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),             # تنسيق عريض ومريح للاستمارة
            'fields': ('username','num_inscription'),  # الحقول المعروضة للإداري في صفحة + Add
        }),)
        
class StudentAdmin(CustomStudentUserAdmin):
    def get_queryset(self,request):
        return super().get_queryset(request).filter(user_type = 'STUDENT')

admin.site.register(Student, StudentAdmin)





# =========================================================
# 1. إنشاء استمارة مخصصة لإضافة موظف (ModelForm)
# =========================================================
class StaffUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email')
        
    def save(self,commit=True):
            user = super().save(commit=False)
            user.num_inscription = None
            user.type = User.user_type.STAFF
            user.set_password(DEFAULT_USER_PASSWORD)
            if commit:
                user.save()
            return user    

# =========================================================
# 2. كلاس التحكم والإدارة الخاّص بـ Django Admin
# =========================================================
class CustomStaffUserAdmin(UserAdmin):
    add_form = StaffUserCreationForm
    # 1. إظهار حقل role في جدول عرض المستخدمين الخارجي
    list_display = ['username', 'email',  'is_staff']
    
    # 2. إظهار حقل role داخل صفحة تعديل المستخدم
    # fieldsets = UserAdmin.fieldsets + (
    #     ('الصلاحيات والوظيفة', {'fields': ('role',)}),
    # )
    
    # 3. إظهار حقل role في صفحة إنشاء مستخدم جديد
   
    add_fieldsets = (
        ('الصلاحيات و الوظيفة', {
            'classes': ('wide',),             # تنسيق عريض ومريح للاستمارة
            'fields': ('username','email'),  # الحقول المعروضة للإداري في صفحة + Add
        }),
    )
class StaffAdmin(CustomStudentUserAdmin):
    def get_queryset(self,request):
        return super().get_queryset(request).filter(user_type = 'STAFF')

admin.site.register(Staff, StaffAdmin)