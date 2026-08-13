from django.db import models
from django.conf import settings


#1. جدول الجامعة / رأس الهرم  
class University(models.Model):
    name = models.CharField(max_length=200,verbose_name="إسم الجامعة")
    code = models.CharField(max_length=20, unique=True, verbose_name="رمز الجامعة")
   
    class Meta:
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
        ('ADMIN_SERVICE', 'مصلحة إدارية / أمانة / عمادة'),
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


# 4. جدول المناصب الإدارية والأكاديمية (الجديد والمكمل)
class Position(models.Model):
    title = models.CharField(max_length=150, verbose_name="عنوان المنصب")
    
    # كود برمجي ثابت نستخدمه في Django Views للتحقق من الصلاحيات
    # مثل: VICE_DEAN_POSTGRAD أو HEAD_OF_DEPT
    code = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="الكود البرمجي للمنصب"
    )
    
    # المنصب قد يكون تابعة لوحدة تنظيمية (كلية/مصلحة) أو قسم أكاديمي مباشر
    unit = models.ForeignKey(
        OrganizationalUnit, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='positions',
        verbose_name="الوحدة التنظيمية / المصلحة"
    )
    department = models.ForeignKey(
        Departement, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='positions',
        verbose_name="القسم الأكاديمي (إن وجد)"
    )
    
    # المنصب الأعلى مباشرة (لبناء الهيكل التنظيمي والشجرة المستقبليّة)
    reports_to = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='subordinates',
        verbose_name="المنصب المسؤول عنه مباشرة"
    )
    
    # الشخص الذي يشغل المنصب حالياً
    current_occupant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='occupying_positions',
        verbose_name="من يشغل المنصب حالياً"
    )

    class Meta:
        verbose_name = "منصب إداري"
        verbose_name_plural = "المناصب الإدارية"

    def __str__(self):
        occupant = self.current_occupant.get_full_name() if self.current_occupant else "شاغر"
        return f"{self.title} ({occupant})"