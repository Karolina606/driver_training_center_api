# Generated by Django 4.1.1 on 2022-11-23 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0014_alter_course_start_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='start_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
