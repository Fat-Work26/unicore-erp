from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import datetime

from accounts.models import TeacherProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'توليد بيانات وهمية تجريبية للمشروع'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('جاري إنشاء البيانات الوهمية...'))

        fake = Faker('ar_SA')

        # 1. إنشاء حساب مدير النظام (Admin)
        admin_user, created = User.objects.get_or_create(
            username='admin_demo',
            defaults={
                'email': 'admin@unicore-demo.edu',
                'user_type': User.UserType.STAFF,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('demo12345')
            admin_user.save()

        # 2. إنشاء حسابات وقواعد بيانات الأساتذة
        for i in range(5):
            username = f'teacher_{i+1}'
            if not User.objects.filter(username=username).exists():
                teacher = User.objects.create_user(
                    username=username,
                    email=f'teacher{i+1}@unicore-demo.edu',
                    password='demo12345',
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    user_type=User.UserType.TEACHER
                )
               
                # إنشاء الملف الشخصي المطابق للنموذج
                TeacherProfile.objects.create(
                    user=teacher,
                    first_name_ar=fake.first_name(),
                    last_name_ar=fake.last_name(),
                    employee_id=f'EMP-2026-{i+100}',
                    rank='أستاذ محاضر أ',
                    grade='الدرجة 3',
                    office_location=f'B-{100 + i}',
                    joining_date=datetime.date(2020, 1, 15),
                    phone_number=fake.phone_number()
                )

        self.stdout.write(self.style.SUCCESS('تم إنشاء البيانات الوهمية بنجاح!'))