import datetime
import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker

# استدعاء الملفات الشخصية للأساتذة والموظفين
from accounts.models import TeacherProfile, StaffProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'توليد بيانات وهمية تجريبية للأساتذة والموظفين الإداريين'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('جاري بدء إنشاء البيانات الوهمية...'))

        fake = Faker('ar_SA')

        # الرتب والدرجات الأكاديمية والإدارية لزيادة تنوع البيانات
        ranks = ['أستاذ تعليم عالي', 'أستاذ محاضر أ', 'أستاذ محاضر ب', 'أستاذ مساعد أ']
        grades = [f'الدرجة {i}' for i in range(1, 13)]

        # 1. إنشاء حساب مدير النظام (Super Admin)
        admin_user, created = User.objects.get_or_create(
            username='admin_demo',
            defaults={
                'email': 'admin@unicore-demo.edu',
                'user_type': User.UserType.SUPER_ADMIN,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('demo12345')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('✔ تم إنشاء حساب المسؤول: admin_demo'))

        # 2. إنشاء بيانات الأساتذة (20 أستاذ)
        for i in range(20):
            username = f'teacher_{i+1}'
            if not User.objects.filter(username=username).exists():
                first_name_ar = fake.first_name()
                last_name_ar = fake.last_name()

                teacher = User.objects.create_user(
                    username=username,
                    email=f'teacher{i+1}@unicore-demo.edu',
                    password='demo12345',
                    first_name=first_name_ar,
                    last_name=last_name_ar,
                    user_type=User.UserType.TEACHER
                )

                joining_date = fake.date_between(start_date='-10y', end_date='-2y')
                
                TeacherProfile.objects.create(
                    user=teacher,
                    first_name_ar=first_name_ar,
                    last_name_ar=last_name_ar,
                    birth_date=fake.date_of_birth(minimum_age=30, maximum_age=65),
                    birth_place=fake.city(),
                    employee_id=f'EMP-T-{2026}-{i+100}',
                    rank=random.choice(ranks),
                    grade=random.choice(grades),
                    joining_date=joining_date,
                    confirmation_date=joining_date + datetime.timedelta(days=365),
                    phone_number=f"0{random.choice(['5', '6', '7'])}{fake.msisdn()[5:]}",
                    office_location=f'مكتب {random.randint(101, 305)} - C',
                    bio=fake.paragraph(nb_sentences=2)
                )

        self.stdout.write(self.style.SUCCESS('✔ تم إنشاء 20 حساب بروفايل للأساتذة.'))

        # 3. إنشاء بيانات الموظفين الإداريين (15 موظف)
        for i in range(30):
            username = f'staff_{i+1}'
            if not User.objects.filter(username=username).exists():
                first_name_ar = fake.first_name()
                last_name_ar = fake.last_name()

                staff_user = User.objects.create_user(
                    username=username,
                    email=f'staff{i+1}@unicore-demo.edu',
                    password='demo12345',
                    first_name=first_name_ar,
                    last_name=last_name_ar,
                    user_type=User.UserType.STAFF,
                    is_staff=True  # لإتاحة الوصول للوحة التحكم عند الحاجة
                )

                joining_date = fake.date_between(start_date='-8y', end_date='-1y')

                StaffProfile.objects.create(
                    user=staff_user,
                    first_name_ar=first_name_ar,
                    last_name_ar=last_name_ar,
                    birth_date=fake.date_of_birth(minimum_age=25, maximum_age=60),
                    birth_place=fake.city(),
                    employee_id=f'EMP-S-{2026}-{i+200}',
                    grade=random.choice(grades),
                    joining_date=joining_date,
                    confirmation_date=joining_date + datetime.timedelta(days=365),
                    phone_number=f"0{random.choice(['5', '6', '7'])}{fake.msisdn()[5:]}",
                    office_location=f'مكتب الإدارة {random.randint(1, 20)}',
                    bio=fake.paragraph(nb_sentences=2)
                )

        self.stdout.write(self.style.SUCCESS('✔ تم إنشاء 15 حساب بروفايل للموظفين الإداريين.'))
        self.stdout.write(self.style.SUCCESS('✨ اكتملت عملية إنشاء البيانات التجريبية بنجاح!'))