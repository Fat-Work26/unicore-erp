from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from organization.models import Departement

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
   
   # 3. البيانات المهنية والأكاديمية
    employee_id = models.CharField(max_length=50, unique=True, verbose_name="الرقم الوظيفي / المعرف")
    # ربط الأستاذ بقسمه الرئيسي
    department = models.ForeignKey(
        Departement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teachers',
        verbose_name="القسم"
    )
    rank = models.CharField(max_length=50, verbose_name="الرتبة الأكاديمية") # مثال: أستاذ محاضر أ، أستاذ تعليم عالي
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
        return f"أستاذ: {self.first_name_ar} {self.last_name_ar}"
