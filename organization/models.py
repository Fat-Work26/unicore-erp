from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


# 1. جدول الجامعة (رأس الهرم)
class University(models.Model):
    name = models.CharField(max_length=200, verbose_name="إسم الجامعة")
    code = models.CharField(max_length=20, unique=True, verbose_name="رمز الجامعة")

    class Meta:
        verbose_name = "جامعة"
        verbose_name_plural = "الجامعات"

    def __str__(self):
        return self.name


# 2. جدول الوحدات التنظيمية (يشمل الكليات، الأمانة العامة، المكتبة، المصالح)
class OrganizationalUnit(models.Model):
    class UnitType(models.TextChoices):
        FACULTY = 'FACULTY', 'كلية'
        INSTITUTE = 'INSTITUTE', 'معهد'
        VICE_PRESIDENCY = 'VICE_PRESIDENCY', 'نيابة مديرية الجامعة'
        DEANERY = 'DEANERY', 'عمادة الكلية'
        VICE_DEANERY = 'VICE_DEANERY', 'نيابة عمادة'
        SECRETARIAT = 'SECRETARIAT', 'أمانة عامة'
        SERVICE = 'SERVICE', 'مصلحة'
        LABORATORY = 'LABORATORY', 'مخبر / مركز بحث'
        LIBRARY = 'LIBRARY', 'مكتبة'
        OTHER = 'OTHER', 'هيكل آخر'

    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name='units',
        verbose_name="الجامعة"
    )
    name = models.CharField(max_length=150, verbose_name="إسم الوحدة / الكيان")
    code = models.CharField(max_length=50, verbose_name="رمز الوحدة")
    unit_type = models.CharField(
        max_length=30, choices=UnitType.choices, verbose_name='نوع الهيكل'
    )
    # حقل الهرمية لبناء الشجرة (مثلاً: المصلحة تتبع الأمانة العامة أو الكلية)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sub_units',
        verbose_name="الجهة التابع لها إدارياً"
    )
    department = models.ForeignKey(
        'Department',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='administrative_services',
        verbose_name="القسم الأكاديمي التابعة له (إن وجد)"
    )

    class Meta:
        unique_together = ('university', 'code')
        verbose_name = "وحدة تنظيمية"
        verbose_name_plural = "الوحدات التنظيمية"

    def __str__(self):
        if self.parent:
            return f"{self.name} - ({self.parent.name})"
        return f"{self.name}"


# 3. جدول الأقسام الأكاديمية (البيداغوجية)
class Department(models.Model):
    unit = models.ForeignKey(
        OrganizationalUnit,
        on_delete=models.CASCADE,
        related_name='departments',
        verbose_name="الكلية / المعهد التابع له"
    )
    name = models.CharField(max_length=100, verbose_name="اسم القسم / الفرع")
    code = models.CharField(max_length=20, verbose_name="رمز القسم")

    class Meta:
        unique_together = ('unit', 'code')
        verbose_name = "قسم أكاديمي"
        verbose_name_plural = "الأقسام الأكاديمية"

    def __str__(self):
        return f"{self.name} - {self.unit.name}"


# 4. جدول المناصب الإدارية والأكاديمية (الهيكل التسييري)
class Position(models.Model):
    OCCUPANT_TYPES = (
        ('TEACHER', 'أستاذ'),
        ('STAFF', 'موظف إداري'),
    )

    title = models.CharField(max_length=150, verbose_name="عنوان المنصب")
    
    # كود ثبات برمجي نستخدمه في Views لمراجعة الصلاحيات (مثل: DEAN, VICE_DEAN_POSTGRAD, SECRETARY...)
    code = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="الكود البرمجي للمنصب"
    )
    
    # تحديد هل المنصب يشغله أستاذ (كالعميد ورؤساء الأقسام) أم موظف (كالأمين العام ورؤساء المصالح)
    occupant_type = models.CharField(
        max_length=15, 
        choices=OCCUPANT_TYPES, 
        default='STAFF',
        verbose_name="طبيعة الشاغر للمنصب"
    )

    # نطاق المنصب: إما تابع لوحدة تنظيمية (كلية/أمانة/مصلحة) وإما تابع لقسم أكاديمي
    unit = models.ForeignKey(
        OrganizationalUnit, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='positions',
        verbose_name="الوحدة التنظيمية / المصلحة"
    )
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='positions',
        verbose_name="القسم الأكاديمي (إن وجد)"
    )

    # التسلسل القيادي المباشر (لبناء المخطط الهيكلي التفاعلي مستقبلاً)
    reports_to = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='subordinates',
        verbose_name="المنصب الأعلى مسؤوليّة"
    )

    # المستخدم الشخصي الذي يشغل هذا المنصب حالياً
    current_occupant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='occupying_positions',
        verbose_name="من يشغل المنصب حالياً"
    )

    class Meta:
        verbose_name = "منصب إداري / أكاديمي"
        verbose_name_plural = "المناصب الإدارية والأكاديمية"

    def clean(self):
        super().clean()
        # التأكد من ربط المنصب بجهة واحدة فقط (إما وحدة أو قسم)
        if not self.unit and not self.department:
            raise ValidationError("يجب ربط المنصب إما بوحدة تنظيمية/مصلحة أو بقسم أكاديمي.")
        if self.unit and self.department:
            raise ValidationError("لا يمكن ربط المنصب بوحدة وقسم في نفس الوقت، اختر أحدهما فقط.")

    def __str__(self):
        occupant_name = self.current_occupant.get_full_name() if self.current_occupant and self.current_occupant.get_full_name() else (self.current_occupant.username if self.current_occupant else "شاغر")
        return f"{self.title} ({occupant_name})"