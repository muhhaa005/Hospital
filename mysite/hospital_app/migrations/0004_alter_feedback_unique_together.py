# Generated by Django 5.1.7 on 2025-03-24 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0003_alter_doctor_work_day'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='feedback',
            unique_together=set(),
        ),
    ]
