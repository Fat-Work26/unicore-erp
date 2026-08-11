from django.db import models
from accounts.models import User

class AcademicMobilityOrder(models.Model):
    user             = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    status           = models.CharField(max_length=12,default='قيد المعالجة')
    is_approved      = models.BooleanField(default=False)
    file1            = models.FileField(upload_to='uploadstage',blank=True) # for creating file input 
    file2            = models.FileField(upload_to='uploadstage',blank=True) # for creating file input 
    notes            = models.CharField(verbose_name=('إضافة ملاحظة'),max_length=255,null=True,blank=True)
    notes1           = models.CharField(verbose_name=('إضافة ملاحظة'),max_length=255,null=True,blank=True)
    updated          = models.DateTimeField(auto_now=True, auto_now_add=False)
    created          = models.DateTimeField(auto_now=False, auto_now_add=True)
    has_updated      = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f"{self.user} - Attestation ({self.created})"
    
