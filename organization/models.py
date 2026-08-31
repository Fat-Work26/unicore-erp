from django.db import models
from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

class OrganizationalTemplate(models.Model):
    UNIT_TYPES = [
        ('UNIVERSITY', 'جامعة / رئاسة الجامعة'),
        ('FACULTY', 'كلية / معهد'),
        ('DEANERY', 'عمادة / نيابة عمادة'),
        ('SECRETARIAT', 'أمانة عامة'),
        ('DEPARTMENT', 'قسم أكاديمي'),
        ('SERVICE', 'مصلحة'),
        ('BRANCH', 'فرع'),
        ('LIBRARY', 'مكتبة'),
    ]
    name = models.CharField(max_length=255, verbose_name="اسم الوحدة النمطي")
    code = models.CharField(max_length=50, unique=True, verbose_name="الرمز الموحد")
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPES, verbose_name="نوع الوحدة")
    
    # الشجرة النمطية المرجعية
    parent_template = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children',
        verbose_name="الوحدة النمطية الأعلى"
    )

    class Meta:
        verbose_name = "نموذج هيكلي قانوني"
        verbose_name_plural = "نماذج هيكلية قانونية"

    def __str__(self):
        return self.name


class OrganizationalUnit(models.Model):
    # Prevent deletion of the template if it is referenced by any live units (Data Safety Lock)
    template = models.ForeignKey(
        OrganizationalTemplate, 
        on_delete=models.PROTECT,
        verbose_name="النموذج الهيكلي القانوني"
    )
    name = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name="اسم الكلية / الكيان"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="الوحدة المباشرة الأعلى"
    )

    class Meta:
        verbose_name = "وحدة تنظيمية"
        verbose_name_plural = "الوحدات التنظيمية"

    def __str__(self):
        return self.name or self.template.name


class PositionType(models.Model):
    title = models.CharField(max_length=150, verbose_name="مسمى المنصب")
    code = models.SlugField(max_length=50, unique=True, verbose_name="رمز المنصب")
    description = models.TextField(null=True, blank=True, verbose_name="الوصف الوظيفي")

    class Meta:
        verbose_name = "نوع المنصب"
        verbose_name_plural = "أنواع المناصب"

    def __str__(self):
        return self.title


class PositionAssignment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='position_assignments',
        verbose_name="الموظف / الأستاذ"
    )
    
    position_type = models.ForeignKey(
        PositionType,
        on_delete=models.PROTECT,
        verbose_name="نوع المنصب"
    )
    
    unit = models.ForeignKey(
        OrganizationalUnit,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name="الوحدة التنظيمية"
    )
    
    start_date = models.DateField(verbose_name="تاريخ بداية التكليف")
    end_date = models.DateField(null=True, blank=True, verbose_name="تاريخ نهاية التكليف")
    is_active = models.BooleanField(default=True, verbose_name="منصب حالي نشط")

    class Meta:
        verbose_name = "تعيين في منصب"
        verbose_name_plural = "تعيينات المناصب"

    def __str__(self):
        return f"{self.user} - {self.position_type.title} ({self.unit.template.name})"






def ensure_template_sync_for_unit(parent_unit, template_node, faculty_root):
    """
    دالة عودية تضمن نقل العقدة القديمة إلى الأب الجديد، 
    وحذف أي نسخ مكررة معلقة بشكل مباشر ومؤكد في قاعدة البيانات.
    """
    for child_template in template_node.children.all():
        
        # 1. البحث عن كافة الوحدات التابعة لنفس القالب ونفس الكلية الميدانية
        # نأخذ العقد التي تبدأ مسيرتها من نفس الكلية الجذرية
        all_faculty_units = OrganizationalUnit.objects.filter(template=child_template)
        
        target_units = []
        for u in all_faculty_units:
            # التحقق من انتمائها لنفس الكلية
            curr = u
            while curr and curr.template.unit_type != 'FACULTY':
                curr = curr.parent
            if curr and curr.id == faculty_root.id:
                target_units.append(u)

        if target_units:
            # 2. احتفاظ بأول عقدة وتحديدها كعقدة رسمية
            main_unit = target_units[0]
            
            # تحديث الأب المباشر فوراً إذا كان مختلفاً
            if main_unit.parent_id != parent_unit.id:
                OrganizationalUnit.objects.filter(id=main_unit.id).update(parent=parent_unit)
                main_unit.parent = parent_unit

            # 3. الحذف الفوري والمباشر لأي سجلات مكررة زائفة داخل قاعدة البيانات
            if len(target_units) > 1:
                duplicate_ids = [u.id for u in target_units[1:]]
                OrganizationalUnit.objects.filter(id__in=duplicate_ids).delete()
            
            child_unit = main_unit
        else:
            # 4. الإنشاء فقط إذا لم تكن العقدة موجودة نهائياً
            child_unit = OrganizationalUnit.objects.create(
                template=child_template,
                parent=parent_unit
            )

        # 5. التراسل العودي لباقي المستويات (الأحفاد)
        ensure_template_sync_for_unit(child_unit, child_template, faculty_root)


@receiver(post_save, sender=OrganizationalTemplate)
def sync_template_tree_changes(sender, instance, **kwargs):
    """مزامنة حاسمة وتصحيح كامل للهيكل عند أي تغيير في القوالب"""
    with transaction.atomic():
        faculties = OrganizationalUnit.objects.filter(template__unit_type='FACULTY')
        for faculty in faculties:
            ensure_template_sync_for_unit(faculty, faculty.template, faculty)






# مهام وقوانين المنصب التنظيمي (مرتبطة بنوع المنصب نفسه وليس بالوحدة)
class PositionRegulation(models.Model):
    position_type = models.OneToOneField(
        'PositionType',  # أو اسم النموذج المسؤول عن المناصب لديك
        on_delete=models.CASCADE, 
        related_name='regulation', 
        verbose_name="المنصب الإداري"
    )
    tasks = models.TextField(verbose_name="المهام الوظيفية والمشاريع")
    laws_and_rules = models.TextField(verbose_name="القوانين واللوائح المنظمة للمنصب")

    class Meta:
        verbose_name = "مهام وقوانين المنصب"
        verbose_name_plural = "مهام وقوانين المناصب"

    def __str__(self):
        return f"قوانين ومهام منصب: {self.position_type.title}"