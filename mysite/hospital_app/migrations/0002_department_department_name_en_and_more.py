# Generated by Django 5.1.7 on 2025-03-23 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='department_name_en',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='department',
            name='department_name_ru',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='bio_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='bio_ru',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='specialty',
            name='specialty_name_en',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='specialty',
            name='specialty_name_ru',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
