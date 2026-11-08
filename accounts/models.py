from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    class UserType(models.TextChoices):
        STUDENT = 'STUDENT'
        TEACHER = 'TEACHER'
        SUPER_ADMIN = 'SUPER_ADMIN'
        STAFF = 'STAFF'
    user_type = models.CharField(
        max_length=50,
        choices=UserType.choices,
        verbose_name="نوع الحساب")
    email = models.EmailField(
        unique =True,
        null   =True,
        blank  =True,
        default=None,
        )
    # num_inscription is unique for students.
    # null=True & default=None are required to allow multiple non-student accounts 
    # (like Teachers) to coexist without violating the UNIQUE constraint in PostgreSQL.
    num_inscription = models.CharField(
        max_length=50, 
        unique =True,
        null   =True,
        blank  =True,
        default=None, 
        verbose_name='رقم التسجيل')#for studiant

# ************************************************************************
#
# ************************************************************************
class Teacher(User):
    class Meta:
        proxy = True
        # verbose_name = 'استاذ'
        # verbose_name_plural = 'الأساتذة'

class Student(User):
    class Meta:
        proxy = True

class Staff(User):
    class Meta:
        proxy = True        
# *****************************
class TeacherProfile(models.Model):
    # 1. الربط بالحساب الرئيسي
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        # verbose_name="الحساب"
    )
    # 2. البيانات الهوية والشخصية (ضرورية للوثائق)
    first_name_ar = models.CharField(max_length=50, verbose_name="الاسم بالعربية")
    last_name_ar = models.CharField(max_length=50, verbose_name="اللقب بالعربية")
    birth_date = models.DateField(null=True, blank=True, verbose_name="تاريخ الميلاد")
    birth_place = models.CharField(max_length=100, verbose_name="مكان الميلاد")
    photo = models.ImageField(default='default.jpg',upload_to='teachers/photos/', null=True, blank=True, verbose_name="الصورة الشخصية")
    cv = models.FileField(upload_to='teachers/cvs/', blank=True, null=True, verbose_name="السيرة الذاتية (PDF)")
   # 3. البيانات المهنية والأكاديمية
    employee_id = models.CharField(max_length=50, unique=True, verbose_name="الرقم الوظيفي / المعرف")
    rank = models.CharField(max_length=50, verbose_name="الرتبة الأكاديمية") # مثال: أستاذ محاضر أ، أستاذ تعليم عالي
    grade = models.CharField(max_length=50, verbose_name="الدرجة") # مثال: الدرجة 1، 2...
    
    # 4. التواريخ الإدارية (لاستخراج شهادات العمل والتثبيت)
    joining_date = models.DateField(verbose_name="تاريخ أول الالتحاق")
    confirmation_date = models.DateField(null=True, blank=True, verbose_name="تاريخ التثبيت")
 
    # 5. معلومات التواصل والتواجد
    phone_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="رقم الهاتف")
    office_location = models.CharField(max_length=100, blank=True, null=True, verbose_name="رقم/موقع المكتب")
    
    
    bio = models.TextField(blank=True, null=True, verbose_name="نبذة مختصرة")

    #6. التبعية الأكاديمية الأصلية (الأساسية)
    home_university = models.CharField(max_length=200, null=True, blank=True, verbose_name="الجامعة الأصلية")
    home_college = models.CharField(max_length=200, null=True, blank=True,verbose_name="الكلية الأصلية")
    home_department = models.CharField(max_length=200, null=True, blank=True, verbose_name="القسم الأصلي")
   
    # class Meta:
        # verbose_name = "ملف أستاذ"
        # verbose_name_plural = "ملفات الأساتذة"
    def __str__(self):
        return f"أستاذ: {self.first_name_ar} {self.last_name_ar}"


# 1. المؤهلات العلمية (مرتبطة بملف الأستاذ)
class Qualification(models.Model):
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='qualifications', verbose_name="الأستاذ")
    degree = models.CharField(max_length=100, verbose_name="الشهادة / المؤهل") # مثال: دكتوراه، ماجستير
    specialty = models.CharField(max_length=200, verbose_name="التخصص") # مثال: الدراسات القضائية، علوم الحاسوب
    institution = models.CharField(max_length=200, verbose_name="المؤسسة / الجامعة") # مثال: جامعة أم القرى
    year = models.IntegerField(verbose_name="سنة الحصول عليها")

    class Meta:
        ordering = ['-year']
        verbose_name = "مؤهل علمي"
        verbose_name_plural = "المؤهلات العلمية"

    def __str__(self):
        return f"{self.degree} - {self.teacher.last_name_ar}"

# 2. الأبحاث والمنشورات العلمية (مرتبطة بملف الأستاذ)
class Research(models.Model):
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='researches', verbose_name="الأستاذ")
    title = models.CharField(max_length=500, verbose_name="عنوان البحث / المقال")
    journal = models.CharField(max_length=300, verbose_name="المجلة / الناشر")
    year = models.IntegerField(verbose_name="سنة النشر")
    link = models.URLField(blank=True, null=True, verbose_name="رابط البحث")

    class Meta:
        ordering = ['-year']
        verbose_name = "بحث علمي"
        verbose_name_plural = "الأبحاث العلمية"

    def __str__(self):
        return self.title

# account/models.py
class AcademicAffiliation(models.Model):
    class AffiliationType(models.TextChoices):
        PRIMARY = 'PRIMARY', 'أستاذ دائم / أصلي'
        ASSOCIATE = 'ASSOCIATE', 'أستاذ مشارك'
        VISITING = 'VISITING', 'أستاذ زائر / منتدب'
        ADJUNCT = 'ADJUNCT', 'أستاذ متعاقد'

    teacher = models.ForeignKey(
        TeacherProfile, 
        on_delete=models.CASCADE, 
        related_name='affiliations', 
        verbose_name="الأستاذ"
    )
    university_name = models.CharField(max_length=200, verbose_name="الجامعة")
    college_name = models.CharField(max_length=200, verbose_name="الكلية")
    department_name = models.CharField(max_length=200, verbose_name="القسم")
    
    role_type = models.CharField(
        max_length=20, 
        choices=AffiliationType.choices, 
        default=AffiliationType.ASSOCIATE, 
        verbose_name="نوع الانتماء / الصفة"
    )
    is_active = models.BooleanField(default=True, verbose_name="نشط حالياً")

    class Meta:
        verbose_name = "انتماء أكاديمي"
        verbose_name_plural = "الانتماءات الأكاديمية"

    def __str__(self):
        return f"{self.get_role_type_display()} - {self.department_name} ({self.university_name})"



# *****************************
class StaffProfile(models.Model):
    # 1. الربط بالحساب الرئيسي
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_profile',
        # verbose_name="الحساب"
    )
    # 2. البيانات الهوية والشخصية (ضرورية للوثائق)
    first_name_ar = models.CharField(max_length=50, verbose_name="الاسم بالعربية")
    last_name_ar = models.CharField(max_length=50, verbose_name="اللقب بالعربية")
    birth_date = models.DateField(null=True, blank=True, verbose_name="تاريخ الميلاد")
    birth_place = models.CharField(max_length=100, verbose_name="مكان الميلاد")
    photo = models.ImageField(default='default.jpg',upload_to='staff/photos/', null=True, blank=True, verbose_name="الصورة الشخصية")
   
   # 3. البيانات المهنية والأكاديمية
    employee_id = models.CharField(max_length=50, unique=True, verbose_name="الرقم الوظيفي / المعرف")
    grade = models.CharField(max_length=50, verbose_name="الدرجة") # مثال: الدرجة 1، 2...
    
    # 4. التواريخ الإدارية (لاستخراج شهادات العمل والتثبيت)
    joining_date = models.DateField(verbose_name="تاريخ أول الالتحاق")
    confirmation_date = models.DateField(null=True, blank=True, verbose_name="تاريخ التثبيت")

    # 5. معلومات التواصل والتواجد
    phone_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="رقم الهاتف")
    office_location = models.CharField(max_length=100, blank=True, null=True, verbose_name="رقم/موقع المكتب")
    
    
    bio = models.TextField(blank=True, null=True, verbose_name="نبذة مختصرة")

    # class Meta:
        # verbose_name = "ملف أستاذ"
        # verbose_name_plural = "ملفات الأساتذة"

    def __str__(self):
        return f"موظف: {self.first_name_ar} {self.last_name_ar}"
 

class StaffQualification(models.Model):
    staff = models.ForeignKey('StaffProfile', on_delete=models.CASCADE, related_name='qualifications')
    title = models.CharField(max_length=150, verbose_name="اسم الشهادة / المؤهل")
    institution = models.CharField(max_length=150, verbose_name="المؤسسة / الجامعة")
    year = models.IntegerField(verbose_name="سنة الحصول عليها")

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.title} - {self.staff}"

class StaffPromotion(models.Model):
    staff = models.ForeignKey('StaffProfile', on_delete=models.CASCADE, related_name='promotions')
    previous_grade = models.CharField(max_length=50, verbose_name="الدرجة/الرتبة السابقة")
    new_grade = models.CharField(max_length=50, verbose_name="الدرجة/الرتبة الجديدة")
    promotion_date = models.DateField(verbose_name="تاريخ الترقية")
    decision_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="رقم القرار الإداري")

    class Meta:
        ordering = ['-promotion_date']

    def __str__(self):
        return f"ترقية {self.staff} إلى {self.new_grade}"
