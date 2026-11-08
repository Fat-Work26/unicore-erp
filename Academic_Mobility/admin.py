from django.contrib import admin
from .models import AcademicMobilityOrder
from .models import MobilitySession



@admin.register(AcademicMobilityOrder)
class AcademicMobilityOrderAdmin(admin.ModelAdmin):
    # Specify the columns to display in the list table
    list_display = ('user', 'notes', 'file1', 'file2', 'created', 'status')
    
    # Optional filtering and search capabilities
    list_filter = ('status', 'created')
    search_fields = ('user__username', 'notes')


@admin.register(MobilitySession)
class MobilitySessionAdmin(admin.ModelAdmin):
    # الأعمدة التي تظهر في الجدول الرئيسي للوحة التحكم
    list_display = ('title', 'session_type', 'start_date', 'end_date', 'is_active', 'is_currently_open_status')
    
    # خيارات التصفية الجانبية
    list_filter = ('session_type', 'is_active', 'start_date')
    
    # حقول البحث
    search_fields = ('title',)
    
    # الترتيب التلقائي (الأحدث أولاً)
    ordering = ('-start_date',)

    # دالة مخصصة لإظهار حالة الدورة (مفتوحة حالياً أم مغلقة) كعمود معتمد
    @admin.display(boolean=True, description='مفتوحة زمنياً الآن')
    def is_currently_open_status(self, obj):
        return obj.is_currently_open()


