# Generated by Django 4.1.1 on 2022-10-12 18:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'course',
            },
        ),
        migrations.CreateModel(
            name='DrivingLicenseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('theory_full_time', models.DecimalField(decimal_places=0, max_digits=100)),
                ('practice_full_time', models.DecimalField(decimal_places=0, max_digits=100)),
            ],
            options={
                'db_table': 'driving_license_category',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('T', 'theory'), ('P', 'practice')], max_length=20)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_lessons', to='db.course')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructor_lessons', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'lesson',
            },
        ),
        migrations.CreateModel(
            name='CourseStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_money', models.DecimalField(decimal_places=2, max_digits=6)),
                ('is_course_paid', models.BooleanField(default=False)),
                ('is_internal_theoretical_exam_passed', models.BooleanField(default=False)),
                ('is_internal_practical_exam_passed', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_status_for_student', to='db.course')),
                ('lessons', models.ManyToManyField(related_name='lesson_student_course_status', to='db.lesson')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_course_status', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'course_status',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='driving_license_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='db.drivinglicensecategory'),
        ),
    ]