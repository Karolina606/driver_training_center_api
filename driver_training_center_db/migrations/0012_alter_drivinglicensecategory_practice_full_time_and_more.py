# Generated by Django 4.1.1 on 2022-11-23 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0011_alter_drivinglicensecategory_practice_full_time_and_more'),
    ]

    operations = [
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
