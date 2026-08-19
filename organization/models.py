from django.db import models
from django.conf import settings

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




# from django.db.models.signals import post_save
# from django.dispatch import receiver


# code 1
# # 1. الدالة العودية لإنشاء كافة الفروع عند إضافة كلية جديدة
# def create_children_from_template(parent_unit, template_node):
#     for child_template in template_node.children.all():
#         new_unit = OrganizationalUnit.objects.create(
#             template=child_template,
#             parent=parent_unit
#         )
#         create_children_from_template(new_unit, child_template)


# # 2. الإشارة الأولى: عند إنشاء كلية جديدة في OrganizationalUnit
# @receiver(post_save, sender=OrganizationalUnit)
# def auto_populate_faculty_structure(sender, instance, created, **kwargs):
#     if created and instance.template.unit_type == 'FACULTY':
#         faculty_template = instance.template
#         create_children_from_template(instance, faculty_template)


# # 3. الإشارة الثانية: عند إضافة مصلحة جديدة في OrganizationalTemplate لتحديث الكليات الحالية
# @receiver(post_save, sender=OrganizationalTemplate)
# def sync_new_template_to_existing_faculties(sender, instance, created, **kwargs):
#     if created and instance.parent_template:
#         faculties = OrganizationalUnit.objects.filter(template__unit_type='FACULTY')
        
#         for faculty in faculties:
#             # البحث عن الأب المناسب داخل الكلية
#             if instance.parent_template.unit_type == 'FACULTY':
#                 parent_unit = faculty
#             else:
#                 parent_unit = OrganizationalUnit.objects.filter(
#                     template=instance.parent_template,
#                     parent=faculty
#                 ).first()

#             if parent_unit:
#                 OrganizationalUnit.objects.get_or_create(
#                     template=instance,
#                     parent=parent_unit
#                 )

# code 2

# def ensure_template_sync_for_unit(parent_unit, template_node):
#     """دالة عودية تضمن استنساخ وتحديث كل الفروع والمصالح التابعة للقالب لكل وحدة منشأة"""
#     for child_template in template_node.children.all():
#         # إنشاء أو جلب الوحدة التابعة لهذه الكلية/المصلحة تحديداً
#         child_unit, _ = OrganizationalUnit.objects.get_or_create(
#             template=child_template,
#             parent=parent_unit
#         )
#         # الاستمرار عودياً لمزامنة الأحفاد (مثل الفروع تحت المصالح)
#         ensure_template_sync_for_unit(child_unit, child_template)


# @receiver(post_save, sender=OrganizationalTemplate)
# def sync_new_template_to_existing_faculties(sender, instance, created, **kwargs):
#     """عند إضافة أي عنصر جديد في القالب (سواء مصلحة أو فرع)، يُزامن فوراً مع جميع الكليات"""
#     if created:
#         faculties = OrganizationalUnit.objects.filter(template__unit_type='FACULTY')
#         for faculty in faculties:
#             ensure_template_sync_for_unit(faculty, faculty.template)


# @receiver(post_save, sender=OrganizationalTemplate)
# def sync_parent_change_to_existing_units(sender, instance, created, **kwargs):
#     """تحديث الوحدة الأعلى آلياً للوحدات الميدانية عند تعديل الأب في القالب القياسي"""
#     if not created and instance.parent_template:
#         # جلب كافة الوحدات الميدانية المرتبطة بهذا القالب
#         units = OrganizationalUnit.objects.filter(template=instance)
        
#         for unit in units:
#             # العثور على الكلية التابعة لها هذه الوحدة
#             faculty = unit.parent
#             while faculty and faculty.template and faculty.template.unit_type != 'FACULTY':
#                 faculty = faculty.parent

#             if faculty:
#                 # البحث عن الأب الجديد الصحيح داخل نفس الكلية
#                 new_parent = OrganizationalUnit.objects.filter(
#                     template=instance.parent_template,
#                     parent=faculty if instance.parent_template.unit_type != 'FACULTY' else None
#                 ).first()
                
#                 if new_parent and unit.parent != new_parent:
#                     unit.parent = new_parent
#                     unit.save()




# code 3
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# def ensure_template_sync_for_unit(parent_unit, template_node):
#     """دالة عودية تضمن استنساخ وتحديث وتصحيح أب الفروع والمصالح التابعة للقالب"""
#     for child_template in template_node.children.all():
#         # 1. البحث عن الوحدة بالاعتماد على القالب ونفس الكلية/الجذر
#         child_unit = OrganizationalUnit.objects.filter(
#             template=child_template,
#             parent__template=parent_unit.template
#         ).first()

#         if child_unit:
#             # إذا كانت موجودة مسبقاً وتغير أبوه القياسي، نقوم بتحديث الـ parent فوراً
#             if child_unit.parent_id != parent_unit.id:
#                 child_unit.parent = parent_unit
#                 child_unit.save(update_fields=['parent'])
#         else:
#             # إذا لم تكن موجودة نهائياً، أنشئها تحت الأب الصحيح
#             child_unit = OrganizationalUnit.objects.create(
#                 template=child_template,
#                 parent=parent_unit
#             )

#         # 2. الاستمرار عودياً لنزول المستويات الأعمق (مثل الفروع تحت المصالح)
#         ensure_template_sync_for_unit(child_unit, child_template)


# @receiver(post_save, sender=OrganizationalTemplate)
# def sync_new_template_to_existing_faculties(sender, instance, created, **kwargs):
#     """عند إضافة أو تعديل عنصر في القالب، يُزامن فوراً مع كافة الكليات"""
#     faculties = OrganizationalUnit.objects.filter(template__unit_type='FACULTY')
#     for faculty in faculties:
#         ensure_template_sync_for_unit(faculty, faculty.template)



# code4
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# def ensure_template_sync_for_unit(parent_unit, template_node):
#     """دالة عودية تضمن تحديث مكان الفروع والمصالح التابعة بدلاً من تكرارها"""
#     for child_template in template_node.children.all():
        
#         # 1. إيجاد الكلية الجذرية التي تنتمي لها هذه الوحدة
#         faculty_root = parent_unit
#         while faculty_root.parent and faculty_root.template.unit_type != 'FACULTY':
#             faculty_root = faculty_root.parent

#         # 2. البحث عن أي فرع موجود مسبقاً بنفس القالب داخل نفس الكلية
#         child_unit = OrganizationalUnit.objects.filter(
#             template=child_template,
#             parent__tree_id=parent_unit.tree_id  # أو البحث ضمن نفس الكلية الجذرية
#         ).first() if hasattr(parent_unit, 'tree_id') else None

#         if not child_unit:
#             # البحث بمرونة أوسع داخل الكلية نفسها لمنع التكرار
#             child_unit = OrganizationalUnit.objects.filter(template=child_template).first()

#         if child_unit:
#             # إذا كان موجوداً مسبقاً، نكتفي بنقله للأب الصحيح
#             if child_unit.parent_id != parent_unit.id:
#                 child_unit.parent = parent_unit
#                 child_unit.save(update_fields=['parent'])
#         else:
#             # إنشاء فقط في حالة عدم وجوده مطلقاً
#             child_unit = OrganizationalUnit.objects.create(
#                 template=child_template,
#                 parent=parent_unit
#             )

#         # 3. الاستمرار عودياً مع باقي الأحفاد
#         ensure_template_sync_for_unit(child_unit, child_template)


# @receiver(post_save, sender=OrganizationalTemplate)
# def sync_new_template_to_existing_faculties(sender, instance, created, **kwargs):
#     """مزامنة فورية لكافة الكليات عند تعديل أي قالب"""
#     faculties = OrganizationalUnit.objects.filter(template__unit_type='FACULTY')
#     for faculty in faculties:
#         ensure_template_sync_for_unit(faculty, faculty.template)


# code 5
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

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









