from django.db import models

#1. جدول الجامعة / رأس الهرم  
class University(models.Model):
    name = models.CharField(max_length=200,verbose_name="إسم الجامعة")
    code = models.CharField(max_length=20, unique=True, verbose_name="رمز الجامعة")
   
    class meta:
        verbose_name = "جامعة"
        verbose_name_plural = "الجامعات"

    def __str__(self):
        return self.name    



# 2. جدول الوحدات التنظيمية (يشمل الكليات، المخابر، الرئاسة...)
class OrganizationalUnit(models.Model):
    UNIT_TYPE = (
        ('FACULTY', 'كلية'),
        ('PRESIDENCY', 'رئاسة الجامعة'),
        ('LABORATORY', 'مخبر بحث'),
        ('INSTITUTE', 'معهد'),
        ('CENTER', 'مركز خدمة / مكتبة'),
    )
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name='units',
        verbose_name="الجامعة"
    )
    name = models.CharField(max_length=100,verbose_name="إسم الوحدة/ الكيان")
    code = models.CharField(max_length = 20,verbose_name="رمز الوحدة")
    unit_type = models.CharField(max_length =20,
    choices=UNIT_TYPE,
    default='FACULTY',
    verbose_name="نوع الكيان"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sub_units',
        verbose_name="الجهة التابع لها (إن وجدت)")

    class Meta:
        unique_together = ('university','code')
        # verbose_name = "وحدة تنظيمية"   
        # verbose_name_plural = "الوحدات التنظيمية" 
    def __str__(self):
        return f"{self.name} " 
        



class Departement(models.Model):
    unit = models.ForeignKey(
        OrganizationalUnit,
        on_delete=models.CASCADE,
        related_name='departments',
        verbose_name= "الوحدة التنظيمية"
    )   
    name = models.CharField(max_length=100,verbose_name = "اسم القسم/الفرع")
    code = models.CharField(max_length=20 , verbose_name = "رمز القسم")  

    class Meta:
        unique_together = ('unit','code')
        # verbose_name = "قسم / فرع" 
        # verbose_name_plural = " الاقسام و الفروع"  
    def __str__(self):
        return (f"{self.name}-{self.unit.name}")    