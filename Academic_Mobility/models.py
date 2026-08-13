from django.db import models
from accounts.models import User
from .upload_paths import (
    mobility_admin_file_path,
    mobility_scientific_file_path,
    mobility_report_file_path
)

class AcademicMobilityOrder(models.Model):
    STATUS_CHOICES = [
        ('PENDING','قيد المعالجة'),
        ('APPROVED', 'مقبول'),
        ('REJECTED', 'مرفوض'),
        
    ]
    user             = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    is_approved      = models.BooleanField(default=False)
    file1            = models.FileField(upload_to=mobility_admin_file_path,blank=True) # for creating file input 
    file2            = models.FileField(upload_to=mobility_scientific_file_path,blank=True) # for creating file input 
    notes            = models.CharField(verbose_name=('إضافة ملاحظة'),max_length=255,null=True,blank=True)
    final_report     = models.FileField(upload_to=mobility_report_file_path, blank=True)
    updated          = models.DateTimeField(auto_now=True, auto_now_add=False)
    created          = models.DateTimeField(auto_now=False, auto_now_add=True)
    has_updated      = models.BooleanField(default=False)
    status           = models.CharField(max_length=12,choices=STATUS_CHOICES, default='PENDING', verbose_name="حالة الطلب")
    rejection_reason = models.TextField(blank=True, null=True, verbose_name="سبب الرفض (في حال الرفض)")
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f"{self.user} - Attestation ({self.created})"
    
