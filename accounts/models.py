from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT'
        TEACHER = 'TEACHER'
        SUPER_ADMIN = 'SUPER_ADMIN'
        ADMIN = 'ADMIN'
    role = models.CharField(max_length=20,choices=Role.choices, verbose_name="نوع الحساب")
    num_inscription = models.CharField(max_length=50, unique =True, verbose_name='رقم التسجيل')