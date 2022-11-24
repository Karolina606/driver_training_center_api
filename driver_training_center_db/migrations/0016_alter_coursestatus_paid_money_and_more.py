# Generated by Django 4.1.1 on 2022-11-24 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0015_alter_course_start_date_alter_lesson_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursestatus',
            name='paid_money',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='drivinglicensecategory',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='drivinglicensecategory',
            name='practice_full_time',
            field=models.DecimalField(decimal_places=0, max_digits=100),
        ),
        migrations.AlterField(
            model_name='drivinglicensecategory',
            name='theory_full_time',
            field=models.DecimalField(decimal_places=0, max_digits=100),
        ),
    ]
