from django.db import models
from accounts.models import User
from .upload_paths import (
    mobility_admin_file_path,
    mobility_scientific_file_path,
    mobility_report_file_path
)
from django.utils import timezone






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
    




class MobilitySession(models.Model):
    SESSION_TYPES = (
        ('REGULAR', 'دورة عادية'),
        ('EXCEPTIONAL', 'دورة استثنائية'),
    )

    title = models.CharField(max_length=200, verbose_name="عنوان الدورة")
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES, default='REGULAR')
    start_date = models.DateTimeField(verbose_name="تاريخ الفتح")
    end_date = models.DateTimeField(verbose_name="تاريخ الغلق")
    is_active = models.BooleanField(default=True, verbose_name="مفتوحة")
    created_at = models.DateTimeField(auto_now_add=True)
    announcement_url = models.URLField(
        max_length=500, 
        blank=True, 
        null=True, 
        verbose_name="رابط الإعلان الرسمي على الموقع"
    )
    def is_currently_open(self):
        """فحص ما إذا كانت الدورة مفتوحة زمنياً وفائتة تاريخ الغلق"""
        
        # print(f"DEBUG: now={now}, start={self.start_date}, end={self.end_date}")
        now = timezone.localtime(timezone.now())
             
        return self.is_active and (self.start_date <= now <= self.end_date)

    def __str__(self):
        return f"{self.title} ({self.get_session_type_display()})"