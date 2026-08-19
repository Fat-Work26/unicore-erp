from django.contrib import admin
from .models import OrganizationalTemplate,PositionType,OrganizationalUnit,PositionAssignment


@admin.register(OrganizationalTemplate)
class OrganizationalTemplateAdmin(admin.ModelAdmin):
    list_display = ('name',  'parent_template', 'code')
    search_fields = ('name', 'code')
    ordering = ( 'parent_template', 'name')

@admin.register(OrganizationalUnit)
class OrganizationalUnitAdmin(admin.ModelAdmin):
    # الحقول التي تظهر في القائمة
    list_display = ('get_display_name',  'parent','template')
    
    # تحسين عرض اسم الوحدة
    def get_display_name(self, obj):
        return obj.name or obj.template.name
    get_display_name.short_description = "اسم الوحدة التنظيمية"
    
    search_fields = ('parent',  'name')
    ordering = ( 'parent',  'name')




@admin.register(PositionType)
class PositionTypeAdmin(admin.ModelAdmin):
    list_display = ('title',   'code')
    search_fields = ('title', 'code')
    # ordering = ( 'title')


@admin.register(PositionAssignment)
class PositionAssignmentAdmin(admin.ModelAdmin):
    list_display = ('position_type','unit','user', 'start_date')
    search_fields = ('position_type','unit','user')
    ordering = ( 'position_type','unit','user')


