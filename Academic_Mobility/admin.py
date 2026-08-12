from django.contrib import admin
from .models import AcademicMobilityOrder


@admin.register(AcademicMobilityOrder)
class AcademicMobilityOrderAdmin(admin.ModelAdmin):
    # Specify the columns to display in the list table
    list_display = ('user', 'notes', 'file1', 'file2', 'created', 'status')
    
    # Optional filtering and search capabilities
    list_filter = ('status', 'created')
    search_fields = ('user__username', 'notes')